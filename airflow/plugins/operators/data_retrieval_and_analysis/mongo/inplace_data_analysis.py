from airflow.models.baseoperator import BaseOperator
from pymongo import MongoClient

from operators.data_retrieval_and_analysis.constants.lookup import personal_data_value_patterns
from operators.data_retrieval_and_analysis.utils.common import get_uri


class Inplace_mongo_data_analysis(BaseOperator):
    def __init__(self, storage: dict, storage_name: str, *args, **kwargs):
        super().__init__(**kwargs)
        self.storage_name = storage_name
        self.connection_uri = get_uri(storage, "mongo")

    def execute(self, context):
        meta_data = context["task_instance"].xcom_pull(
            key=f"{context['dag_run'].run_id}*meta_data*{self.storage_name}")

        database_error = meta_data.get('error')
        findings = {}
        if database_error:
            findings = {'error': database_error}
            meta_data = {
                key: value
                for key, value in meta_data if key != 'error'
            }

        with MongoClient(self.connection_uri) as client:
            for collection_identifier, collection_meta in meta_data.items():
                collection_identifier_list = collection_identifier.split(".")
                if not len(collection_identifier_list) == 2:
                    continue
                db_name = collection_identifier_list[0]
                collection_name = collection_identifier_list[1]
                db = client[db_name]
                collection = db[collection_name]
                for field in collection_meta.get("keys"):
                    for pattern_name, pattern in personal_data_value_patterns.items(
                    ):
                        matches = []
                        try:
                            match_cursor = collection.distinct(
                                "_id", {field: {
                                    "$regex": pattern
                                }})
                            matches = [
                                str(object_id) for object_id in match_cursor
                            ]
                        except Exception as e:
                            findings = {
                                **findings, f"{db_name}.{collection_name}": {
                                    **findings.get(
                                        f"{db_name}.{collection_name}", {}), field:
                                    {
                                        'error': repr(e)
                                    }
                                }
                            }
                        findings = {
                            **findings, f"{db_name}.{collection_name}": {
                                **findings.get(f"{db_name}.{collection_name}", {}),
                                **({field: {
                                    **findings.get(f"{db_name}.{collection_name}", {}).get(field, {}),
                                    **({f"{pattern_name}_pattern": {"references": matches}} if matches else {})
                                }} if matches or findings.get(f"{db_name}.{collection_name}", {}).get(field) else {})
                            }
                        }

        context["task_instance"].xcom_push(
            key=
            f"{context['dag_run'].run_id}*data_analysis*{self.storage_name}",
            value=findings)

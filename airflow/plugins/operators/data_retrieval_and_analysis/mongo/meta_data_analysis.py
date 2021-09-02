from airflow.models.baseoperator import BaseOperator

from operators.data_retrieval_and_analysis.constants.lookup import personal_data_value_patterns, personal_data_key_words
from operators.data_retrieval_and_analysis.utils.nlp import process_proximity_of_items, process_proximity


class Analyze_mongo_meta(BaseOperator):
    def __init__(self, storage_name: str, *args, **kwargs):
        super().__init__(**kwargs)
        self.storage_name = storage_name

    def execute(self, context):
        meta_data = context["task_instance"].xcom_pull(
            key=f"{context['dag_run'].run_id}*meta_data*{self.storage_name}")
        database_error = meta_data.get('error')
        findings = {"storage_type": "mongo"}
        if database_error:
            findings = {**findings, 'error': database_error}
            meta_data = {
                key: value
                for key, value in meta_data if key != 'error'
            }

        for collection, collection_meta in meta_data.items():
            key_names = collection_meta.get('keys', [])
            key_proximities = process_proximity_of_items(
                key_names, personal_data_key_words)
            collection_findings = {
                'number_of_entities':
                collection_meta.get('number_of_entities'),
                **({
                    "key_proximities": key_proximities
                } if len(key_proximities) else {}), "key_names":
                key_names
            }
            findings = {**findings, collection: collection_findings}

        context["task_instance"].xcom_push(
            key=
            f"{context['dag_run'].run_id}*meta_data_analysis*{self.storage_name}",
            value=findings)

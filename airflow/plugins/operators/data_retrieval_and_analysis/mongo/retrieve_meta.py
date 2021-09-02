from airflow.models.baseoperator import BaseOperator
from pymongo import MongoClient

from operators.data_retrieval_and_analysis.constants.lookup import mongo_internal_collections, mongo_internal_keys
from operators.data_retrieval_and_analysis.utils.common import get_uri

# query source: https://stackoverflow.com/a/43570730/15139328 / accessed on 2021-6-29
meta_data_query = [{
    "$project": {
        "list_of_keys": {
            "$objectToArray": "$$ROOT"
        }
    }
}, {
    "$unwind": "$list_of_keys"
}, {
    "$group": {
        "_id": "",
        "keys": {
            "$addToSet": "$list_of_keys.k"
        }
    }
}]


class Retrieve_mongo_meta(BaseOperator):
    def __init__(self, storage: dict, storage_name: str, *args, **kwargs):
        super().__init__(**kwargs)
        self.storage_name = storage_name
        self.connection_uri = get_uri(storage, "mongo")

    def execute(self, context):
        meta_data = {}
        with MongoClient(self.connection_uri) as client:
            database_names = client.list_database_names()
            user_databases = [
                db_name for db_name in database_names
                if db_name not in mongo_internal_collections
            ]
            for database_name in user_databases:
                db = client[database_name]
                collection_names = db.list_collection_names()
                for collection_name in collection_names:
                    collection_stats = db.command("collstats", collection_name)
                    keys_cursor = db[collection_name].aggregate(
                        meta_data_query)
                    keys = [
                        key for key in list(keys_cursor)[0].get("keys")
                        if key not in mongo_internal_keys
                    ]
                    meta_data = {
                        **meta_data,
                        collection_stats.get("ns"): {
                            "number_of_entities":
                            collection_stats.get("count"),
                            "collection_uri":
                            collection_stats.get("indexDetails",
                                                 {}).get("_id_",
                                                         {}).get("uri"),
                            "keys":
                            keys
                        }
                    }

        context["task_instance"].xcom_push(
            key=f"{context['dag_run'].run_id}*meta_data*{self.storage_name}",
            value=meta_data)

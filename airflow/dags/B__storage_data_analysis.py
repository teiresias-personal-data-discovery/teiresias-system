from airflow import DAG
from airflow.sensors.external_task import ExternalTaskSensor
from airflow.operators.python import BranchPythonOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
from airflow.models import Variable
from airflow import DAG
from airflow.utils.trigger_rule import TriggerRule

from datetime import datetime
import time
import logging
import json

from operators.code_analyzer.code_analyzer_operator import Clone_and_analyze_code
from operators.code_analyzer.process_code_analyis_operator import Process_code_analysis
from operators.reporting.reporter import Reporter
from operators.data_retrieval_and_analysis.mongo.retrieve_meta import Retrieve_mongo_meta
from operators.data_retrieval_and_analysis.mongo.meta_data_analysis import Analyze_mongo_meta
from operators.data_retrieval_and_analysis.mongo.inplace_data_analysis import Inplace_mongo_data_analysis
from operators.data_retrieval_and_analysis.postgre.retrieve_meta import Retrieve_postgre_meta
from operators.data_retrieval_and_analysis.postgre.meta_data_analysis import Analyze_postgre_meta
from operators.data_retrieval_and_analysis.postgre.inplace_data_analysis import Inplace_postgre_data_analysis
from operators.data_retrieval_and_analysis.process_data_analyis_operator import Process_data_analysis

mandatory_connection_keys = ['user', 'password', 'host', 'db', 'storage_type']

map_storage_to_task = {
    'mongodb': lambda storage_name: f"retrieve_mongo_meta_data_{storage_name}",
    'postgres':
    lambda storage_name: f"retrieve_postgres_meta_data_{storage_name}",
}


def has_complete_traces(storage):
    if False in [(True if storage.get(key) else False)
                 for key in mandatory_connection_keys]:
        return False
    return True


def get_storage_handler(storage, storage_name):
    def get_storage_handler_callable():
        if not has_complete_traces(storage):
            return f"circuit_{storage_name}"
        storage_type = storage.get("storage_type")
        return map_storage_to_task[storage_type](storage_name)

    return get_storage_handler_callable


with DAG("B_storage_data_analysis",
         start_date=days_ago(1),
         schedule_interval=None) as dag:

    storages: dict = {}
    try:
        storages = {
            storage_name: storage
            for storage_name, storage in Variable.get(
                "storages", deserialize_json=True).items()
            if storage.get("isActive", True)
        }

    except:
        pass

    process_data_analysis = Process_data_analysis(
        task_id="process_data_analysis",
        storage_names=list(storages.keys()),
        trigger_rule=TriggerRule.ALL_DONE)

    for storage_name, storage in storages.items():
        branch_by_storage = BranchPythonOperator(
            task_id=f'handle_storage_{storage_name}',
            python_callable=get_storage_handler(storage, storage_name))

        retrieve_mongo_storage_meta = Retrieve_mongo_meta(
            task_id=f"retrieve_mongo_meta_data_{storage_name}",
            storage=storage,
            storage_name=storage_name)

        inplace_mongo_data_analysis = Inplace_mongo_data_analysis(
            task_id=f"inplace_mongo_data_analysis_{storage_name}",
            storage=storage,
            storage_name=storage_name)

        analyze_mongo_meta = Analyze_mongo_meta(
            task_id=f"analyze_mongo_meta_{storage_name}",
            storage_name=storage_name)

        circuit = DummyOperator(task_id=f"circuit_{storage_name}")

        retrieve_postgres_storage_meta = Retrieve_postgre_meta(
            task_id=f"retrieve_postgres_meta_data_{storage_name}",
            storage=storage,
            storage_name=storage_name)

        inplace_postgre_data_analysis = Inplace_postgre_data_analysis(
            task_id=f"inplace_postgre_data_analysis_{storage_name}",
            storage=storage,
            storage_name=storage_name)

        analyze_postgre_meta = Analyze_postgre_meta(
            task_id=f"analyze_postgre_meta_{storage_name}",
            storage_name=storage_name)

        branch_by_storage >> [
            retrieve_mongo_storage_meta, retrieve_postgres_storage_meta,
            circuit
        ]
        retrieve_mongo_storage_meta >> [
            analyze_mongo_meta, inplace_mongo_data_analysis
        ] >> process_data_analysis
        retrieve_postgres_storage_meta >> [
            analyze_postgre_meta, inplace_postgre_data_analysis
        ] >> process_data_analysis
        circuit >> process_data_analysis

    report_data_analysis = Reporter(task_id="report_data_analysis",
                                    loggin_task="storage_data_analyzer",
                                    with_timeout=0)

    process_data_analysis >> report_data_analysis

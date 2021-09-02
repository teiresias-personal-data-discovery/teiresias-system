from airflow.models.baseoperator import BaseOperator
from airflow.models import Variable

from pymongo import MongoClient
import json
from datetime import datetime
from threading import Thread, Event
import time

breaker = Event()


def timeout_fn():
    while True:
        time.sleep(1)
        if breaker.is_set():
            break


class Reporter(BaseOperator):
    def __init__(self, loggin_task: str, with_timeout: int, *args, **kwargs):
        super().__init__(**kwargs)
        self.loggin_task = loggin_task
        self.with_timeout = with_timeout

    def execute(self, context):
        log_identifier = context['dag_run'].conf.get('log_identifier')
        if log_identifier is None:
            log_identifier = context['dag_run'].run_id

        # this variable is set via environment and cannot be seen in the UI
        connection_uri = Variable.get("REPORT_DB_SERVER")
        db_name = Variable.get("REPORT_DB_NAME")
        report = context["task_instance"].xcom_pull(
            key=f"{context['dag_run'].run_id}*{self.loggin_task}")
        if report:
            with MongoClient(connection_uri) as client:
                db = client[db_name]
                db["reports"].update_one({'dag_run': log_identifier}, {
                    "$set": {
                        self.loggin_task: report,
                        "date": datetime.utcnow(),
                        'dag_run': log_identifier
                    }
                },
                                         upsert=True)

        # some timeout must be set, in order to allow Airflow the parsing of variables-scaled subsequent DAGs
        if self.with_timeout > 0:
            get_timeout = Thread(target=timeout_fn)
            get_timeout.start()
            get_timeout.join(timeout=self.with_timeout)
            breaker.set()

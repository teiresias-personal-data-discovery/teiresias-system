from airflow.models.baseoperator import BaseOperator
import json

from operators.data_retrieval_and_analysis.utils.common import analyze_json


class Analyze_json(BaseOperator):
    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)

    def execute(self, context):
        data = json.loads(context['dag_run'].conf.get('conf', {}).get('data'))
        dataIdentifier = context['dag_run'].conf.get('conf',
                                                     {}).get('dataIdentifier')

        report = analyze_json(data)

        context["task_instance"].xcom_push(
            key=f"{context['dag_run'].run_id}*json_data_analyzer",
            value={dataIdentifier: report})

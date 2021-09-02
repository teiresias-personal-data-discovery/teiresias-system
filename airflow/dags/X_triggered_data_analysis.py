from airflow import DAG
from airflow.utils.dates import days_ago

from operators.reporting.reporter import Reporter
from operators.data_retrieval_and_analysis.analyze_json.analysis import Analyze_json

with DAG("X_triggered_data_analysis",
         start_date=days_ago(1),
         schedule_interval=None) as dag:

    data_analysis = Analyze_json(task_id="data_analysis")

    report_data_analysis = Reporter(task_id="report_data_analysis",
                                    loggin_task="json_data_analyzer",
                                    with_timeout=0)

    data_analysis >> report_data_analysis

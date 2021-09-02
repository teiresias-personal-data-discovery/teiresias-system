from airflow import DAG
from airflow.sensors.filesystem import FileSensor
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from airflow.utils.dates import days_ago

from operators.code_analyzer.code_analyzer_operator import Analyze_local_code
from operators.code_analyzer.process_code_analyis_operator import Process_code_analysis
from operators.reporting.reporter import Reporter

with DAG("A2_manually_code_analysis",
         start_date=days_ago(1),
         schedule_interval=None) as dag:

    sensing_filesystem = FileSensor(task_id='sensing_filesystem',
                                    filepath='',
                                    fs_conn_id='REPOSITORIES_PATH',
                                    poke_interval=10,
                                    mode="reschedule")

    analyze_local_repository = Analyze_local_code(task_id="code_analysis")

    process_code_analysis = Process_code_analysis(
        task_id="processing_storage_traces", repository_names=["file_system"])

    report_code_analysis = Reporter(task_id="report_code_analysis",
                                    loggin_task="manually_code_analyzer",
                                    with_timeout=10)

    trigger_data_analysis = TriggerDagRunOperator(
        task_id="trigger_data_analysis",
        trigger_dag_id="B_storage_data_analysis")

    sensing_filesystem >> analyze_local_repository >> process_code_analysis >> report_code_analysis >> trigger_data_analysis

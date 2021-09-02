from airflow import DAG
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from airflow.utils.dates import days_ago
from airflow.models import Variable
from airflow.utils.trigger_rule import TriggerRule

from operators.code_analyzer.code_analyzer_operator import Clone_and_analyze_code
from operators.code_analyzer.process_code_analyis_operator import Process_code_analysis
from operators.reporting.reporter import Reporter

with DAG("A1_repository_code_analysis",
         start_date=days_ago(1),
         schedule_interval="@monthly") as dag:

    repositories = {}
    try:
        repositories = Variable.get("repositories", deserialize_json=True)
    except:
        pass

    process_code_analysis = Process_code_analysis(
        task_id="processing_storage_traces",
        repository_names=list(repositories.keys()),
        trigger_rule=TriggerRule.ALL_DONE)

    for name, repository in repositories.items():
        analyze_local_repository = Clone_and_analyze_code(
            task_id=f"code_analysis_{name}",
            repository=repository,
            repository_name=name)
        analyze_local_repository >> process_code_analysis

    report_code_analysis = Reporter(task_id="report_code_analysis",
                                    loggin_task="repository_code_analyzer",
                                    with_timeout=20)

    trigger_data_analysis = TriggerDagRunOperator(
        task_id="trigger_data_analysis",
        trigger_dag_id="B_storage_data_analysis",
        conf={"log_identifier": "{{run_id}}"})

    process_code_analysis >> report_code_analysis >> trigger_data_analysis

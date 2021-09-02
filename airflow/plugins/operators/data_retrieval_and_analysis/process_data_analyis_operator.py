from airflow.models.baseoperator import BaseOperator
import time


class Process_data_analysis(BaseOperator):
    def __init__(self, storage_names: list, *args, **kwargs):
        super().__init__(**kwargs)
        self.storage_names = storage_names

    def execute(self, context):
        try:
            report_identifier = f"{context['dag_run'].run_id}*storage_data_analyzer"
            report = {}

            for storage_name in self.storage_names:
                meta_data_analysis = context["task_instance"].xcom_pull(
                    key=
                    f"{context['dag_run'].run_id}*meta_data_analysis*{storage_name}"
                )
                data_analysis = context["task_instance"].xcom_pull(
                    key=
                    f"{context['dag_run'].run_id}*data_analysis*{storage_name}"
                )

                report = {
                    **report,
                    **({
                        storage_name: {
                            **({
                                "meta_data_analysis": meta_data_analysis
                            } if meta_data_analysis else {}),
                            **({
                                "data_analysis": data_analysis
                            } if data_analysis else {})
                        }
                    } if meta_data_analysis or data_analysis else {})
                }
            context["task_instance"].xcom_push(key=report_identifier,
                                               value=report)

        except Exception as e:
            print("Error in Process_data_analysis", e)

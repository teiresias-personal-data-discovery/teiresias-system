from airflow.models.baseoperator import BaseOperator
from airflow.exceptions import AirflowException
from airflow.models import Variable

import json
from datetime import datetime


class Process_code_analysis(BaseOperator):
    def __init__(self, repository_names: list, *args, **kwargs):
        super().__init__(**kwargs)
        self.mandatory_connection_keys = [
            'user', 'password', 'host', 'port', 'db'
        ]
        self.repository_names = repository_names

    def execute(self, context):
        try:
            analyzing_task = "manually_code_analyzer" if self.repository_names[
                0] == "file_system" else "repository_code_analyzer"
            report_identifier = f"{context['dag_run'].run_id}*{analyzing_task}"
            report = {}
            storages = {}
            try:
                # throws if not present
                storages = Variable.get("storages", deserialize_json=True)
            except:
                pass
            for repository_name in self.repository_names:
                code_analysis = context["task_instance"].xcom_pull(
                    key=f"code_analysis_{repository_name}")
                connection_items = code_analysis.get("connection_items")
                analyzed_files = code_analysis.get("yaml_files")
                error = code_analysis.get("error")
                # set date of errored access try to repository object
                if error:
                    repositories = Variable.get("repositories",
                                                deserialize_json=True)
                    repositories = {
                        **repositories, repository_name: {
                            **repositories.get(repository_name, {}), "last_run_errored_at":
                            datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
                        }
                    }
                    Variable.set("repositories", json.dumps(repositories))
                    report = {**report, repository_name: {"error": error}}
                    continue

                # remove date of prior errored access try from repository object
                last_run_errored_at = code_analysis.get("last_run_errored_at")
                if last_run_errored_at:
                    repositories = Variable.get("repositories",
                                                deserialize_json=True)
                    repositories.get(repository_name,
                                     {}).pop('last_run_errored_at', None)
                    Variable.set("repositories", json.dumps(repositories))

                if connection_items is None:
                    report = {
                        **report, repository_name: {
                            "number_of_strorages_found": 0,
                            "complete_storage_trace": 0,
                            "analyzed_files": analyzed_files
                        }
                    }
                    continue

                missing_values = {}
                number_of_total_missing_values = 0
                complete_storage_trace = []

                for storage_identifier, storage_info in connection_items.items(
                ):
                    current_stored_credentials = storages.get(
                        storage_identifier, {})
                    # prioritize user edit, overwrite else
                    if current_stored_credentials.get('user_edited_at'):
                        continue
                    # check for missing values in storage_info
                    new_credentials = {}
                    is_complete = True
                    for variable in self.mandatory_connection_keys:
                        value = storage_info.get('values', {}).get(variable)
                        if value is None:
                            is_complete = False
                            number_of_total_missing_values += 1
                            missing_values = {
                                **missing_values, storage_identifier: {
                                    'values': [
                                        *missing_values.get(
                                            storage_identifier, {}).get(
                                                'values', []), variable
                                    ]
                                }
                            }
                        new_credentials = {**new_credentials, variable: value}
                    new_credentials = {
                        **new_credentials, "source_repository":
                        repository_name,
                        "source_file": storage_info.get('source'),
                        "storage_type": storage_info.get('storage_type')
                    }
                    storages = {
                        **storages, storage_identifier: new_credentials
                    }

                    if is_complete:
                        complete_storage_trace.append(storage_identifier)

                # 2. pass report per repository to XCom
                report = {
                    **report, repository_name: {
                        "number_of_storages_found": len(connection_items),
                        "complete_storage_trace": complete_storage_trace,
                        "number_of_total_missing_values":
                        number_of_total_missing_values,
                        "analyzed_files": analyzed_files,
                        "missing_values": missing_values
                    }
                }
            Variable.set("storages", json.dumps(storages))
            context["task_instance"].xcom_push(key=report_identifier,
                                               value=report)

        except Exception as e:
            print("Error in Process_code_analysis", e)

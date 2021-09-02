from airflow.models.baseoperator import BaseOperator
from airflow.exceptions import AirflowException

from operators.code_analyzer.utils.os_utils import create_directory, remove_directory, clean_directory
from operators.code_analyzer.utils.analysis.main import analyze_code
from operators.code_analyzer.utils.analysis.resolver import resolve_match_multiple
from operators.code_analyzer.utils.source_code_utils import clone_repository, build_repository_path
from airflow.models import Variable

import json
from airflow.models.connection import Connection

CODE_ANALYZER_BASE_PATH = "/opt/airflow/repositories/"


class Analyze_local_code(BaseOperator):
    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)
        self.path = f'{CODE_ANALYZER_BASE_PATH}paste_analyzable_code_here'

    def execute(self, context):
        try:
            connection_items, yaml_files = analyze_code(self.path)
            context["task_instance"].xcom_push(key="code_analysis_file_system",
                                               value={
                                                   "yaml_files":
                                                   yaml_files,
                                                   "connection_items":
                                                   connection_items,
                                               })

        except Exception as e:
            context["task_instance"].xcom_push(key="code_analysis_file_system",
                                               value={"error": repr(e)})
            raise AirflowException("Error in Analyze_code", e)

        finally:
            clean_directory(self.path)


class Clone_and_analyze_code(BaseOperator):
    def __init__(self, repository: str, repository_name: str, *args, **kwargs):
        super().__init__(**kwargs)
        self.repository = repository
        self.repository_name = repository_name

    def execute(self, context):
        path = None
        try:
            path = build_repository_path(self.repository.get("uri"),
                                         CODE_ANALYZER_BASE_PATH)
            if create_directory(path) == -1:
                raise AirflowException(
                    "Error in Clone_and_analyze_code on directory creation")

            error = clone_repository(repository=self.repository.get("uri"),
                                     branch=self.repository.get("branch"),
                                     path=path)
            if error is not None:
                context["task_instance"].xcom_push(
                    key=f"code_analysis_{self.repository_name}",
                    value={"error": repr(error)})
                raise AirflowException(
                    "Error in Clone_and_analyze_code on repository retrieval",
                    error)

            connection_items, yaml_files = analyze_code(path)
            value = {
                "yaml_files": yaml_files,
                "connection_items": connection_items,
            }
            last_run_errored_at = self.repository.get("last_run_was_errored")
            if last_run_errored_at:
                value["last_run_errored_at"] = last_run_errored_at
            context["task_instance"].xcom_push(
                key=f"code_analysis_{self.repository_name}", value=value)
        except Exception as e:
            context["task_instance"].xcom_push(
                key=f"code_analysis_{self.repository_name}",
                value={"error": repr(e)})
            raise AirflowException("Error in Clone_and_analyze_code", e)

        finally:
            if path is not None:
                remove_directory(path)

from airflow.models.baseoperator import BaseOperator
from sqlalchemy import create_engine
import time

from operators.data_retrieval_and_analysis.constants.lookup import personal_data_value_patterns
from operators.data_retrieval_and_analysis.utils.common import get_uri, get_list_from_tuple


class Inplace_postgre_data_analysis(BaseOperator):
    def __init__(self, storage: dict, storage_name: str, *args, **kwargs):
        super().__init__(**kwargs)
        self.storage_name = storage_name
        self.connection_uri = get_uri(storage, "postgre")

    def execute(self, context):
        meta_data = context["task_instance"].xcom_pull(
            key=f"{context['dag_run'].run_id}*meta_data*{self.storage_name}")
        database_error = meta_data.get('error')
        findings = {}
        if database_error:
            findings = {'error': database_error}
            meta_data = {
                key: value
                for key, value in meta_data if key != 'error'
            }

        engine = create_engine(self.connection_uri)
        with engine.connect() as connection:
            for table, table_meta in meta_data.items():
                primary_keys = table_meta.get("primary_keys")
                # we're going to store reference only, thus skipping tables without primary keys
                if not primary_keys:
                    findings = {
                        **findings, table: {
                            'error': 'no primary keys'
                        }
                    }
                    continue

                string_columns = [
                    column for column, column_meta in table_meta.get(
                        'columns').items() if column_meta.get('type') == "TEXT"
                ]
                primary_keys_string = ", ".join(primary_keys)
                for column in string_columns:
                    for pattern_name, pattern in personal_data_value_patterns.items(
                    ):
                        query = f"SELECT {primary_keys_string} FROM {table} WHERE {column} ~ '{pattern}'"
                        matches = []
                        try:
                            match_cursor = connection.execute(query)
                            matches = [
                                get_list_from_tuple(reference_tuple)
                                for reference_tuple in match_cursor
                            ]
                        except Exception as e:
                            findings = {
                                **findings, table: {
                                    **findings.get(table, {}), column: {
                                        'error': repr(e)
                                    }
                                }
                            }

                        findings = {
                            **findings, table: {
                                **findings.get(table, {}),
                                "primary_keys": table_meta.get("primary_keys"),
                                **({column: {
                                    **findings.get(table, {}).get(column, {}),
                                    **({f"{pattern_name}_pattern": {"pk_references": matches}} if matches else {})
                                }} if matches or findings.get(table, {}).get(column) else {})
                            }
                        }

        context["task_instance"].xcom_push(
            key=
            f"{context['dag_run'].run_id}*data_analysis*{self.storage_name}",
            value=findings)

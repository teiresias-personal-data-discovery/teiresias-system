from airflow.models.baseoperator import BaseOperator

from operators.data_retrieval_and_analysis.constants.lookup import personal_data_value_patterns, personal_data_key_words, postgresql_personal_data_types
from operators.data_retrieval_and_analysis.utils.nlp import process_proximity_of_items, process_proximity


class Analyze_postgre_meta(BaseOperator):
    def __init__(self, storage_name: str, *args, **kwargs):
        super().__init__(**kwargs)
        self.storage_name = storage_name

    def execute(self, context):
        meta_data = context["task_instance"].xcom_pull(
            key=f"{context['dag_run'].run_id}*meta_data*{self.storage_name}")
        database_error = meta_data.get('error')
        findings = {"storage_type": "postgre"}
        if database_error:
            findings = {**findings, 'error': database_error}
            meta_data = {
                key: value
                for key, value in meta_data if key != 'error'
            }
        for table, table_meta in meta_data.items():
            str_columns = [
                column
                for column, meta in table_meta.get('columns', {}).items()
                if meta.get('type') == "TEXT"
            ]
            personal_data_typed_columns = {
                column: postgresql_personal_data_types.get(meta.get('type'))
                for column, meta in table_meta.get('columns', {}).items()
                if postgresql_personal_data_types.get(meta.get('type'))
                is not None
            }
            column_comments = {
                column: meta.get('comment')
                for column, meta in table_meta.get('columns', {}).items()
                if meta.get('comment') is not None
            }
            table_comment = table_meta.get('table_comment')
            column_names = list(table_meta.get('columns', {}).keys())
            column_proximities = process_proximity_of_items(
                column_names, personal_data_key_words)
            table_comment_proximities = process_proximity(
                table_comment,
                personal_data_key_words) if table_comment else None
            column_comments_proximities = process_proximity_of_items(
                column_comments,
                personal_data_key_words) if len(column_comments) else None

            table_findings = {
                'number_of_entities':
                table_meta.get('number_of_entities'),
                **({'str_columns':
                str_columns} if str_columns else {}),
                **({
                    'personal_data_typed_columns': personal_data_typed_columns
                } if len(personal_data_typed_columns) else {}),
                **({
                    "column_proximities": column_proximities
                } if len(column_proximities) else {}),
                **({
                    "table_comment_proximities": table_comment_proximities
                } if table_comment and len(table_comment_proximities) else {}),
                **({
                    "column_comments_proximities": column_comments_proximities
                } if len(column_comments) and len(column_comments_proximities) else {})
            }
            findings = {**findings, table: table_findings}

        context["task_instance"].xcom_push(
            key=
            f"{context['dag_run'].run_id}*meta_data_analysis*{self.storage_name}",
            value=findings)

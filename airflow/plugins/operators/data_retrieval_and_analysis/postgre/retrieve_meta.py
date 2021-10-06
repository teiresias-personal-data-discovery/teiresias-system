from airflow.models.baseoperator import BaseOperator
from airflow import AirflowException
from sqlalchemy import create_engine, inspect

from operators.data_retrieval_and_analysis.utils.common import get_uri, get_serializable_sqlalchemy_type


class Retrieve_postgre_meta(BaseOperator):
    def __init__(self, storage: dict, storage_name: str, *args, **kwargs):
        super().__init__(**kwargs)
        self.storage_name = storage_name
        self.connection_uri = get_uri(storage, "postgre")

    def execute(self, context):
        meta_data = {}
        try:
            engine = create_engine(self.connection_uri)
            inspector = inspect(engine)
            tables = inspector.get_table_names()
            with engine.connect() as connection:
                for table in tables:
                    primary_keys = inspector.get_indexes(table)
                    aggregation_columns = '*'
                    if len(primary_keys):
                        try:
                            primary_keys = primary_keys[0].get('column_names')
                            aggregation_columns = ", ".join(primary_keys)
                        except:
                            pass
                    count_cursor = connection.execute(
                        f"SELECT COUNT({aggregation_columns}) as count FROM {table}"
                    )
                    count = {
                        "number_of_entities": row['count']
                        for row in count_cursor
                    }
                    if not count.get("number_of_entities"):
                        count = {"number_of_entities": 0}

                    table_comment = inspector.get_table_comment(table)
                    columns_meta = inspector.get_columns(table)
                    table_meta = {
                        **count,
                        **({
                            'table_comment': table_comment.get("text")
                        } if table_comment.get("text") is not None else {}), "columns":
                        {
                            column.get('name'): {
                                'type':
                                get_serializable_sqlalchemy_type(
                                    column.get('type')),
                                **({
                                    'comment': column.get('comment')
                                } if column.get('comment') else {})
                            }
                            for column in columns_meta
                        }
                    }
                    if len(primary_keys):
                        table_meta['primary_keys'] = primary_keys
                    meta_data = {**meta_data, table: table_meta}

        except Exception as e:
            meta_data = {'error': f"self.storage_name: {repr(e)}"}
            raise AirflowException(meta_data)

        context["task_instance"].xcom_push(
            key=f"{context['dag_run'].run_id}*meta_data*{self.storage_name}",
            value=meta_data)

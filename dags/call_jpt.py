from datetime import datetime, timedelta

from airflow import DAG
from airflow.providers.papermill.operators.papermill import PapermillOperator

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0,
    'retry_delay': timedelta(minutes=1)
}

with DAG(
    dag_id='example_papermill_operator',
    default_args=default_args,
    schedule_interval='0 0 * * *',
    start_date=datetime(2021, 1, 1),
    template_searchpath='/usr/local/airflow/include',
    catchup=False
) as dag_1:

    notebook_task = PapermillOperator(
        task_id="run_example_notebook",
        input_nb="include/example_notebook.ipynb",
        output_nb="include/out-{{ execution_date }}.ipynb",
        parameters={"execution_date": "{{ execution_date }}"},
    )
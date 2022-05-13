from datetime import timedelta
from airflow.models import DAG
from airflow.operators.papermill_operator import PapermillOperator
from airflow.utils.dates import days_ago

default_args = {
    'owner': 'abc',
    'start_date': days_ago(2)
}

dag=DAG(
    dag_id='example_ppm_dag',
    default_args=default_args,
    schedule_interval='0 0 * * *',
    dagrun_timeout=timedelta(minutes=60))

run_this = PapermillOperator(
        task_id="run_example_notebook",
        dag=dag,
        input_nb="/tmp/tranfer_minio.ipynb",
        output_nb="/tmp/out-{{ execution_date }}.ipynb",
        parameters={"msgs": "Ran from Airflow at {{ execution_date }}!"}
)
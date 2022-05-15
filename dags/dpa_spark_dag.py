from airflow.models import DAG
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from airflow.utils.dates import days_ago
from airflow.operators.bash_operator import BashOperator

import os
import sys

args = {
    'owner': 'Airflow',
}

with DAG(
    dag_id='dpa_cassandra_etl',
    default_args=args,
    schedule_interval=None,
    start_date=days_ago(2),
    tags=['hung'],
) as dag:
    # [START howto_operator_spark_submit]
    os.environ['SPARK_HOME'] = '/dags_airflowdag/dags/spark-3.0.1-bin-hadoop2.7'
    sys.path.append(os.path.join(os.environ['SPARK_HOME'], 'bin'))

    load_and_write = BashOperator(
        task_id="load_and_write_job",
        bash_command='spark-submit \
            --packages com.datastax.spark:spark-cassandra-connector_2.12:3.0.1 \
            --properties-file /dags_airflowdag/dags/00_script/conf/properties.conf \
            /dags_airflowdag/dags/00_script/py/extract_and_load.py'
    )

    etl_job = BashOperator(
        task_id="etl_job",
        bash_command='spark-submit \
            --packages com.datastax.spark:spark-cassandra-connector_2.12:3.0.1 \
            --properties-file /dags_airflowdag/dags/00_script/conf/properties.conf \
            /dags_airflowdag/dags/00_script/py/etl.py'
    )

    load_and_write >> etl_job
    # [END howto_operator_spark_submit]

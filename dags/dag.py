import sys
import os
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.email import send_email
from datetime import datetime, timedelta
from pyspark.sql import SparkSession

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__) + "/../scripts"))

from bronze import ler_dados_api
from prata import transformar_dados_prata
from ouro import transformar_dados_ouro

spark = SparkSession.builder.appName("teste_ABInbev").getOrCreate()

args = {
    'owner': 'murilo rossi',
    'retries': 3,
    'retry_delay': timedelta(minutes=1),
    'email_on_failure': True,
    'email_on_retry': False,
    'email': ['murilorossi@live.com'],
    'start_date': datetime(2024, 9, 17),
}

def email(context):
    assunto = f"Airflow Falhou - DAG {context['dag'].dag_id} - Task {context['task'].task_id}"
    html = f"""
        <h2>Airflow: Falha na execução da DAG</h2>
        <ul>
            <li><strong>DAG:</strong> {context['dag'].dag_id}</li>
            <li><strong>Task:</strong> {context['task'].task_id}</li>
            <li><strong>Data de Execução:</strong> {context['ts']}</li>
            <li><strong>Tentativa:</strong> {context['ti'].try_number}</li>
        </ul>
        """
    send_email(to='murilorossi@live.com', subject=assunto, html_content=html)


with DAG('cervejarias', default_args=args, schedule_interval='@daily', catchup=False) as dag:
    bronze = PythonOperator(
        task_id='bronze',
        python_callable=ler_dados_api,
        on_failure_callback = email
    )

    prata = PythonOperator(
        task_id='prata',
        python_callable=transformar_dados_prata,
        op_args=[spark],
        on_failure_callback = email
    )


    ouro = PythonOperator(
        task_id='ouro',
        python_callable=transformar_dados_ouro,
        op_args=[spark],
        on_failure_callback = email
    )


    bronze >> prata >> ouro



from airflow.models import DAG

from airflow.operators.python import PythonOperator
from elasticsearch_plugin.hooks.elastic_hooks import ElasticHook


from airflow.utils.task_group import TaskGroup
from datetime import datetime


default_args={
    'start_date':datetime(2022,3,30),

}

def _print_es_info():
    hook = ElasticHook()
    print(hook.info())

with DAG('elasticsearch_dag',schedule_interval='@daily',
        default_args=default_args,catchup=False) as dag:

            print_es_info=PythonOperator(
            task_id='print_es_info',
            python_callable=_print_es_info
        )

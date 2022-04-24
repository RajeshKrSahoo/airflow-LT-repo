#

from airflow.models import DAG

from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator

from airflow.utils.task_group import TaskGroup
from datetime import datetime


default_args={
    'start_date':datetime(2022,3,30),

}



with DAG('parallel_dag',schedule_interval='@daily',
        default_args=default_args,catchup=False) as dag:

            task1=BashOperator(
                task_id='task_1',
                bash_command='sleep 3'
            )

            # task2=BashOperator(
            #         task_id='task_2',
            #         bash_command='sleep 3'
            # )
                    
            # task3=BashOperator(
            #     task_id='task_3',
            #     bash_command='sleep 3'
            # )
            with TaskGroup('processing_tasks') as processing_task:
                task2=BashOperator(
                    task_id='task_2',
                    bash_command='sleep 3'
                )
                    
                task3=BashOperator(
                    task_id='task_3',
                    bash_command='sleep 3'
                )


            # processing=SubDagOperator(
            #     task_id='processing_tasks',
            #     subdag=subdag_parallel_dag('parallel_dag', 'processing_tasks',default_args)
            # )
            

            task4=BashOperator(
                task_id='task_4',
                bash_command='sleep 3'
            )


            ## DAG Runs paralally 
            # task1 >> task2 >> task4
            # task1 >> task3 >> task4 

            ## DAG runs in parallel in subgroup
            task1 >> processing_task >> task4
###

from airflow.models import DAG
from airflow.providers.sqlite.operators.sqlite import SqliteOperator
from airflow.providers.http.sensors.http import HttpSensor
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime
import pandas as pd
import json
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

default_args={
    'start_date':datetime(2022,3,30),

}

def _processing_user(ti):
    users=ti.xcom_pull(task_ids=['extracting_user'])
    print(users[0])

    if not len(users) or 'states' not in users[0].keys():
        raise ValueError("Data is empty!!")

    user=users[0]
    process_data=pd.DataFrame(user['states'])
    process_data.to_csv('/tmp/processed_user.csv',index=None,header=False)





with DAG('user_processing',schedule_interval='@daily',
        default_args=default_args,catchup=False) as dag:

            ##First task
            creating_table=SqliteOperator(
                task_id='creating_table',
                sqlite_conn_id='db_sqlite',
                sql='''
                    create table IF NOT EXISTS statedata(
                      
                        state_id text integer not null,
                        state_name text not null
                        
                    );
                '''
            )

            ##Sensor operator to check if the api is available or not
            is_api_available=HttpSensor(
                task_id='is_api_available',
                http_conn_id='user_api',
                endpoint='api/v2/admin/location/states/'
            )

            extracting_user=SimpleHttpOperator(
                task_id='extracting_user',
                http_conn_id='user_api',
                endpoint='api/v2/admin/location/states/',
                method='GET',
                response_filter=lambda response: json.loads(response.text),
                log_response=True
            )


            processing_user=PythonOperator(
                task_id='processing_user',
                python_callable=_processing_user
            )

            storing_user=BashOperator(
                task_id='storing_user',
                bash_command='echo -e ".separator ","\n.import /tmp/processed_user.csv statedata" | sqlite3 /home/airflow/airflow/airflow.db'
            )

            ##dependnacies in order
            creating_table >> is_api_available >> extracting_user >> processing_user >> storing_user







            


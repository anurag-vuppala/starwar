from airflow import DAG
from airflow.operators.python import PythonOperator 
import pendulum
from datetime import datetime, timedelta

args={
    # 'depends_on_past': False,
    'email': ['anuragvuppala@gmail.com'],
    # 'email_on_failure': False,
    # 'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(seconds=5),
}

with DAG (
    dag_id="starwarapi",
    default_args= args,
    schedule_interval=timedelta(seconds=10),
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    catchup=False,
    tags=["API"],
) as dag:

    def starwar_api(*args):
        import requests

        end_point = "https://swapi.dev/api/starships"
        api_req = requests.get(end_point)
        print(api_req)
        if api_req.status_code == 200:
            api_j = api_req.json()
            print(api_j)
            return api_j
        else:
            print(f'Reuest Failed! -- Http error code {api_req.status_code}')
    

    # def save_data_to_csv(data):

    # print(starwar_api())
    run_this = PythonOperator(task_id = "starwarapi",
                                python_callable=starwar_api,
                                dag = dag,
                                )
    run_this
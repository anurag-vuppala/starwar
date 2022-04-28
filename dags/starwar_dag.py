from dataclasses import dataclass
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta



args={
    # 'email': ['anuragvuppala@gmail.com'],
    'retries': 1,
    'retry_delay': timedelta(seconds=10),
}

with DAG(
    dag_id="starwarapi",
    default_args=args,
    schedule_interval=timedelta(seconds=60),
    start_date=datetime(2021, 1, 1),
    catchup=False,
    tags=["API"],
) as dag:
    
    
    # [start_Extracting_data_from_api]#
    def starwar_api(*args):
        import requests
        import json
        
        
        end_point = "https://swapi.dev/api/starships"
        api_req = requests.get(end_point)
        print(api_req)
        if api_req.status_code == 200:
            api_j = api_req.json()
            # print(api_j)
            
            # Save json response to .json file to simplify code instead of using TaskFlow API #
            with open('request.json', 'w') as json_file:
                json.dump(api_j, json_file)
            
        else:
            print(f'Request Failed! -- Http error code {api_req.status_code}')
    # [END_Extract_data_from_api]#   


    # [Start_transforming_data]#
    def store_data(*args):
        import pandas
        import json
        
        
        f = open('request.json')
        data = json.load(f)
        name = []
        model = []
        speed = []
        cost = []
        pass_cap = []
        
        
        # filtering responce data #
        
        for s in data["results"]:
            name.append(s["name"])
            model.append(s["model"])
            speed.append(s["max_atmosphering_speed"])
            cost.append(s["cost_in_credits"])
            pass_cap.append(s["passengers"])
        # json to distionary  #
        ship_dic = {
            "Spaceship_Name" : name,
            "Spaceship_Model" : model,
            "Max_Speed" :speed, 
            "Spaceship_Cost" : cost,
            "Passenger_Capacity":pass_cap,
        }
        # Distionary to pandas dataframe ##
        ship_df = pandas.DataFrame(ship_dic, columns= ["Spaceship_Name",
                                                    "Spaceship_Model",
                                                    "Max_Speed",
                                                    "Spaceship_Cost",
                                                    "Passenger_Capacity",])
        
        # Creating .CSV file from pandas dataframe ##
        ship_df.to_csv("/opt/airflow/output/Output_data.csv")
        
        
    extract = PythonOperator(task_id = "extract",
                                python_callable=starwar_api)
        
    transform_load = PythonOperator(task_id = "transform_load",
                                        python_callable =store_data) 
        
    extracted = BashOperator(task_id = "extracted",
                                bash_command = "echo 'Data_Extracted'")
        
    loaded = BashOperator(task_id = "loaded",
                            bash_command = "echo 'Data_loaded_to_CSV'"
    )
    
    
    extract >> extracted >> transform_load >> loaded


from email import header
from operator import index
import pandas
import json

def starwar_api(*args):
    import requests

    end_point = "https://swapi.dev/api/starships"
    api_req = requests.get(end_point)
    print(api_req)
    if api_req.status_code == 200:
        api_j = api_req.json()
        # print(api_j)
        with open('request.json', 'w') as json_file:
                json.dump(api_j, json_file)
        return api_j
    else:
        print(f'Reuest Failed! -- Http error code {api_req.status_code}')
        
starwar_api()

def store_data(*args):
    f = open('request.json')
    data = json.load(f)
    name = []
    model = []
    speed = []
    cost = []
    pass_cap = []
    
    for s in data["results"]:
        name.append(s["name"])
        model.append(s["model"])
        speed.append(s["max_atmosphering_speed"])
        cost.append(s["cost_in_credits"])
        pass_cap.append(s["passengers"])
    
    ship_dic = {
        "Spaceship_Name" : name,
        "Spaceship_Model" : model,
        "Max_Speed" :speed, 
        "Spaceship_Cost" : cost,
        "Passenger_Capacity":pass_cap,
    }
    
    ship_df = pandas.DataFrame(ship_dic, columns= ["Spaceship_Name",
                                                   "Spaceship_Model",
                                                   "Max_Speed",
                                                   "Spaceship_Cost",
                                                   "Passenger_Capacity",])
    
    ship_df.to_csv("Output_data.csv")
    return ship_df
store_data()


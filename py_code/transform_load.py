import pandas
import json
    
    
def main():      
                
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
                                                    "Passenger_Capacity",]
                                                    )
    
    # Creating .CSV file from pandas dataframe ##
    ship_df.to_csv("/opt/airflow/output/Output_data.csv")
    
    
if __name__ == "__main__":
    main()
    
import requests
import json
    
    
def main():
    
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
#[END_Extract_data_from_api]#
    
    
if __name__ == "__main__":
    main()
    
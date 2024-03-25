# The code snippet above is used to call the API. The data is read from a CSV file, converted to a dictionary, and then to JSON format.
# The data is then sent to the API using a POST request. The response from the API is printed.


import requests
import json
import pandas as pd 

def call_api():
    url = 'http://:5000/predict'

    data = pd.read_csv("data/future_unseen_data.csv")

    data = data.to_dict(orient='records')

    data = json.dumps(data)

    headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}

    r = requests.post(url, data=data, headers=headers)

    print(r.json())

if __name__ == '__main__':
    call_api

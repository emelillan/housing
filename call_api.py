# This code snippet is used to call the API. The data is read from a CSV file, converted to a dictionary, and then to JSON format.
# The data is then sent to the API using a POST request. The response from the API is printed.


import requests
import json
import pandas as pd


def call_api_batch():
    """
    Call the API to predict the output based on the input data. Batch prediction is printed.
    """
    url = 'http://0.0.0.0:5055/predict'
    data = pd.read_csv("data/future_unseen_examples.csv")
    data = data.to_dict()
    data = json.dumps(data)
    headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
    r = requests.post(url, data=data, headers=headers)
    print(r)
    print(r.json())
    return


def call_api_single():
    """
    Call the API to predict the output based on the input data. Single prediction is printed.
    """
    url = 'http://0.0.0.0:5055/predict'
    data = pd.read_csv("data/future_unseen_examples.csv")
    data = data.sample(1).to_dict()
    data = json.dumps(data)
    headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
    r = requests.post(url, data=data, headers=headers)
    print(r)
    print(r.json())
    return


def call_api_search(zipcode):
    """
    Call the API to predict the output based on the input data. Single prediction is printed.
    """
    url = 'http://0.0.0.0:5055/search'
    data = {"zipcode": zipcode}
    data = json.dumps(data)
    headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
    r = requests.post(url, data=data, headers=headers)
    print(r)
    print(r.json())
    return


if __name__ == '__main__':
    # code to use argparser to choose between batch and single prediction
    import argparse
    parser = argparse.ArgumentParser(
        description='Choose between batch and single prediction.')
    parser.add_argument('-c', '--choice', type=str,
                        help='Choose between batch and single prediction.',
                        required=False, choices=['batch', 'single'])

    parser.add_argument('-z', '--zipcode', type=str,
                        help='Enter the zip code for search.',
                        required=False)
    args = parser.parse_args()
    if args.choice == "batch":
        call_api_batch()
    elif args.choice == "single":
        call_api_single()
    elif args.zipcode:
        zipcode = args.zipcode
        call_api_search(zipcode)
    else:
        print("Invalid choice. Please choose between batch and single prediction.")
        exit(1)

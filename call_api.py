import requests
import json
import pandas as pd
import argparse


def create_api_client(base_url):
    """Creates an API client with base URL."""
    return lambda endpoint, data=None, method="POST": _request_api(base_url, endpoint, data, method)


def _request_api(base_url, endpoint, data, method):
    """Performs an API request and returns response and JSON data."""
    url = f"{base_url}/{endpoint}"
    headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
    response = requests.request(
        method, url, data=json.dumps(data), headers=headers)
    return response, response.json()


def load_data_from_csv(file_path):
    """Loads data from a CSV file and converts it to a dictionary."""
    return pd.read_csv(file_path)


def predict_batch(api_client, data):
    """Predicts using batch data."""
    response, response_json = api_client("/predict", data.to_dict())
    return f"Batch prediction response: {response.status_code}", response_json


def predict_single(api_client, data):
    """Predicts using a single data sample."""
    return predict_batch(api_client, data.sample(1))  # Reuse batch logic


def get_features(api_client):
    """Gets the features used in the model."""
    response, response_json = api_client("/features", method="GET")
    return f"Features used in the model: {response.status_code}", response_json


def search(api_client, zipcode):
    """Searches based on zipcode."""
    response, response_json = api_client("/search", {"zipcode": zipcode})
    return f"Search response: {response.status_code}", response_json


def choose_action(api_client, choice, data, args):
    """Selects and executes the action based on user input."""
    actions = {
        "batch": lambda: predict_batch(api_client, load_data_from_csv("data/future_unseen_examples.csv")),
        "single": lambda: predict_single(api_client, load_data_from_csv("data/future_unseen_examples.csv")),
        "search": lambda: search(api_client, args.zipcode),
        "features": lambda: get_features(api_client),
    }
    return actions.get(choice, lambda: print("Invalid choice."))()


def main():
    """Parses arguments and runs the chosen action."""
    parser = argparse.ArgumentParser(
        description="Choose between batch, single prediction, or search.")
    parser.add_argument(
        '-c',
        '--choice',
        type=str,
        required=True,
        choices=['batch', 'single', 'search', "features"],
        help="Choose between batch, single prediction, or search."
    )
    parser.add_argument(
        '-z',
        '--zipcode',
        type=str,
        help="Enter the zip code for search (required for search action)."
    )
    parser.add_argument(
        '-i',
        '--ip',
        type=str,
        default="http://0.0.0.0:5055",
        help="Enter the IP address for the API (defaults to dev server)."
    )
    args = parser.parse_args()

    ips = {
        'dev': "http://0.0.0.0:5055",
        'prod': "http://127.0.0.1:80"
    }

    api_client = create_api_client(ips[args.ip])
    data = load_data_from_csv("data/future_unseen_examples.csv")
    results = choose_action(api_client, args.choice, data, args)
    print(results)


if __name__ == "__main__":
    main()

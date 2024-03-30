# Description: This file is the main file for the model API. It loads the model and the model features and predicts the output based on the input data.
# It also checks if the input data is in the correct format before predicting the output.


from flask import Flask, request, jsonify

import joblib
import json
import socket
import pandas as pd
import redis

app = Flask(__name__)
r = redis.Redis(host='redis', port=6379)


def check_data(data) -> bool:
    """
    Check if the input data has the correct format for prediction.
    """
    model_features = json.load(open("model/model_features.json", "r"))
    for feature in model_features:
        if feature not in data.columns:
            return False
    return True


def fetchDetails() -> str:
    """
    Fetch the hostname and IP address of the server.
    """
    hostname = socket.gethostname()
    host_ip = socket.gethostbyname(hostname)
    return str(hostname), str(host_ip)


def data_prep(data) -> pd.DataFrame:
    """
    Prepare the data for prediction, including converting the data types and merging with the demographics data. 
    """
    dtypes_loaded = json.load(open("model/model_dtypes.json", "r"))
    for key, value in dtypes_loaded.items():
        data[key] = data[key].astype(value)
    demographics = pd.read_csv("data/zipcode_demographics.csv",
                               dtype={'zipcode': str})
    demographics['zipcode'] = demographics['zipcode'].astype(str)
    data['zipcode'] = data['zipcode'].astype(str)

    merged_data = data.merge(demographics, how="left",
                             on="zipcode")
    return merged_data


@app.route("/")
def details():
    hostname, ip = fetchDetails()
    return jsonify({"Hostname": hostname, "IP": ip})


@app.route('/features', methods=['GET'])
def features():
    model_features = json.load(open("model/model_features.json", "r"))
    return jsonify({"features": model_features})


@app.route('/search', methods=['POST'])
def search():
    data = request.get_json()
    prediction = r.get(data.get("zipcode"))

    if prediction:
        return jsonify({"prediction": prediction.decode('utf-8')})
    else:
        return jsonify({f"zipcode - {data.get('zipcode')}": "Not Found"})


@app.route('/predict', methods=['POST'])
def predict():
    # get the data from the post request
    data = pd.DataFrame(request.get_json())
    data = data_prep(data)

    # check data
    if not check_data(data):
        return jsonify({'error': 'Input Error'})

    model = joblib.load("model/model.pkl")
    model_features = json.load(open("model/model_features.json", "r"))
    data['predictions'] = model.predict(data[model_features])

    for i in range(len(data)):
        r.set(data['zipcode'][i], data['predictions'][i])
        print("Data to DB", data['zipcode'][i],
              data['predictions'][i], flush=True)

    worker_detail = fetchDetails()

    return jsonify({"zipcode": data['zipcode'].tolist(),
                    'prediction': data['predictions'].tolist(),
                    "worker": worker_detail[0],
                    "IP": worker_detail[1],
                    })


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5050)

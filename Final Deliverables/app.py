from flask import Flask, request,render_template
import joblib

import requests

# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "QPrWDn2BZ7ubYvtx8nmiJ5LzmROuv-wxHLOl-WatJZmG"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
 API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}


app = Flask(__name__)
model = joblib.load("model.save")

app = Flask(__name__)

@app.route('/')
def predict():
    return render_template("manual_predict.html")

@app.route('/y_predict',methods=['POST'])
def y_predict():

    x_test = [[float(x) for x in request.form.values()]]

    payload_scoring = {"input_data": [{"field": [['distance', 'speed', 'temp_inside', 'temp_outside', 'AC', 'rain', 'sun','E10', 'SP98']], "values": x_test }]}

    response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/64d6e5d1-66b4-4d52-9ac1-12c3731fcf11/predictions?version=2022-11-11', json=payload_scoring,headers={'Authorization': 'Bearer ' + mltoken})

    pred = response_scoring.json()

    return render_template('manual_predict.html', prediction_text=('fuel Comsumption(L/100km): ',pred['predictions'][0]['values'][0]))


if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True)
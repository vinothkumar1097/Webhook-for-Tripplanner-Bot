import json
import os
import requests

from flask import Flask, request, make_response

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    #Extracting the JSON data from dialogflow's POST request
    req = request.get_json(silent=True, force=True)
    print(json.dumps(req, indent=4))

    #Extracting the parameters from JSON request using user-defined function
    res = makeResponse(req)
    print(json.dumps(res, indent=4))

    #Setting the response for dialogflow
    r = make_response(res)
    r.headers['content-type'] = 'application/json'
    return r

def makeResponse(req):
    result = req.get('queryResult')
    print(result)
    parameters = result.get('parameters')
    print(parameters)
    city = parameters.get('geo-city')
    date = parameters.get('date')

    #querying openweathermap using api
    r = requests.get("https://samples.openweathermap.org/data/2.5/forecast?q="+city+"&appid=cc5042349f192ce820076b39c16676e5")
    json_object = r.json()
    weather = json_object['list']
    for i in len(weather):
        if date in weather[i]['dt_txt']:
            condition = weather[i]['weather'][0]['description']

    speech = "The forecast for "+city+" for "+date+" is "+condition
    return {
        "speech":speech,
        "displayText":speech,
        "source":"dialogflow-weather-webhook"
    }

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print('App is starting on port %d' %port)
    app.run(debug=False, port=port, host='0.0.0.0')

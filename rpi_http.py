from flask import Flask
from flask import jsonify
from flask import request
import time
import sys
import time
import grovepi
import requests
from grovepi import *
# By appending the folder of all the GrovePi libraries to the system path here,
# we are successfully `import grovepi`
sys.path.append('../../Software/Python/')

led = 4
LED_STATUS = "OFF"
WEATHER_API_KEY = "c246a82046604c3997b43435232711"


import argparse
import json

app = Flask('RaspberryPi Server')

"""
The @app.route() above the function is called a decorator. We will skip
explaining decorators in detail for brevity. The functions below, such as
get_mailbox_callback(), are callbacks that get called when certain types
of HTTP request are received by the Flask server. With the decorator's
input arguments below and the Flask server initialization in
if __name__ == '__main__':, this first callback is set to be specifically
called when a GET request is sent to the URL "http://0.0.0.0:[port]/mailbox"
"""

@app.route('/LED', methods=['GET'])
def get_mailbox_callback():
    """
    Summary: A callback which for when GET is called on [host]:[port]/mailbox

    Returns:
        string: A JSON-formatted string containing the response message
    """

    # Since we have `from flask import request` above, the 'request' object
    # will (magically) be available when the callback is called. `request` is
    # the object that stores all the HTTP message data (header, payload, etc.).
    # We will skip explaining how this object gets here because the answer is
    # a bit long and out of the scope of this lab.
    global LED_STATUS
    response = jsonify({'Response': LED_STATUS})
    print(response)

    # The object returned will be sent back as an HTTP message to the requester
    return response



@app.route('/mailbox/delete', methods=['DELETE'])
def delete_mail_callback():
    """
    Summary: A callback for when DELETE is called on [host]:[port]/mailbox/delete

    Returns:
        string: A JSON-formatted string containing the response message
    """

    # Get the payload containing the list of mail ids to delete
    payload = request.get_json()
    print(payload)

    return response

@app.route('/send-mail', methods=['POST'])
def post_mail_callback():
    """
    Summary: A callback for when POST is called on [host]:[port]/mailbox/send-mail

    Returns:
        string: A JSON-formatted string containing the response message
    """

    # Get the payload containing the sender, subject and body parameters
    payload = request.get_json()
    print(payload)

    response = {'Response': 'Mail sent'}

    # The object returned will be sent back as an HTTP message to the requester
    return json.dumps(response)

@app.route('/LED', methods=['PUT'])
def put_callback():
    payload = request.get_json()
    print(payload)
    global LED_STATUS
    if payload['LED'] == 'ON':
        grovepi.digitalWrite(led,1)

        LED_STATUS = "ON"
        response = {'Response': 'LED_ON'}
    elif payload['LED'] == 'OFF':
        grovepi.digitalWrite(led,0)
        LED_STATUS = "OFF"
        response = {'Response': 'LED_OFF'}
    # The object returned will be sent back as an HTTP message to the requester
    return json.dumps(response)

@app.route('/weather', methods=['GET'])
def get_weather_callback():
    params = {
        'key': WEATHER_API_KEY,
        'q': "Los Angeles",
        'aqi': 'no'
    }

    response = requests.get('http://api.openweathermap.org/data/2.5/weather', params)

    if response.status_code == 200: # Status: OK
        data = response.json()
        return jsonify({'temperature':data['current']['temp_f'], 
                        'condition':data['current']['condition']['text']})

    else:
        print('error: got response code %d' % response.status_code)
        print(response.text)
        return jsonify({0.0:0.0, 0.0:0.0})

if __name__ == '__main__':

    grovepi.digitalWrite(led,0)
    app.run(debug=False, host='0.0.0.0', port=5000)


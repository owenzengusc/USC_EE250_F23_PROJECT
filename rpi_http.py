from flask import Flask
from flask import jsonify
from flask import request
import time
import sys
import time
import grovepi
import requests
import threading
from grovepi import *
# set I2C to use the hardware bus
grovepi.set_bus("RPI_1")

ultrasonic_ranger = 2


led = 4
ultrasonic_read = 0
threshold = 10
warn_flag = False
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


@app.route('/ultrasonic', methods=['GET'])
def get_ultrasonic_callback():
    global ultrasonic_read
    if warn_flag == True: 
        response = jsonify({'US Reading': ultrasonic_read, 'Warning': 'True'})
    else:
        response = jsonify({'US Reading': ultrasonic_read, 'Warning': 'False'})
    print(response)

    # The object returned will be sent back as an HTTP message to the requester
    return response


@app.route('/LED', methods=['PUT'])
def put_callback():
    payload = request.get_json()
    print(payload)
    global LED_STATUS
    if payload['LED'] == 'ON':
        grovepi.digitalWrite(led,1)

        LED_STATUS = "ON"
        response = {'Response': 'ON'}
    elif payload['LED'] == 'OFF':
        grovepi.digitalWrite(led,0)
        LED_STATUS = "OFF"
        response = {'Response': 'OFF'}
    # The object returned will be sent back as an HTTP message to the requester
    return json.dumps(response)

@app.route('/weather', methods=['GET'])
def get_weather_callback():
    params = {
        'key': WEATHER_API_KEY,
        'q': "Los Angeles",
        'aqi': 'no'
    }

    response = requests.get('https://api.weatherapi.com/v1/current.json', params)

    if response.status_code == 200: # Status: OK
        data = response.json()
        return jsonify({'temperature':data['current']['temp_f'], 
                        'condition':data['current']['condition']['text']})
    else:
        print('error: got response code %d' % response.status_code)
        print(response.text)
        return jsonify({0:0, 0:0})
def read_ultrasonic():
    global ultrasonic_read, warn_flag
    while True:
        try:
            ultrasonic_read = grovepi.ultrasonicRead(ultrasonic_ranger)
            print(ultrasonic_read)
            if ultrasonic_read < threshold:
                warn_flag = True
            else:
                warn_flag = False
        except Exception as e:
            print("Error in ultrasonic read: {}".format(e))
        time.sleep(5)  


if __name__ == '__main__':
    # Initialize ultrasonic reading thread
    ultrasonic_thread = threading.Thread(target=read_ultrasonic)
    ultrasonic_thread.daemon = True  # This ensures the thread exits when the main program does
    ultrasonic_thread.start()

    # Start Flask server
    app.run(debug=False, host='0.0.0.0', port=5000)


from flask import Flask
from flask import jsonify
from flask import request
import time
import sys
import time
import grovepi
from grovepi import *
# By appending the folder of all the GrovePi libraries to the system path here,
# we are successfully `import grovepi`
sys.path.append('../../Software/Python/')

led = 4
LED_STATUS = "OFF"


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

# TODO: Use Flash's route() decorator to add support to your HTTP server for
# handling GET requests made to the URL '/mailbox/search'
#
# Use get_mailbox_callback() as an example. You'll need to use mailboxManager
# for this request as well, so make sure to spend some time understanding how
# it works and the features it provides.
#
# Your implementation should handle reasonable error cases as well, such as an
# incorrect password.

#def search_mailbox_callback():


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

if __name__ == '__main__':

    grovepi.digitalWrite(led,0)
    app.run(debug=False, host='0.0.0.0', port=5000)


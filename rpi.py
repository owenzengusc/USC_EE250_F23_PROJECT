#Owen Zeng & Felix Chen

import paho.mqtt.client as mqtt
import time
import sys
import time
import grovepi
from grovepi import *
# Import functions in grove_rgb_lcd.py (setText etc.)
import grove_rgb_lcd
# By appending the folder of all the GrovePi libraries to the system path here,
# we are successfully `import grovepi`
sys.path.append('../../Software/Python/')
# This append is to support importing the LCD library.
sys.path.append('../../Software/Python/grove_rgb_lcd')

led = 4


def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))

    #subscribe to topics of interest here
    client.subscribe("owenzeng/led")
    client.subscribe("owenzeng/weather")

#Default message callback. Please use custom callbacks.
def on_message(client, userdata, msg):
    print("on_message: " + msg.topic + " " + str(msg.payload, "utf-8"))
    
    #if the topic is owenzeng/led, turn on or off the led
    if msg.topic == "owenzeng/led":
        if str(msg.payload, "utf-8") == "LED_ON":
            print("LED_ON")
            digitalWrite(led,1)
        elif str(msg.payload, "utf-8") == "LED_OFF":
            print("LED_OFF")
            digitalWrite(led,0)
    elif msg.topic == "owenzeng/lcd":
        #print("lcd", str(msg.payload, "utf-8"))
        #write_lcd(str(msg.payload, "utf-8")," ")
        grove_rgb_lcd.setText(str(msg.payload, "utf-8"))
        
        

if __name__ == '__main__':
    #this section is covered in publisher_and_subscriber_example.py
    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = on_connect
    client.connect(host="test.mosquitto.org", port=1883, keepalive=60)
    client.loop_start()
            

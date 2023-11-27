import speech_recognition as sr
import pyttsx3
import paho.mqtt.client as mqtt


def on_connect(client, userdata, flags, rc):
    print("Connected to server with result code "+str(rc))
    client.subscribe("owenzeng/led")
    client.subscribe("owenzeng/weather")

    #subscribe to topics of interest here

#Default message callback. Please use custom callbacks.
def on_message(client, userdata, msg):
    print("on_message: " + msg.topic + " " + str(msg.payload, "utf-8"))

if __name__ == '__main__':
    recognizer = sr.Recognizer()
    engine = pyttsx3.init()

    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = on_connect
    client.connect(host="test.mosquitto.org", port=1883, keepalive=60)
    client.loop_start()

    while True:
        with sr.Microphone() as source:
            print("Say something!")
            audio = recognizer.listen(source)

        try:
            print("Google Speech Recognition thinks you said:")
            print(recognizer.recognize_google(audio))
            engine.say("Google Speech Recognition thinks you said:")
            words = recognizer.recognize_google(audio)
            engine.say(words)
            if "hey" in words.lower():
                engine.say("hello there")
            elif "weather" in words.lower():
                engine.say("The weather is nice")
            elif "led" in words.lower():
                if "on" in words.lower():
                    client.publish("owenzeng/led", "LED_ON")
                    engine.say("LED_ON")
                elif "off" in words.lower():
                    client.publish("owenzeng/led", "LED_OFF")
                    engine.say("LED_OFF")
            engine.runAndWait()
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
            engine.say("Google Speech Recognition could not understand audio")
            engine.runAndWait()
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
            engine.say("Could not request results from Google Speech Recognition service")
            engine.runAndWait()
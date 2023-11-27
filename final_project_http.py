import speech_recognition as sr
import pyttsx3
import requests
import json

ip_address = "172.20.10.12:5000"

if __name__ == '__main__':
    recognizer = sr.Recognizer()
    engine = pyttsx3.init()

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
                response_json = requests.get("http://{}/weather".format(ip_address))
                response_dict = json.loads(response_json.text)
                print("condition: {}".format(response_dict['condition']))
                print("temperature: {}".format(response_dict['temperature']))
                engine.say("condition: {}".format(response_dict['condition'])+"temperature: {}".format(response_dict['temperature']))
            elif "led" in words.lower():
                if "on" in words.lower():
                    response = requests.put("http://{}/LED".format(ip_address), json={"LED": "ON"})
                    if response.status_code == 200:
                        engine.say("LED_ON")
                        engine.say(response.text)
                    else:
                        engine.say("error")
                elif "off" in words.lower():
                    response = requests.put("http://{}/LED".format(ip_address), json={"LED": "OFF"})
                    engine.say("LED_OFF")
                elif "status" in words.lower():
                    response = requests.get("http://{}/LED".format(ip_address))
                    print(response.text)
                    engine.say(response.text)
            engine.runAndWait()
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
            engine.say("Google Speech Recognition could not understand audio")
            engine.runAndWait()
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
            engine.say("Could not request results from Google Speech Recognition service")
            engine.runAndWait()
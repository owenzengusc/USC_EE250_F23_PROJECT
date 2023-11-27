import speech_recognition as sr
import pyttsx3

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
        engine.say(recognizer.recognize_google(audio))
        engine.runAndWait()
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
        engine.say("Google Speech Recognition could not understand audio")
        engine.runAndWait()
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
        engine.say("Could not request results from Google Speech Recognition service")
        engine.runAndWait()
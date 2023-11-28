import os
print(os.__file__)
import pyttsx3
print(pyttsx3.__file__)
#engine = pyttsx3.init()
engine = pyttsx3.init('dummy')
engine.say("hello world")
engine.runAndWait()
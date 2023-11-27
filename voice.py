import speech_recognition as sr
import pyttsx3

recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Load the audio file
audio_file = "filtered_recording.wav"
with sr.AudioFile(audio_file) as source:
    print(f"Loading audio file: {audio_file}")
    audio = recognizer.record(source)

try:
    print("Google Speech Recognition thinks you said:")
    recognized_text = recognizer.recognize_google(audio)
    print(recognized_text)
    engine.say("Google Speech Recognition thinks you said:")
    engine.say(recognized_text)
    engine.runAndWait()
except sr.UnknownValueError:
    print("Google Speech Recognition could not understand audio")
    engine.say("Google Speech Recognition could not understand audio")
    engine.runAndWait()
except sr.RequestError as e:
    print(f"Could not request results from Google Speech Recognition service; {e}")
    engine.say("Could not request results from Google Speech Recognition service")
    engine.runAndWait()

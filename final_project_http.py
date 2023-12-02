import speech_recognition as sr
import pyttsx3
import requests
import json
import wave, struct    
import pyaudio
import matplotlib.pyplot as plt
import numpy as np


# parameters for the wave file
RATE = 16000
FORMAT = pyaudio.paInt16 # 16-bit frames, ie audio is in 2 bytes
CHANNELS = 1             # mono recording, use 2 if you want stereo
CHUNK_SIZE = 1024        # bytes
RECORD_DURATION = 5     # how long the file will be in seconds
#ip_address = "172.20.10.12:5000"
# ip address of the raspberry pi
ip_address = "172.20.10.5:5000"

# initialize the recognizer
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# wait for user to press enter to start recording
while input("Press enter to record audio") == "":
    print("Recording...")
    # Record audio for RECORD_DURATION=5 seconds
    with wave.open("recording.wav", "wb") as wavefile:
        p = pyaudio.PyAudio()
        wavefile.setnchannels(CHANNELS)
        wavefile.setsampwidth(p.get_sample_size(FORMAT))
        wavefile.setframerate(RATE)
        stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True)
        for _ in range(0, RATE // CHUNK_SIZE * RECORD_DURATION):
            wavefile.writeframes(stream.read(CHUNK_SIZE))
        stream.close()
    p.terminate()
    print("Done recording")

    # Initialize an empty list to store audio data
    audio_data = []
    w = wave.open("recording.wav", "r")
    length = w.getnframes()
    # loop through the wave file and store the audio data
    for i in range(0, length):
        waveData = w.readframes(1)
        data = struct.unpack("<h", waveData)
        audio_data.append(int(data[0]))

    # Plot the original audio data
    plt.figure(figsize=(12, 12)) 
    plt.subplot(2, 2, 1)  # 2 rows, 2 columns, position 1
    plt.plot(audio_data, linestyle="-")
    plt.title("Original Audio Waveform")
    plt.xlabel("Sample")
    plt.ylabel("Amplitude")

    # Perform FFT
    n = len(audio_data)
    audio_fft = np.fft.fft(audio_data)
    frequencies = np.fft.fftfreq(n, d=1.0/RATE)

    # Get the magnitude of the FFT and corresponding frequency values
    magnitude = np.abs(audio_fft)[:n // 2]
    frequencies = frequencies[:n // 2]

    # Plot the frequency spectrum
    plt.subplot(2, 2, 2)  # 2 rows, 2 columns, position 2
    plt.plot(frequencies, magnitude)
    plt.title("Original Frequency Spectrum")
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Magnitude")
    plt.xlim(0, RATE / 2)

    # Identify the noise frequencies (example: noise between 3000 Hz to 5000 Hz)
    noise_freq_range = (300, 8000)

    # Create a filter
    filtered_fft = np.copy(audio_fft)
    for i, freq in enumerate(frequencies):
        if noise_freq_range[0] <= np.abs(freq) <= noise_freq_range[1]:
            filtered_fft[i] = 0

    # Plot the filtered frequency spectrum
    plt.subplot(2, 2, 4)  # 2 rows, 2 columns, position 4
    plt.plot(frequencies, np.abs(filtered_fft)[:n // 2])
    plt.title("Filtered Frequency Spectrum")
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Magnitude")
    plt.xlim(0, RATE / 2)


    # Apply the filter and perform inverse FFT
    filtered_audio = np.fft.ifft(filtered_fft)

    # Convert the filtered audio back to 16-bit integer format
    # Ensure the real part is taken and properly scaled
    filtered_audio_int = np.int16(filtered_audio.real / np.max(np.abs(filtered_audio.real)) * 32767)
    #print(filtered_audio_int)

    # Plot the filtered sound wave
    plt.subplot(2, 2, 3)  # 2 rows, 2 columns, position 3
    plt.plot(filtered_audio.real, linestyle="-")
    plt.title("Filtered Audio Waveform")
    plt.xlabel("Sample")
    plt.ylabel("Amplitude")

    # Display the plots
    plt.tight_layout()  # Adjusts subplot params so that subplots fit into the figure area
    # hide the graph for now
    #plt.show()
    # save the graph
    plt.savefig('./static/voice.jpg', bbox_inches='tight')

    # Write the filtered audio to a new wave file
    with wave.open("filtered_recording.wav", "wb") as wavefile:
        wavefile.setnchannels(CHANNELS)
        wavefile.setsampwidth(p.get_sample_size(FORMAT))
        wavefile.setframerate(RATE)
        for sample in filtered_audio_int:
            wavefile.writeframes(struct.pack('<h', sample))

    print("Filtered recording saved as 'filtered_recording.wav'")

    # Load the audio file
    audio_file = "filtered_recording.wav"
    with sr.AudioFile(audio_file) as source:
        print(f"Loading audio file: {audio_file}")
        audio = recognizer.record(source)

    try:
        print("Google Speech Recognition thinks you said:")
        # recognize speech using Google Speech Recognition
        words = recognizer.recognize_google(audio)
        print(words)
        if "hey" in words.lower():
            engine.say("hello there")
            engine.runAndWait()
        elif "weather" in words.lower():
            try:
                response_json = requests.get("http://{}/weather".format(ip_address))
                response_dict = json.loads(response_json.text)
                answer = "today is {}".format(response_dict['condition'])+" and the temperature is {}".format(response_dict['temperature'])+" fahrenheit"
                print(answer)
                engine.say(answer)
                engine.runAndWait()
            except:
                engine.say("error")
                engine.runAndWait()
        elif "led" in words.lower():
            if "on" in words.lower():
                response = requests.put("http://{}/LED".format(ip_address), json={"LED": "ON"})
                if response.status_code == 200:
                    answer = "LED is on"
                    print(answer)
                    engine.say(answer)
                    engine.runAndWait()
                else:
                    print("error")
                    engine.say("error")
                    engine.runAndWait()
            elif "off" in words.lower():
                response = requests.put("http://{}/LED".format(ip_address), json={"LED": "OFF"})
                if response.status_code == 200:
                    answer = "LED is off"
                    print(answer)
                    engine.say(answer)
                    engine.runAndWait()
            elif "status" in words.lower():
                response = requests.get("http://{}/LED".format(ip_address))
                response_dict = json.loads(response.text)
                if response.status_code == 200:
                    answer = "LED is {}".format(response_dict['Response'])
                    print(answer)
                    engine.say(answer)
                    engine.runAndWait()
                else:
                    print("error")
                    engine.say("error")
                    engine.runAndWait()
        elif "ultrasonic" in words.lower():
            response = requests.get("http://{}/ultrasonic".format(ip_address))
            response_dict = json.loads(response.text)
            if response.status_code == 200:
                if response_dict['Warning'] == 'True':
                    answer = "Warning there is an object in front of you at {} centimeters\n".format(response_dict['US Reading'])
                    print(answer)
                    engine.say(answer)
                    engine.runAndWait()

                else:
                    answer = "There is no object in front of you, the distance is {} centimeters\n".format(response_dict['US Reading'])
                    print(answer)
                    engine.say(answer)
                    engine.runAndWait()

    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
        engine.say("Google Speech Recognition could not understand audio")
        engine.runAndWait()
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
        engine.say("Could not request results from Google Speech Recognition service")
        engine.runAndWait()
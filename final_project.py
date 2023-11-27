import wave, struct     # this will probably also need to be installed
import pyaudio
import matplotlib.pyplot as plt
import numpy as np
import json


RATE = 16000
FORMAT = pyaudio.paInt16 # 16-bit frames, ie audio is in 2 bytes
CHANNELS = 1             # mono recording, use 2 if you want stereo
CHUNK_SIZE = 1024        # bytes
RECORD_DURATION = 5     # how long the file will be in seconds

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
# w = wave.open("recording.wav", "rb")
# for i in range(w.getnframes()):
#     print(w.readframes(1))

# Initialize an empty list to store audio data
audio_data = []

print("Done recording")
w = wave.open("recording.wav", "r")
length = w.getnframes()
for i in range(0, length):
    waveData = w.readframes(1)
    data = struct.unpack("<h", waveData)
    audio_data.append(int(data[0]))

plt.figure(figsize=(12, 12)) 
# Plot the original sound wave
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
print(filtered_audio_int)
# output the filtered audio to a json file with RATE, FORMAT, CHANNELS, and CHUNK_SIZE, and the filtered_audio_int

# Convert numpy array to list for JSON serialization
filtered_audio_list = filtered_audio_int.tolist()

# Prepare the data dictionary
audio_data_dict = {
    "rate": RATE,
    "format": FORMAT,
    "channels": CHANNELS,
    "chunk_size": CHUNK_SIZE,
    "audio_data": filtered_audio_list
}

# Write to a JSON file
with open("filtered_audio_data.json", "w") as json_file:
    json.dump(audio_data_dict, json_file)

print("Filtered audio data saved as 'filtered_audio_data.json'")

# Plot the filtered sound wave
plt.subplot(2, 2, 3)  # 2 rows, 2 columns, position 3
plt.plot(filtered_audio.real, linestyle="-")
plt.title("Filtered Audio Waveform")
plt.xlabel("Sample")
plt.ylabel("Amplitude")

# Display the plots
plt.tight_layout()  # Adjusts subplot params so that subplots fit into the figure area
plt.show()

# Write the filtered audio to a new wave file
with wave.open("filtered_recording.wav", "wb") as wavefile:
    wavefile.setnchannels(CHANNELS)
    wavefile.setsampwidth(p.get_sample_size(FORMAT))
    wavefile.setframerate(RATE)
    for sample in filtered_audio_int:
        wavefile.writeframes(struct.pack('<h', sample))

print("Filtered recording saved as 'filtered_recording.wav'")

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




import wave      # this will probably also need to be installed
import pyaudio

RATE = 16000
FORMAT = pyaudio.paInt16 # 16-bit frames, ie audio is in 2 bytes
CHANNELS = 1             # mono recording, use 2 if you want stereo
CHUNK_SIZE = 1024        # bytes
RECORD_DURATION = 10     # how long the file will be in seconds

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
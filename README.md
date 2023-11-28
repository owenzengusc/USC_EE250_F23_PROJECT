# Voice-Controlled IoT System

## Team Members
- Owen Zeng
- Felix Chen

## Demo Video
[View Demo Online](<Link to your video>)

## Instructions to Compile/Execute Programs
1. **final_project_http.py (Run on Laptop)**
   - Install required libraries: `pyaudio`, `matplotlib`, `numpy`, `speech_recognition`, `pyttsx3`, `requests`, `wave`, `struct`.
   - Execute the script: `python final_project_http.py`.
   - Follow the on-screen instructions to record and process audio commands.

2. **rpi_http.py (Run on Raspberry Pi)**
   - Install Flask: `pip install Flask`.
   - Set up GrovePi: Follow [GrovePi setup instructions](https://github.com/DexterInd/GrovePi).
   - Run the script: `python rpi_http.py`.
   - The server will start, and the Raspberry Pi will begin responding to API requests.

## External Libraries Used
- **Laptop (final_project_http.py)**
  - `pyaudio`: For audio recording and processing.
  - `matplotlib`: For plotting audio waveforms and frequency spectrum.
  - `numpy`: For numerical operations, especially Fast Fourier Transform (FFT).
  - `speech_recognition`: For converting spoken words to text.
  - `pyttsx3`: For text-to-speech conversion.
  - `requests`: For sending HTTP requests to the Raspberry Pi server.
  - `wave`, `struct`: For handling .wav audio file format.

- **Raspberry Pi (rpi_http.py)**
  - `Flask`: For creating the HTTP server.
  - `grovepi`: For interfacing with GrovePi sensors and actuators.
  - `requests`: For making API requests to external services like Weather API.
  - `threading`: For running the ultrasonic sensor reading in a separate thread.
  - `json`: For JSON data handling.

Note: Ensure you have the latest version of Python installed and configure your Raspberry Pi with the necessary GrovePi sensors and actuators as per your project setup.

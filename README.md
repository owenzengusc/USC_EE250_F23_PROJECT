# Voice-Controlled IoT System

## Team Members
- Owen Zeng
- Felix Chen


## Instructions to Compile/Execute Programs
1. **final_project_http.py (Run on Laptop)**
   - Install required libraries: `pyaudio`, `matplotlib`, `numpy`, `speech_recognition`, `pyttsx3`, `requests`, `wave`, `struct`. If you are working on a MAC OS, you will need to use  `pip install py3-tts`.
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

## Example Voice Commands
- "Hey, how's the weather?" - The system will fetch and tell you the current weather conditions.
- "LED on" - Turns the LED connected to the Raspberry Pi on.
- "LED off" - Turns the LED connected to the Raspberry Pi off.
- "LED status" - Informs about the current status of the LED.
- "Ultrasonic" - Gives the current reading from the ultrasonic sensor.

## What Happens to Recordings
- Your voice is recorded for a duration of 5 seconds upon pressing enter.
- The recording is processed to filter out noise and then converted into text using Google Speech Recognition.
- Based on the recognized text, specific actions are triggered (like fetching weather data, controlling LED, etc.).
- The processed audio data and the FFT visualizations are temporarily saved locally for analysis purposes.

Note: Ensure you have the latest version of Python installed and configure your Raspberry Pi with the necessary GrovePi sensors and actuators as per your project setup.

brew install node
cd ee250_frontend
npm install
npm start

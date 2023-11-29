import logo from './logo.svg';
import './App.css';
import axios from 'axios';
import { useState, useEffect } from 'react';

function App() {
  const ipaddress = "172.20.10.5:5000"
  
  const [ledState, setLedState] = useState("Loading...");
  const [distance, setDistance] = useState("Loading...");
  const [weather, setWeather] = useState("Loading...");

  const checkLED = async () => {
    try {
      let res = await axios.get(`http://${ipaddress}/LED`);
      console.log(res)
      console.log(res.data);
      setLedState(res.data.Response);
    } catch {
      setLedState("RPi not online");
    }
  }

  const checkUltrasonicSensor = async () => {
    try {
      let res = await axios.get(`http://${ipaddress}/ultrasonic`);
      console.log(res.data);
      setDistance(res.data["US Reading"]);
    } catch {
      setDistance("RPi not online")
    }
  }

  const checkWeather = async () => {
    try {
      let res = await axios.get(`http://${ipaddress}/weather`);
      console.log(res.data);
      setWeather(`Condition: ${res.data.condition}\nTemperature: ${res.data.temperature}`);
    } catch {
      setWeather("RPi not online")
    }
  }

  const toggleLED = async () => {
    let newState = {"LED": "ON"};
    if(ledState === "ON") {
      newState["LED"] = "OFF";
    }
    try{
    await axios.put(`http://${ipaddress}/LED`, newState);
    } catch(err) {
      console.log(err);
    }
  }

  // On startup, check everything
  useEffect(() => {
    checkLED();
    checkUltrasonicSensor();
    checkWeather();
  }, []);

  return (
<div className="App bg-gray-100 min-h-screen flex flex-col items-center justify-center p-4">
  <h1 className="text-4xl font-extrabold text-blue-800 mb-6">EE250 Final Project Frontend</h1>
  <p className="text-xl mb-3">Authors: Owen Zeng and Felix Chen</p>
  <p className="mb-6 text-gray-600 italic">Note: use CLI interface for voice commands</p>
  <div className="space-y-6 w-full max-w-md">
    <div className="card bg-white shadow-lg rounded-lg p-4 hover:shadow-xl transition-shadow duration-300 ease-in-out">
      <button 
        className="btn px-6 py-3 bg-blue-500 text-white rounded-lg font-semibold text-lg hover:bg-blue-600 shadow transition duration-300 ease-in-out transform hover:-translate-y-1"
        onClick={() => checkLED()}>
        Check LED Status
      </button>
      <p className="text-center mt-4 text-lg font-medium">{ledState}</p>
    </div>
    <div className="card bg-white shadow-lg rounded-lg p-4 hover:shadow-xl transition-shadow duration-300 ease-in-out">
      <button 
        className="btn px-6 py-3 bg-green-500 text-white rounded-lg font-semibold text-lg hover:bg-green-600 shadow transition duration-300 ease-in-out transform hover:-translate-y-1"
        onClick={() => checkUltrasonicSensor()}>
        Check Radar Distance
      </button>
      <p className="text-center mt-4 text-lg font-medium">{distance}</p>
    </div>
    <div className="card bg-white shadow-lg rounded-lg p-4 hover:shadow-xl transition-shadow duration-300 ease-in-out">
      <button 
        className="btn px-6 py-3 bg-red-500 text-white rounded-lg font-semibold text-lg hover:bg-red-600 shadow transition duration-300 ease-in-out transform hover:-translate-y-1"
        onClick={() => checkWeather()}>
        Check Weather
      </button>
      <p className="text-center mt-4 text-lg font-medium">{weather}</p>
    </div>
    <button 
      className="btn w-full px-6 py-3 bg-purple-500 text-white rounded-lg font-semibold text-lg hover:bg-purple-600 shadow transition duration-300 ease-in-out transform hover:-translate-y-1"
      onClick={() => toggleLED()}>
      Toggle LED State
    </button>
  </div>
</div>
  );
}

export default App;

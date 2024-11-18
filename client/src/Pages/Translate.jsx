import React, { useState } from 'react';
import axios from 'axios';

const MyComponent = () => {
  const [letter, setLetter] = useState(null);

  const fetchData = async () => {
    try {
      const response = await axios.get('http://127.0.0.1:5000/detect',{
        headers: {
          'Content-Type': 'application/json'
        }
      });
      setLetter(response.data.predicted_character);
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  };

  const fetchDataCustom = async () =>{
    try {
      const response = await axios.get('http://127.0.0.1:5000/detectCustom',{
        headers: {
          'Content-Type': 'application/json'
        }
      });
      setLetter(response.data.predicted_character);

    } catch (error) {
      console.error('Error fetching data:', error);
      
    }
  }

  const speakLetter = () => {
    if (letter) {
      // Use text-to-speech API to speak out the letter
      const speechSynthesis = window.speechSynthesis;
      const utterance = new SpeechSynthesisUtterance(letter);
      speechSynthesis.speak(utterance);
    }
  };

  return (
    <div className="translate-container flex flex-col items-center justify-center h-screen bg-gray-800">
      {/* Predicted character section */}
      <div className="predicted-character mt-8 text-3xl font-bold text-gray-100">
        {letter ? `Predicted character: ${letter}`.split(',').map((char, index) => (
          <span key={index}>{char}</span>
        )) : 'Waiting for prediction...'}
      </div>

      {/* Translate button */}
      <button onClick={fetchData} className="translate-button bg-teal-500 hover:bg-teal-700 text-white font-bold py-2 px-4 rounded mt-4 focus:outline-none">
        Translate
      </button>

      <button onClick={fetchDataCustom} className="translate-button bg-teal-500 hover:bg-teal-700 text-white font-bold py-2 px-4 rounded mt-4 focus:outline-none">
        Translate with Custom Sign
      </button>
      {/* Speak button */}
      <button onClick={speakLetter} className="speak-button bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded mt-4 focus:outline-none">
        Speak
      </button>

      {/* Go back button */}
      {/* <Link to="/" className="back-button text-gray-300 mt-4">Go Back</Link> */}
    </div>
  );
};

export default MyComponent;

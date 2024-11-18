import React, { useState } from "react";
import axios from "axios";
import { Link } from "react-router-dom";

const TrainCustom = () => {
  const [noOfClasses, setNoOfClasses] = useState("");
  const [dataSize, setDataSize] = useState("");
  const [message, setMessage] = useState("");
  const [customSignNames, setCustomSignNames] = useState([]);
  const [showButton, setShowButton] = useState(false);

  const sendData = async () => {
    try {
      if (!noOfClasses || !dataSize) {
        console.error("Please fill in both fields");
        return;
      }

      const numClasses = parseInt(noOfClasses);
      const size = parseInt(dataSize);

      const response = await axios.post("http://127.0.0.1:5000/upload-image", {
        noOfClasses: numClasses,
        dataSize: size,
      });

      if (response.status === 200) {
        setMessage(response.data.message);
        setShowButton(true);
      } else {
        console.error("Error:", response.data.error);
      }
    } catch (error) {
      console.error("Error sending data:", error);
    }
  };

  const handleButtonClick = async () => {
    try {
      // Gather all custom sign names
      const customSignNamesData = customSignNames.map((name, index) => ({
        name,
        index: index,
      }));
      const config = {
        headers: {
          "Content-Type": "application/json",
        },
      };
      // Send all data to backend
      const response = await axios.post(
        "http://127.0.0.1:5000/detect",
        {
          // noOfClasses: parseInt(noOfClasses),
          // dataSize: parseInt(dataSize),
          customSignNames: customSignNamesData,
        },
        config
      );

      // Handle response from backend if needed
    } catch (error) {
      console.error("Error sending data to backend:", error);
    }
  };

  return (
    <div className="bg-gray-900 min-h-screen flex flex-col justify-center items-center">
      <h1 className="text-3xl font-bold text-teal-500">Train Custom Model</h1>

      <div className="max-w-md p-8 rounded-lg bg-gray-800 text-white">
        <label htmlFor="noOfClasses" className="block mb-2 ">
          Number of Custom Handsigns:
        </label>
        <input
          id="noOfClasses"
          type="number"
          placeholder="Enter number of custom handsigns you want to add"
          value={noOfClasses}
          onChange={(e) => setNoOfClasses(e.target.value)}
          className="rounded-lg p-2 mb-4 w-full text-black"
        />
        <label htmlFor="dataSize" className="block mb-2">
          Data Size of Image:
        </label>
        <input
          id="dataSize"
          type="number"
          placeholder="Data size of image"
          value={dataSize}
          onChange={(e) => setDataSize(e.target.value)}
          className="rounded-lg p-2 mb-4 w-full text-black"
        />
        <button
          onClick={sendData}
          className="bg-teal-500 text-white px-4 py-2 rounded-lg mb-4 w-full"
        >
          Take Images
        </button>
        {message && (
          <div>
            <h3>{message}</h3>
            <p>Give the name for custom handsign</p>
            <div>
              {[...Array(parseInt(noOfClasses))].map((_, index) => (
                <input
                  key={index}
                  type="text"
                  placeholder={`Custom handsign ${index + 1}`}
                  onChange={(e) => {
                    const newCustomSignNames = [...customSignNames];
                    newCustomSignNames[index] = e.target.value;
                    setCustomSignNames(newCustomSignNames);
                  }}
                  className="rounded-lg p-2 mb-4 w-full text-black"
                />
              ))}
            </div>
          </div>
        )}
        {showButton && (
          <Link to="/translate" className="w-full">
            <button
              onClick={handleButtonClick}
              className="bg-teal-500 text-white px-4 py-2 rounded-lg w-full"
            >
              Translate
            </button>
          </Link>
        )}
      </div>
    </div>
  );
};

export default TrainCustom;

import React, { useState } from "react";
import InputForm from "./components/InputForm";
import Results from "./components/Results";
import "./App.css";

const App = () => {
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [videoUrl, setVideoUrl] = useState(""); // Track the video URL
  const [playerRef, setPlayerRef] = useState(null); // ReactPlayer reference for seeking

  const handleAnalyzeSubmit = async (data) => {
    setLoading(true);
    setError(null);
    try {
      // Sending POST request to the backend API for video analysis
      const response = await fetch("http://127.0.0.1:5000/api/video/analyze", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
      });

      if (!response.ok) {
        throw new Error("Error analyzing videos.");
      }

      const result = await response.json();
      setResults(result.results); // Set the analysis results
      setVideoUrl(data.urls[0]); 
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };
  

  // Function to handle timestamp click and jump to that time in the video
  const handleTimestampClick = (timestamp) => {
    if (playerRef) {
      playerRef.seekTo(timestamp);  // ReactPlayer API to seek to the timestamp
    }
  };

  return (
    <div className="App">
      <h1>Video Analysis & Clip Extraction</h1>

      {/* Input Form */}
      <InputForm onSubmit={handleAnalyzeSubmit} />

      {/* Loading spinner */}
      {loading && <div>Loading...</div>}

      {/* Error message */}
      {error && <div className="error">{error}</div>}

      {/* Displaying results */}
      {results && (
        <div>
          {/* Only show the video player after results are received */}
          <Results 
            results={results} 
            onTimestampClick={handleTimestampClick}
            videoUrl={videoUrl} // Pass the videoUrl to play video
            setPlayerRef={setPlayerRef} // Pass ref setter to Results for ReactPlayer
          />
        </div>
      )}
    </div>
  );
};

export default App;

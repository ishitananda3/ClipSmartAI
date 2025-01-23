import React, { useRef } from "react";
import ReactPlayer from "react-player";
import "./Results.css";

const Results = ({ results }) => {
  const playerRefs = useRef({});

  const handleTimestampClick = (videoId, startTime) => {
    const videoElement = playerRefs.current[videoId];
    if (videoElement) {
      videoElement.seekTo(startTime, "seconds");
    }
  };

  const handleClipDownload = async (videoUrl, timestamp) => {
    try {
      const response = await fetch("http://127.0.0.1:5000/api/video/extract_clips", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          url: videoUrl,
          timestamps: [timestamp],
        }),
      });

      if (!response.ok) {
        throw new Error("Error extracting clip.");
      }

      const data = await response.json();
      const clips = data.clips;

      if (clips && clips.length > 0) {
        // Create a download link for the clip
        clips.forEach((clipUrl, index) => {
          const link = document.createElement("a");
          link.href = `http://127.0.0.1:5000/${clipUrl}`; // Assuming the server is serving the clips
          link.download = `clip_${index + 1}.mp4`;
          link.click();
        });
      } else {
        alert("No clips generated.");
      }
    } catch (error) {
      console.error(error);
      alert("Failed to download clips.");
    }
  };

  return (
    <div className="results-wrapper">
      <h2 className="results-title">Analysis Results</h2>
      {Object.entries(results).map(([videoId, timestamps]) => (
        <div key={videoId} className="result-item">
          <h3 className="video-title">Video ID: {videoId}</h3>

          {/* Embed the YouTube video player */}
          <div className="video-player">
            <ReactPlayer
              url={`https://www.youtube.com/watch?v=${videoId}`}
              controls={true}
              ref={(el) => (playerRefs.current[videoId] = el)}
            />
          </div>

           <ul className="timestamps-list">
            {timestamps.map((ts, idx) => (
              <li
                key={idx}
                className="timestamp-item"
                onClick={() => handleTimestampClick(videoId, ts.start)}
              >
                <div className="timestamp-info">
                  <strong>Start:</strong> {ts.start.toFixed(2)}s | <strong>End:</strong>{" "}
                  {(ts.end || ts.start + 5).toFixed(2)}s
                </div>
                <p className="timestamp-text">
                  <strong>Text:</strong> {ts.text}
                </p>

                <button
                  className="download-clip-button"
                  onClick={() =>
                    handleClipDownload(`https://www.youtube.com/watch?v=${videoId}`, {
                      start: ts.start,
                      end: ts.end || ts.start + 5, // Default end time to 5 seconds if not provided
                    })
                  }
                >
                  Download Clip
                </button>
              </li>
            ))}
          </ul>
        </div>
      ))}
    </div>
  );
};

export default Results;

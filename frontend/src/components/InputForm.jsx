import React, { useState } from "react";
import ReactPlayer from "react-player";
import "./InputForm.css";

const InputForm = ({ onSubmit, videoUrl }) => {
  const [urls, setUrls] = useState("");
  const [keywords, setKeywords] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    const urlList = urls.split("\n").map((url) => url.trim());
    const keywordList = keywords.split(",").map((kw) => kw.trim());
    onSubmit({ urls: urlList, keywords: keywordList });
  };

  return (
    <div className="form-wrapper">
      <h2 className="form-title">Video Analysis Tool</h2>
      <form onSubmit={handleSubmit} className="input-form">
        <label htmlFor="urls" className="form-label">
          Paste YouTube URLs (one per line):
        </label>
        <textarea
          placeholder="Paste YouTube URLs (one per line)"
          className="form-textarea"
          id="urls"
          value={urls}
          onChange={(e) => setUrls(e.target.value)}
          rows="6"
        />
        <label htmlFor="keywords" className="form-label">
          Enter keywords (comma-separated):
        </label>
        <input
          type="text"
          id="keywords"
          className="form-input"
          placeholder="Enter keywords (comma-separated)"
          value={keywords}
          onChange={(e) => setKeywords(e.target.value)}
        />
        
        <button type="submit" className="form-button">
          Analyze
        </button>
      </form>

      {/* Only show the video after the analysis is done */}
      {videoUrl && (
        <div className="video-player">
          <ReactPlayer url={videoUrl} controls={true} />
        </div>
      )}
    </div>
  );
};

export default InputForm;

A web application to extract video clips from YouTube videos based on keyword occurrences. Identify timestamps where keywords appear, download videos, and extract relevant MP4 clips seamlessly.

Features
Extract timestamps from video transcripts where specified keywords are used.
Download video clips (MP4) corresponding to keyword timestamps.
Play specific timestamps directly in the UI.
Support for multiple YouTube video URLs.
Handles errors gracefully, such as missing keywords.

Tech Stack
Frontend: React.js, React Player, CSS
Backend: Flask, yt-dlp, ffmpeg

Setup
Prerequisites
Python 3.8+
Node.js and npm
ffmpeg installed (ffmpeg -version to verify)
yt-dlp installed (pip install yt-dlp)

git clone https://github.com/ishitananda3/ClipSmartAI.git

cd backend
pip install -r requirements.txt
python app.py

cd frontend
npm install
npm start

Usage
Start both the frontend and backend servers.
Enter YouTube URLs and keywords in the UI.
View keyword timestamps and play or download the extracted clips as MP4.

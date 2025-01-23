from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from utils.transcript import get_youtube_transcript, get_playlist_transcripts
from models.ai_model import analyze_transcript
from utils.video_utils import download_video, extract_clip
import os
app = Flask(__name__)
CORS(app)


# Route to analyze the video based on transcript and keywords
@app.route('/api/video/analyze', methods=['POST'])
def analyze_video():
    data = request.json
    urls = data.get('urls')  # Accept multiple URLs
    keywords = data.get('keywords')

    if not urls or not keywords:
        return jsonify({'error': 'URLs and keywords are required.'}), 400

    results = {}
    for url in urls:
        if 'playlist' in url:
            # If it's a playlist URL, fetch transcripts for all videos in the playlist
            transcripts = get_playlist_transcripts(url)
            for video_id, transcript in transcripts.items():
                analysis = analyze_transcript(transcript, keywords)
                results[video_id] = analysis
        else:
            # Single video URL
            video_id = url.split('v=')[-1]  # Extract video ID
            transcript = get_youtube_transcript(video_id)
            if transcript:
                analysis = analyze_transcript(transcript, keywords)
                results[video_id] = analysis

    return jsonify({'results': results}), 200

@app.route('/api/video/extract_clips', methods=['POST'])
def extract_clips():
    data = request.json
    url = data['url']
    timestamps = data['timestamps']

    # Directory to store clips
    clips_dir = "clips"
    os.makedirs(clips_dir, exist_ok=True)

    # Clear old clips before processing new ones
    for old_clip in os.listdir(clips_dir):
        os.remove(os.path.join(clips_dir, old_clip))

    try:
        clips = []
        video_id = url.split('v=')[-1]  # Extract video ID (or generate a unique identifier)
        video_path = download_video(url, f"temp_video_{video_id}.mp4", use_cookies=True)

        for ts in timestamps:
            start_time = ts['start']
            end_time = ts.get('end', start_time + 5)  # Default end_time to 5 seconds if not specified

            # Use video ID and timestamps to create unique filenames
            clip_filename = f"clip_{video_id}_{start_time:.2f}-{end_time:.2f}.mp4"
            clip_file = extract_clip(video_path, start_time, end_time, os.path.join(clips_dir, clip_filename))
            clips.append(clip_file)

        return jsonify({"clips": clips}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Route to handle playlist and fetch transcripts for all videos in the playlist
@app.route('/api/playlist/transcripts', methods=['POST'])
def get_playlist():
    data = request.json
    playlist_urls = data['playlist_urls']

    if not playlist_urls:
        return jsonify({'error': 'Playlist URLs are required.'}), 400

    # Extract video IDs from the playlist URLs
    video_ids = []
    for url in playlist_urls:
        if 'v=' in url:
            video_ids.append(url.split('v=')[-1])

    try:
        # Fetch transcripts for all video IDs in the playlist
        transcripts = get_playlist_transcripts(video_ids)
        return jsonify({"transcripts": transcripts}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Serve the clips from the server (static files)
@app.route('/clips/<path:filename>')
def serve_clip(filename):
    clips_dir = "clips"
    return send_from_directory(clips_dir, filename)

if __name__ == '__main__':
    app.run(debug=True)

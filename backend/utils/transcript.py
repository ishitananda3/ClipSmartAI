from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound
import yt_dlp


def get_youtube_transcript(video_id, requested_language="en"):
    """
    Fetches the transcript for a given YouTube video ID.
    Tries to fetch in the requested language, and falls back to other available languages if necessary.
    """
    try:
        # Attempt to fetch transcript in the requested language
        return YouTubeTranscriptApi.get_transcript(video_id, languages=[requested_language])
    except NoTranscriptFound:
        print(f"No transcript found in the requested language '{requested_language}' for video ID: {video_id}")
        try:
            # List all available transcripts for the video
            transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
            for transcript in transcript_list:
                if transcript.language_code != requested_language:
                    print(f"Falling back to language: {transcript.language} ({transcript.language_code})")
                    return transcript.fetch()
        except Exception as e:
            print(f"Failed to fetch transcript in any language for video ID {video_id}. Error: {str(e)}")
    except TranscriptsDisabled:
        print(f"Transcripts are disabled for video ID: {video_id}")
    except Exception as e:
        print(f"Unexpected error fetching transcript for video ID {video_id}: {str(e)}")
    return None


def get_playlist_transcripts(playlist_url, requested_language="en"):
    """
    Extracts video IDs from a YouTube playlist and fetches transcripts for each video.
    """
    try:
        # Extract video IDs from the playlist
        ydl_opts = {
            'quiet': True,
            'noplaylist': False,
            'extract_flat': True  # Only extract video metadata without downloading
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            playlist_info = ydl.extract_info(playlist_url, download=False)

            # Ensure the playlist has entries
            if 'entries' not in playlist_info or not playlist_info['entries']:
                print(f"No videos found in the playlist: {playlist_url}")
                return {}

            # Extract video URLs
            video_urls = [entry['url'] for entry in playlist_info['entries'] if 'url' in entry]

        # Fetch transcripts for each video
        transcripts = {}
        for video_url in video_urls:
            video_id = video_url.split('v=')[-1]
            print(f"Fetching transcript for video ID: {video_id}")
            transcript = get_youtube_transcript(video_id, requested_language=requested_language)
            if transcript:
                transcripts[video_id] = transcript
            else:
                print(f"No transcript available for video ID: {video_id}")

        return transcripts
    except Exception as e:
        print(f"Error fetching playlist transcripts: {str(e)}")
        return {}


# Example usage
if __name__ == "__main__":
    # Replace with your playlist URL
    playlist_url = "https://www.youtube.com/playlist?list=YOUR_PLAYLIST_ID"
    requested_language = "en"  # Change to desired language code, e.g., 'es' for Spanish

    transcripts = get_playlist_transcripts(playlist_url, requested_language=requested_language)

    # Print the fetched transcripts
    if transcripts:
        for video_id, transcript in transcripts.items():
            print(f"Transcript for video ID {video_id}:")
            for entry in transcript[:3]:  # Print first 3 entries for brevity
                print(entry)
    else:
        print("No transcripts were fetched.")

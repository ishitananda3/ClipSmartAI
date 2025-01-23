import yt_dlp
import os
import subprocess


def download_video(url, output_path, use_cookies=False, cookie_file=None):
    """
    Downloads a video from a given URL using yt-dlp.
    
    :param url: URL of the video to download
    :param output_path: Path where the video will be saved
    :param use_cookies: Whether to use cookies for authentication
    :param cookie_file: Path to the cookie file if use_cookies is True
    :return: Path of the downloaded video
    """
    try:
        ydl_opts = {
            'format': 'mp4',  # Download as mp4
            'outtmpl': output_path,  # Save the video in the specified path
        }

        if use_cookies and cookie_file:
            ydl_opts['cookiefile'] = cookie_file

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        if os.path.exists(output_path):
            return output_path
        else:
            raise Exception("Failed to download the video in the correct format.")
    except Exception as e:
        raise Exception(f"Error downloading video: {str(e)}")

def extract_clip(video_path, start_time, end_time, output_clip_path):
    """
    Extracts a clip from a video using FFmpeg, from start_time to end_time.
    """
    try:
        # Use FFmpeg to cut the clip between start_time and end_time
        command = [
            "ffmpeg",
            "-ss", str(start_time),  # Start time
            "-to", str(end_time),    # End time
            "-i", video_path,        # Input video
            "-c:v", "libx264",       # Video codec
            "-c:a", "aac",           # Audio codec
            "-strict", "experimental",  # Compatibility flag
            "-y",  # Overwrite output file if it exists
            output_clip_path         # Output file
        ]
        subprocess.run(command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        if os.path.exists(output_clip_path):
            return output_clip_path
        else:
            raise Exception("Error extracting clip: Clip file not created.")
    except subprocess.CalledProcessError as e:
        raise Exception(f"FFmpeg process failed: {str(e)}")
    except Exception as e:
        raise Exception(f"Error extracting clip: {str(e)}")


def extract_clip_with_url(url, start_time, end_time, output_clip_path):
    """
    Directly extracts a clip from a video URL using yt-dlp and FFmpeg.
    
    :param url: URL of the video to extract the clip from
    :param start_time: Start time of the clip in seconds
    :param end_time: End time of the clip in seconds
    :param output_clip_path: Path where the extracted clip will be saved
    :return: Path of the extracted clip
    """
    try:
        # Prepare yt-dlp options for fetching video metadata
        ydl_opts = {
            'format': 'mp4',
            'quiet': True,
            'noplaylist': True,
            'no_warnings': True,
        }

        # Extract video metadata without downloading
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            video_url = info_dict['url']  # Direct video URL from metadata

        # Use FFmpeg to extract the clip from the direct video URL
        command = [
            "ffmpeg",
            "-ss", str(start_time),  # Start time
            "-i", video_url,         # Input video (URL)
            "-to", str(end_time),    # End time
            "-c:v", "libx264",       # Video codec
            "-c:a", "aac",           # Audio codec
            "-strict", "experimental",  # Compatibility flag
            "-y",  # Overwrite output file if it exists
            output_clip_path         # Output file
        ]
        subprocess.run(command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        if os.path.exists(output_clip_path):
            return output_clip_path
        else:
            raise Exception("Error extracting clip: Clip file not created.")
    except subprocess.CalledProcessError as e:
        raise Exception(f"FFmpeg process failed: {str(e)}")
    except Exception as e:
        raise Exception(f"Error extracting clip from URL: {str(e)}")


# Save this file as app.py
from flask import Flask, render_template, request, jsonify, stream_with_context, Response
from yt_dlp import YoutubeDL
import os
import tempfile
from flask_sse import sse
import time

app = Flask(__name__)
app.config["REDIS_URL"] = "redis://localhost:6379"
app.register_blueprint(sse, url_prefix='/stream')

# Dictionary to store progress information
progress_data = {"progress": 0}

def download_hook(d):
    if d['status'] == 'downloading':
        # Extract percentage and update global progress_data
        progress = d['_percent_str'].strip()
        progress_data['progress'] = progress

        # Send progress to the front-end via SSE
        sse.publish({"progress": progress}, type='progress')

# Function to validate YouTube URLs
def is_valid_youtube_url(url):
    return "youtube.com/watch" in url or "youtu.be/" in url

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download_video():
    video_url = request.form.get('video_url', '').strip()

    # Validate the URL
    if not is_valid_youtube_url(video_url):
        return "Invalid YouTube URL. Please check and try again.", 400

    try:
        # yt-dlp options for downloading the best quality video
        ydl_opts = {
            'format': 'best',
            'noplaylist': True,  # Disable playlist downloading
            'quiet': True,       # Suppress yt-dlp output
            'progress_hooks': [download_hook],  # Add hook to track progress
        }

        with YoutubeDL(ydl_opts) as ydl:
            # Extract video information without downloading
            info_dict = ydl.extract_info(video_url, download=False)
            video_title = info_dict.get('title', 'video')
            video_ext = info_dict.get('ext', 'mp4')
            filename = f"{video_title}.{video_ext}"

            # Create a temporary file
            temp_dir = tempfile.mkdtemp()
            temp_file_path = os.path.join(temp_dir, filename)

            # Update yt-dlp options to download to the temporary file
            ydl_opts['outtmpl'] = temp_file_path

            # Download the video
            ydl.download([video_url])

        # Send the file to the user
        return jsonify({"download_url": temp_file_path})

    except Exception as e:
        return f"An error occurred: {e}", 500

if __name__ == '__main__':
    app.run(debug=True)

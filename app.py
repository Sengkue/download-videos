# Save this file as app.py
from flask import Flask, render_template, request, jsonify
from yt_dlp import YoutubeDL
import os
import tempfile
import threading

app = Flask(__name__)

# Global variable to store progress information
progress_data = {"progress": 0}

def download_hook(d):
    if d['status'] == 'downloading':
        # Extract percentage and update global progress_data
        progress = d['_percent_str'].strip()
        progress_data['progress'] = progress

def video_download_thread(video_url):
    global progress_data
    # yt-dlp options for downloading the best quality video
    ydl_opts = {
        'format': 'best',
        'noplaylist': True,
        'quiet': True,
        'progress_hooks': [download_hook],
    }

    with YoutubeDL(ydl_opts) as ydl:
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

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download_video():
    video_url = request.form.get('video_url', '').strip()

    # Validate the URL
    if not video_url.startswith('http'):
        return "Invalid YouTube URL. Please check and try again.", 400

    global progress_data
    progress_data['progress'] = 0

    # Start a new thread for downloading the video
    thread = threading.Thread(target=video_download_thread, args=(video_url,))
    thread.start()

    return jsonify({"status": "Download started"}), 200

@app.route('/progress', methods=['GET'])
def get_progress():
    return jsonify(progress_data)

if __name__ == '__main__':
    app.run(debug=True)

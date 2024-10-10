# Save this file as app.py
from flask import Flask, render_template, request, send_file, jsonify
import os
import tempfile
import time
from yt_dlp import YoutubeDL
from yt_dlp.utils import DownloadError

app = Flask(__name__)

# Initialize a global variable to hold the download progress
download_progress = 0

# Function to validate YouTube URLs
def is_valid_youtube_url(url):
    return "youtube.com/watch" in url or "youtu.be/" in url

# Function to update the progress
def progress_hook(d):
    global download_progress
    if d['status'] == 'downloading':
        download_progress = int(d['downloaded_bytes'] / d['total_bytes'] * 100)

# Home route to render the HTML form
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle the video download request
@app.route('/download', methods=['POST'])
def download_video():
    global download_progress
    video_url = request.form.get('video_url', '').strip()
    
    # Reset the progress
    download_progress = 0

    # Validate the URL
    if not is_valid_youtube_url(video_url):
        return "Invalid YouTube URL. Please check and try again.", 400

    try:
        # yt-dlp options for downloading the best quality video
        ydl_opts = {
            'format': 'best',
            'noplaylist': True,
            'quiet': True,
            'no_warnings': True,
            'restrictfilenames': True,
            'outtmpl': '%(title)s.%(ext)s',
            'progress_hooks': [progress_hook],  # Set the progress hook
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
            ydl_opts_temp = ydl_opts.copy()
            ydl_opts_temp['outtmpl'] = temp_file_path

            # Download the video to the temporary file
            ydl_temp = YoutubeDL(ydl_opts_temp)
            ydl_temp.download([video_url])

        # Send the file to the user
        return send_file(
            temp_file_path,
            as_attachment=True,
            download_name=filename,
            mimetype='application/octet-stream'
        )

    except DownloadError as de:
        print(f"DownloadError: {de}")
        return "Error downloading the video. Please check the URL or try again later.", 500
    except Exception as e:
        print(f"Exception: {e}")
        return f"An unexpected error occurred: {e}", 500
    finally:
        # Clean up the temporary directory and file
        try:
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)
            if os.path.exists(temp_dir):
                os.rmdir(temp_dir)
        except Exception as cleanup_error:
            print(f"Cleanup Error: {cleanup_error}")

# Route to get the current download progress
@app.route('/progress')
def get_progress():
    return jsonify(progress=download_progress)

if __name__ == '__main__':
    app.run(debug=True)

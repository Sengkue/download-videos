# Save this file as app.py
from flask import Flask, render_template, request, send_file
from pytube import YouTube
import os
from urllib.parse import urlparse
from pytube.exceptions import VideoUnavailable

app = Flask(__name__)

# Directory to store downloaded videos
DOWNLOAD_FOLDER = 'downloads'

# Ensure the download folder exists
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

# Function to check if a URL is valid
def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc, result.path])
    except:
        return False

# Home route to render the HTML form
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle the video download request
@app.route('/download', methods=['POST'])
def download_video():
    video_url = request.form['video_url']

    # Validate the URL format
    if not is_valid_url(video_url) or "youtube.com" not in video_url:
        return "Invalid YouTube URL. Please check and try again."

    try:
        # Attempt to create a YouTube object
        yt = YouTube(video_url)

        # Fetch the highest resolution stream
        stream = yt.streams.filter(progressive=True).first()

        if not stream:
            return "No available streams for this video."

        # Download the video to the downloads folder
        stream.download(output_path=DOWNLOAD_FOLDER)
        video_title = stream.default_filename

        # Prepare the file path for downloading
        file_path = os.path.join(DOWNLOAD_FOLDER, video_title)

        # Send the file for download
        return send_file(file_path, as_attachment=True)

    except VideoUnavailable:
        return "The video is unavailable. Please check the URL."
    except Exception as e:
        print(f"Error: {e}")
        return f"Error downloading the video: {e}. Please check the URL or try again later."

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)

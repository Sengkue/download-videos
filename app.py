# Save this file as app.py
from flask import Flask, render_template, request, send_file, redirect, url_for
from pytube import YouTube
import os

app = Flask(__name__)

# Define the path to store the downloaded videos
DOWNLOAD_FOLDER = 'downloads'

# Ensure the download folder exists
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download_video():
    try:
        # Get the YouTube URL from the form
        video_url = request.form['video_url']

        # Download the video using pytube
        yt = YouTube(video_url)
        stream = yt.streams.get_highest_resolution()
        stream.download(output_path=DOWNLOAD_FOLDER)
        video_title = stream.default_filename

        # Prepare the file path for downloading
        file_path = os.path.join(DOWNLOAD_FOLDER, video_title)

        # Send the file for download
        return send_file(file_path, as_attachment=True)

    except Exception as e:
        print(f"Error: {e}")
        return "Error downloading the video. Please check the URL."

if __name__ == '__main__':
    app.run(debug=True)

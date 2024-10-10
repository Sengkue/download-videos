from flask import Flask, render_template, request, send_file
import os
from yt_dlp import YoutubeDL

app = Flask(__name__)

# Directory to store downloaded videos
DOWNLOAD_FOLDER = 'downloads'

# Ensure the download folder exists
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download_video():
    video_url = request.form['video_url']
    
    try:
        # Set yt-dlp options for downloading the best video quality
        ydl_opts = {
            'format': 'best',  # Choose the best quality format
            'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),  # Save the file to the downloads folder
        }

        # Use yt-dlp to download the video
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=True)
            video_title = ydl.prepare_filename(info)
            video_title = video_title.split("/")[-1]

        # Prepare the file path for download
        file_path = os.path.join(DOWNLOAD_FOLDER, video_title)

        # Send the file for download
        return send_file(file_path, as_attachment=True)

    except Exception as e:
        return f"Error downloading the video: {e}. Please check the URL or try again later."

if __name__ == '__main__':
    app.run(debug=True)

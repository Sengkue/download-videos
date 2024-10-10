from flask import Flask, render_template, request, send_file
import os
import tempfile  # For temporary files
from yt_dlp import YoutubeDL
import shutil  # For cleaning up temp files

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download_video():
    video_url = request.form['video_url']
    
    try:
        # Create a temporary directory to store the video file temporarily
        with tempfile.TemporaryDirectory() as tmpdirname:
            ydl_opts = {
                'format': 'best',  # Download the best quality video
                'outtmpl': os.path.join(tmpdirname, '%(title)s.%(ext)s'),  # Store in temporary folder
            }

            # Use yt-dlp to download the video
            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(video_url, download=True)
                video_filename = ydl.prepare_filename(info)
                video_title = video_filename.split("/")[-1]

            # Send the file to the user for download
            return send_file(video_filename, as_attachment=True, download_name=video_title)

    except Exception as e:
        return f"Error downloading the video: {e}. Please check the URL or try again later."

if __name__ == '__main__':
    app.run(debug=True)

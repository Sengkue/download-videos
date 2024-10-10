# Save this file as app.py
from flask import Flask, render_template, request, send_file
import yt_dlp
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    video_url = request.form['video_url']
    download_audio = request.form.get('download_type') == 'audio'  # Check if the audio option is selected

    try:
        if download_audio:
            # Download audio only
            ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',  # Extract audio
                    'preferredcodec': 'mp3',  # Convert to MP3
                    'preferredquality': '192',
                }],
                'outtmpl': '%(title)s.%(ext)s',  # Save with title as filename
            }
        else:
            # Download video
            ydl_opts = {
                'format': 'best',
                'outtmpl': '%(title)s.%(ext)s',  # Save with title as filename
            }

        # Use yt-dlp to download the video/audio
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_url, download=True)  # Download the file
            title = info_dict.get('title', None)

        # Determine the correct filename based on whether we downloaded audio or video
        file_extension = 'mp3' if download_audio else 'mp4'
        filename = f"{title}.{file_extension}"

        return send_file(filename, as_attachment=True)

    except Exception as e:
        return render_template('index.html', error=str(e))

if __name__ == '__main__':
    app.run(debug=True)

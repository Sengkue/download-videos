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
        # Set the options for yt-dlp
        if download_audio:
            # Options for downloading audio
            ydl_opts = {
                'format': 'bestaudio/best',  # Download best audio available
                'outtmpl': '%(title)s.%(ext)s',  # Save with title as filename
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',  # Extract audio
                    'preferredcodec': 'mp3',  # Convert to mp3
                    'preferredquality': '192',  # Set quality
                }],
                'noplaylist': True,  # Download only single video
            }
        else:
            # Options for downloading video
            ydl_opts = {
                'format': 'best',  # Download best video available
                'outtmpl': '%(title)s.%(ext)s',  # Save with title as filename
                'noplaylist': True,  # Download only single video
            }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_url, download=False)  # Get video info
            title = info_dict.get('title', None)
            ydl.download([video_url])  # Download the video/audio

        # Return the appropriate file after download
        if download_audio:
            filename = f"{title}.mp3"
        else:
            filename = f"{title}.mp4"

        return send_file(filename, as_attachment=True)

    except Exception as e:
        return render_template('index.html', error=str(e))

if __name__ == '__main__':
    app.run(debug=True)

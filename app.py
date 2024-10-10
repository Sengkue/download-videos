# Save this file as app.py
from flask import Flask, render_template, request, send_file, jsonify
import yt_dlp
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    video_url = request.form.get('video_url')
    download_type = request.form.get('download_type')

    if not video_url:
        return render_template('index.html', error="Please provide a valid YouTube URL.")

    try:
        if download_type == 'audio':
            # Set options for audio download
            ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'outtmpl': '%(title)s.%(ext)s',
                'noplaylist': True,
            }
        else:
            # Set options for video download
            ydl_opts = {
                'format': 'bestvideo+bestaudio/best',
                'outtmpl': '%(title)s.%(ext)s',
                'noplaylist': True,
            }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_url, download=True)
            title = info_dict.get('title', None)
            file_name = ydl.prepare_filename(info_dict)

        return send_file(file_name, as_attachment=True)

    except Exception as e:
        return render_template('index.html', error=f"Error downloading the video/audio: {str(e)}")

if __name__ == '__main__':
    app.run(debug=True)

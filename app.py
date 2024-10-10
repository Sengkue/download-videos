# Save this file as app.py
from flask import Flask, render_template, request, send_file
import yt_dlp

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    video_url = request.form['video_url']
    download_audio = 'audio' in request.form  # Check if the audio option is selected

    try:
        ydl_opts = {
            'format': 'bestaudio/best' if download_audio else 'best',  # Download audio only if selected
            'outtmpl': '%(title)s.%(ext)s',  # Save with title as filename
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',  # Extract audio if downloading audio only
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }] if download_audio else [],  # Only add if downloading audio
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_url, download=False)  # Get video info
            title = info_dict.get('title', None)
            ydl.download([video_url])  # Download the video/audio

        return send_file(f"{title}.mp3", as_attachment=True) if download_audio else send_file(f"{title}.mp4", as_attachment=True)

    except Exception as e:
        return render_template('index.html', error=str(e))

if __name__ == '__main__':
    app.run(debug=True)

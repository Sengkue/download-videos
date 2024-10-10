# Save this file as app.py
from flask import Flask, request, render_template, send_file
import yt_dlp
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', error=None)

@app.route('/download', methods=['POST'])
def download():
    video_url = request.form['video_url']
    format_choice = request.form['format']  # Get format choice

    # Prepare options for yt-dlp
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best' if format_choice == 'video' else 'bestaudio/best',  # Choose format
        'outtmpl': 'downloads/%(title)s.%(ext)s',  # Output template
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',  # Set audio codec to mp3
            'preferredquality': '192',
        }] if format_choice == 'audio' else []
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_url, download=True)
            title = info_dict.get('title', None)
            if format_choice == 'audio':
                # If downloading audio, set filename for send_file
                filename = os.path.join('downloads', f"{title}.mp3")
            else:
                # If downloading video, set filename for send_file
                filename = os.path.join('downloads', f"{title}.{info_dict['ext']}")
        
        return send_file(filename, as_attachment=True)
    
    except Exception as e:
        return render_template('index.html', error=str(e))

if __name__ == '__main__':
    if not os.path.exists('downloads'):
        os.makedirs('downloads')
    app.run(debug=True)

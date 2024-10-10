# Save this file as app.py
from flask import Flask, render_template, request, send_file, jsonify
import yt_dlp
import os
import tempfile

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
        # Create a temporary file to save the download
        temp_file = tempfile.NamedTemporaryFile(delete=False)

        if download_type == 'audio':
            # Set options for audio download
            ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'outtmpl': temp_file.name,
                'noplaylist': True,
            }
        else:
            # Set options for video download
            ydl_opts = {
                'format': 'bestvideo+bestaudio/best',
                'outtmpl': temp_file.name,
                'noplaylist': True,
            }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_url, download=True)
            title = info_dict.get('title', None)

        # Set the correct filename for the response
        if download_type == 'audio':
            file_name = f"{title}.mp3"
        else:
            file_name = f"{title}.mp4"

        return send_file(temp_file.name, as_attachment=True, download_name=file_name)

    except Exception as e:
        return render_template('index.html', error=f"Error downloading the video/audio: {str(e)}")
    finally:
        # Clean up: Delete the temporary file after sending it to the user
        try:
            os.remove(temp_file.name)
        except Exception as cleanup_exception:
            print(f"Error cleaning up temporary file: {cleanup_exception}")

if __name__ == '__main__':
    app.run(debug=True)

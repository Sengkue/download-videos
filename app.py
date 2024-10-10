import os
from flask import Flask, render_template, request, send_file
import yt_dlp

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    video_url = request.form['video_url']
    download_audio = request.form.get('download_type') == 'audio'  # Check if audio is selected

    try:
        # Set the path to the local FFmpeg executable
        ffmpeg_path = os.path.join(os.getcwd(), 'ffmpeg', 'ffmpeg.exe')
        print("FFmpeg path:", ffmpeg_path)  # Debugging line

        # Set the options for yt-dlp based on the selection
        if download_audio:
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': '%(title)s.%(ext)s',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                    'executable': ffmpeg_path,  # Specify the local FFmpeg executable
                }],
                'noplaylist': True,
            }
        else:
            ydl_opts = {
                'format': 'bestvideo+bestaudio/best',
                'outtmpl': '%(title)s.%(ext)s',
                'merge_output_format': 'mp4',
                'postprocessors': [{
                    'key': 'FFmpegVideoMerge',
                    'executable': ffmpeg_path,  # Specify the local FFmpeg executable
                }],
                'noplaylist': True,
            }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_url, download=False)
            title = info_dict.get('title', None)
            ydl.download([video_url])  # Download the video/audio

        # Return the appropriate file after download
        filename = f"{title}.mp3" if download_audio else f"{title}.mp4"
        return send_file(filename, as_attachment=True)

    except Exception as e:
        return render_template('index.html', error=str(e))

if __name__ == '__main__':
    app.run(debug=True)

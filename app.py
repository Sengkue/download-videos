from flask import Flask, request, render_template, send_file, jsonify
import os
import yt_dlp

app = Flask(__name__)

# Global variable to hold the download progress
download_progress = {}

def progress_hook(d):
    if d['status'] == 'downloading':
        download_progress['percent'] = d['downloaded_bytes'] / d['total_bytes'] * 100
    elif d['status'] == 'finished':
        download_progress['percent'] = 100

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check', methods=['POST'])
def check():
    url = request.form.get('url')
    if not url:
        return "No URL provided", 400

    ydl_opts = {
        'format': 'best',
        'noplaylist': True,
        'quiet': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            title = info_dict.get('title', 'Unknown Title')
            formats = info_dict.get('formats', [])
            available_formats = []

            # Add MP4 video format option with sound
            available_formats.append({
                'format_id': 'bestvideo+bestaudio[ext=mp4]',
                'type': 'Video (MP4)',
            })

            # Add MP3 audio format option
            available_formats.append({
                'format_id': 'bestaudio[ext=m4a]',
                'type': 'Audio (MP3)',
            })

            return render_template('index.html', title=title, formats=available_formats, url=url)

    except Exception as e:
        return str(e), 500

@app.route('/download', methods=['POST'])
def download():
    global download_progress
    download_progress = {}  # Reset progress

    url = request.form.get('url')
    format_id = request.form.get('format_id')
    if not url or not format_id:
        return "No URL or format ID provided", 400

    # Set up yt-dlp options
    ydl_opts = {
        'format': format_id,
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'noplaylist': True,
        'progress_hooks': [progress_hook],
        'retries': 5,  # Retry up to 5 times
        'socket_timeout': 30,  # Timeout after 30 seconds
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Attempt to download the selected format
            ydl.download([url])
            filename = ydl.prepare_filename(ydl.extract_info(url))
            return send_file(filename, as_attachment=True)

    except Exception as e:
        print(f"Error during download: {str(e)}")  # Log the error
        return f"An error occurred while downloading the video: {str(e)}. Please try again later.", 500

@app.route('/progress')
def progress():
    return jsonify(download_progress)

if __name__ == '__main__':
    if not os.path.exists('downloads'):
        os.makedirs('downloads')
    app.run(debug=True)

from flask import Flask, request, render_template, send_file, jsonify
import os
import yt_dlp
import time
import threading

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

            desired_resolutions = ['1440', '1080', '720', '480', '360', '240']
            for f in formats:
                if 'height' in f and str(f['height']) in desired_resolutions:
                    format_info = {
                        'format_id': f['format_id'],
                        'height': f.get('height', 'N/A'),
                        'width': f.get('width', 'N/A'),
                        'filesize': f.get('filesize', f.get('filesize_approx', 'N/A')),
                        'ext': f.get('ext', 'N/A'),
                    }
                    available_formats.append(format_info)

            # Add MP3 format option
            available_formats.append({
                'format_id': 'bestaudio[ext=m4a]',
                'height': 'Audio',
                'width': 'N/A',
                'filesize': 'N/A',
                'ext': 'mp3',
            })

            return render_template('check.html', title=title, formats=available_formats, url=url)

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

    ydl_opts = {
        'format': format_id,
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'noplaylist': True,
        'progress_hooks': [progress_hook],  # Use progress hook
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])  # This will block until download is finished
            return send_file(ydl.prepare_filename(ydl.extract_info(url)), as_attachment=True)

    except Exception as e:
        return str(e), 500

@app.route('/progress')
def progress():
    return jsonify(download_progress)

if __name__ == '__main__':
    if not os.path.exists('downloads'):
        os.makedirs('downloads')
    app.run(debug=True)

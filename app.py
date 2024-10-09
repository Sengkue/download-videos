from flask import Flask, request, render_template, send_file, redirect, url_for, jsonify
import os
import yt_dlp
import time

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check', methods=['POST'])
def check():
    url = request.form.get('url')
    if not url:
        return "No URL provided", 400

    # Set up options for yt-dlp to get video info without downloading
    ydl_opts = {
        'format': 'best',
        'noplaylist': True,
        'quiet': True,  # Suppress output
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)  # Only extract info
            title = info_dict.get('title', 'Unknown Title')
            formats = info_dict.get('formats', [])
            available_formats = []

            # Filter formats based on desired resolutions and add MP3 option
            desired_resolutions = ['1440', '1080', '720', '480', '360', '240']
            for f in formats:
                if 'height' in f and str(f['height']) in desired_resolutions:
                    format_info = {
                        'format_id': f['format_id'],
                        'height': f.get('height', 'N/A'),
                        'width': f.get('width', 'N/A'),
                        'filesize': f.get('filesize', f.get('filesize_approx', 'N/A')),  # Size in bytes
                        'ext': f.get('ext', 'N/A'),
                    }
                    available_formats.append(format_info)

            # Add MP3 format option
            available_formats.append({
                'format_id': 'bestaudio[ext=m4a]',
                'height': 'Audio',
                'width': 'N/A',
                'filesize': 'N/A',  # Size is not available until download
                'ext': 'mp3',
            })

            return render_template('check.html', title=title, formats=available_formats, url=url)

    except Exception as e:
        return str(e), 500

@app.route('/download', methods=['POST'])
def download():
    url = request.form.get('url')
    format_id = request.form.get('format_id')
    if not url or not format_id:
        return "No URL or format ID provided", 400

    # Set up options for yt-dlp to download the selected format
    ydl_opts = {
        'format': format_id,  # Use the selected format ID
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'noplaylist': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info_dict)

            # Check if the file exists and has been completely downloaded
            for _ in range(5):
                if os.path.exists(filename):
                    return send_file(filename, as_attachment=True)
                time.sleep(1)

            return "File not found after download", 500
    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    if not os.path.exists('downloads'):
        os.makedirs('downloads')
    app.run(debug=True)

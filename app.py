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
            size = info_dict.get('filesize') or info_dict.get('filesize_approx')  # Get size in bytes

            # Convert size to a more readable format (MB)
            if size is not None:
                size_mb = size / (1024 * 1024)  # Convert bytes to megabytes
                size_info = f"Size: {size_mb:.2f} MB"
            else:
                size_info = "Size: Unknown"

            return render_template('check.html', title=title, size=size_info, url=url)  # Render check page

    except Exception as e:
        return str(e), 500

@app.route('/download', methods=['POST'])
def download():
    url = request.form.get('url')
    if not url:
        return "No URL provided", 400

    # Set up options for yt-dlp
    ydl_opts = {
        'format': 'best',
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

from flask import Flask, request, render_template, send_file, redirect, url_for
import os
import yt_dlp
import time

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

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
                    send_file(filename, as_attachment=True)
                    return redirect(url_for('index'))  # Redirect to homepage after downloading
                time.sleep(1)

            return "File not found after download", 500
    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    if not os.path.exists('downloads'):
        os.makedirs('downloads')
    app.run(debug=True)

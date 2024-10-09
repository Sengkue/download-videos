from flask import Flask, request, send_file, render_template
from pytube import YouTube
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form.get('url')  # Use get() to avoid KeyError
    print(f"Received URL: {url}")  # Debugging output
    if not url:
        return "No URL provided", 400  # Return error if URL is missing
    try:
        yt = YouTube(url)
        video = yt.streams.get_highest_resolution()
        video.download(output_path='downloads')
        return send_file(f'downloads/{video.default_filename}', as_attachment=True)
    except Exception as e:
        print(f"Error: {e}")  # Debugging output
        return str(e), 400  # Return the error message

if __name__ == '__main__':
    if not os.path.exists('downloads'):
        os.makedirs('downloads')
    app.run(debug=True)

from flask import Flask, render_template, request, send_file
from pytube import YouTube
import os
from urllib.parse import urlparse, parse_qs

app = Flask(__name__)

# Directory to store downloaded videos
DOWNLOAD_FOLDER = 'downloads'

# Ensure the download folder exists
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

# Function to clean and validate the URL
def clean_url(url):
    parsed_url = urlparse(url)
    # If the URL is from youtu.be, convert to full youtube URL
    if 'youtu.be' in parsed_url.netloc:
        video_id = parsed_url.path[1:]  # Extract the video ID from the path
        return f'https://www.youtube.com/watch?v={video_id}'
    # If there are query params (e.g. "?si="), remove them
    elif 'youtube.com' in parsed_url.netloc:
        query = parse_qs(parsed_url.query)
        return f'https://www.youtube.com/watch{parsed_url.path}'
    return url

# Home route to render the HTML form
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle the video download request
@app.route('/download', methods=['POST'])
def download_video():
    video_url = request.form['video_url']

    # Clean the URL before processing
    clean_video_url = clean_url(video_url)

    try:
        # Attempt to create a YouTube object with cleaned URL
        yt = YouTube(clean_video_url)

        # Fetch the highest resolution stream
        stream = yt.streams.filter(progressive=True).first()

        if not stream:
            return "No available streams for this video."

        # Download the video to the downloads folder
        stream.download(output_path=DOWNLOAD_FOLDER)
        video_title = stream.default_filename

        # Prepare the file path for downloading
        file_path = os.path.join(DOWNLOAD_FOLDER, video_title)

        # Send the file for download
        return send_file(file_path, as_attachment=True)

    except Exception as e:
        print(f"Error: {e}")
        return f"Error downloading the video: {e}. Please check the URL or try again later."

if __name__ == '__main__':
    app.run(debug=True)

import yt_dlp

url = 'https://www.youtube.com/watch?v=gRCnrjs0Ki0'  # Use the full URL

try:
    ydl_opts = {
        'outtmpl': 'downloads/%(title)s.%(ext)s',  # Save to downloads folder
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    print("Download completed!")
except Exception as e:
    print(f"Error: {e}")

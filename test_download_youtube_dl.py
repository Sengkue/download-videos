import youtube_dl

url = 'https://www.youtube.com/watch?v=gRCnrjs0Ki0'  # Use the full URL

ydl_opts = {
    'outtmpl': 'downloads/%(title)s.%(ext)s',  # Save to downloads folder
}

try:
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    print("Download completed!")
except Exception as e:
    print(f"Error: {e}")

from pytube import YouTube

url = 'https://www.youtube.com/watch?v=gRCnrjs0Ki0'  # Use the full URL

try:
    yt = YouTube(url)
    video = yt.streams.get_highest_resolution()
    print(f'Downloading: {video.title}')
    video.download(output_path='downloads')  # Ensure this folder exists
    print("Download completed!")
except Exception as e:
    print(f"Error: {e}")

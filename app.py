import json

@app.route('/check', methods=['POST'])
def check():
    data = json.loads(request.data)
    url = data.get('url')
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

            return jsonify(formats=available_formats)  # Return formats as JSON

    except Exception as e:
        return str(e), 500

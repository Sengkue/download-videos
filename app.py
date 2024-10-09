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

            # Desired resolutions to filter
            desired_resolutions = ['240', '360', '480', '720', '1080']
            seen_resolutions = set()  # To avoid duplicates by resolution

            for f in formats:
                # Only add formats that match desired resolutions
                if 'height' in f and str(f['height']) in desired_resolutions:
                    resolution_key = str(f['height'])  # Use height as the key for uniqueness
                    if resolution_key not in seen_resolutions:
                        format_info = {
                            'format_id': f['format_id'],
                            'height': f.get('height', 'N/A'),
                            'width': f.get('width', 'N/A'),
                            'filesize': f.get('filesize', f.get('filesize_approx', 'N/A')),
                            'ext': f.get('ext', 'N/A'),
                        }
                        available_formats.append(format_info)
                        seen_resolutions.add(resolution_key)  # Mark this resolution as seen

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

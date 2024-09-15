import yt_dlp
import json

def download_audio(url):
    ydl_opts = {
        'format': 'm4a/bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'm4a',
            'preferredquality': '192',
        }],
        'write-info-json': True,
        'embed-chapters': True,
        'outtmpl': '%(title)s.%(ext)s',
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    
    # Return the filename (assuming it's the same as the video title)
    info = ydl.extract_info(url, download=False)
    return f"{info['title']}.m4a"

def get_chapters(url):
    ydl_opts = {
        'quiet': True,
        'skip_download': True,
        'extract_flat': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        chapters = info_dict.get('chapters', [])
        
    return chapters

def format_chapters(chapters):
    return "\n".join([f"{chapter['title']} (Starts at {chapter['start_time']} seconds)" for chapter in chapters])
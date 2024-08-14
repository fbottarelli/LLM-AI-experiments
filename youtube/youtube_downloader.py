import yt_dlp
import json
import os
import re
from pydub import AudioSegment

from

# List of URLs to process
URLS = ["https://www.youtube.com/watch?v=ZJlfF1ESXVw&t=1750s"]
folder = "youtube/media"

# Define options for yt-dlp
ydl_opts = {
    'format': 'm4a/bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'm4a',
        'preferredquality': '192',
    }],
    'writeinfojson': True,
    'outtmpl': {
        'default': f'{folder}/%(title)s.%(ext)s'
    },
}

def sanitize_filename(filename):

    return filename

# Function to extract and print chapter information
def print_chapters(info_dict, sanitized_title):
    chapters = info_dict.get('chapters', [])
    if chapters:
        print("Chapters:")
        for chapter in chapters:
            start_time = chapter['start_time']
            chapter_title = chapter['title']
            print(f"{chapter_title} (Starts at {start_time} seconds)")
    else:
        print("No chapters found.")
    
    # Save chapters to a JSON file
    with open(f"{folder}/{sanitized_title}_chapters.json", 'w') as f:
        json.dump(chapters, f, indent=4)

# Function to split audio by chapters
def split_audio_by_chapters(sanitized_title):
    audio = AudioSegment.from_file(f"{folder}/{sanitized_title}.m4a", format="m4a")
    with open(f"{folder}/{sanitized_title}_chapters.json", 'r') as f:
        chapters = json.load(f)
    
    if not os.path.exists(f"{folder}/{sanitized_title}_chapters"):
        os.makedirs(f"{folder}/{sanitized_title}_chapters")
    
    for i, chapter in enumerate(chapters):
        start_time = int(chapter['start_time'] * 1000)  # pydub works in milliseconds
        end_time = int(chapters[i + 1]['start_time'] * 1000) if i + 1 < len(chapters) else len(audio)
        chapter_audio = audio[start_time:end_time]
        output_file = f"{folder}/{sanitized_title}_chapters/{sanitize_filename(chapter['title'])}.m4a"
        chapter_audio.export(output_file, format="mp4", codec="aac")

def process_urls(urls):
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        for url in urls:
            info_dict = ydl.extract_info(url, download=True)
            original_title = info_dict['title']
            sanitized_title = sanitize_filename(original_title)
            
            # Rename the downloaded file if necessary
            original_path = f"{folder}/{original_title}.m4a"
            sanitized_path = f"{folder}/{sanitized_title}.m4a"
            if os.path.exists(original_path) and original_path != sanitized_path:
                os.rename(original_path, sanitized_path)
            
            print_chapters(info_dict, sanitized_title)
            split_audio_by_chapters(sanitized_title)

if __name__ == "__main__":
    process_urls(URLS)


import yt_dlp

# List of URLs to process
URLS = ["https://www.youtube.com/watch?v=ZJlfF1ESXVw&t=1750s"]

# Define options for yt-dlp
ydl_opts = {
    'format': 'm4a/bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'm4a',
        'preferredquality': '192',
    }],
    'write-info-json': True,  # Save metadata including chapter info
    'embed-chapters': True,    # Embed chapter info into the audio file
    'outtmpl': {
        'default': 'youtube_dub/media/%(title)s'.replace(' ', '_') + '.%(ext)s'  # Output filename template without spaces in the media directory
    },
}

# Function to extract and print chapter information
import json

def print_chapters(info_dict, title):
    chapters = info_dict.get('chapters', [])
    if chapters:
        print("Chapters:")
        for chapter in chapters:
            start_time = chapter['start_time']
            title = chapter['title']
            print(f"{title} (Starts at {start_time} seconds)")
    else:
        print("No chapters found.")
    
    # Save chapters to a JSON file
    title = title.replace(' ', '_')
    with open(f"youtube_dub/media/{title}_chapters.json", 'w') as f:
        json.dump(chapters, f, indent=4)

# Process each URL
def process_urls(urls):
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        for url in urls:
            info_dict = ydl.extract_info(url, download=False)
            title = info_dict['title'].replace(' ', '_')
            ydl.download([url])
            print_chapters(info_dict, info_dict['title'])
            split_audio_by_chapters(info_dict['title'])

if __name__ == "__main__":
    process_urls(URLS)

def split_audio_by_chapters(title):
    title = title.replace(' ', '_')
    audio = AudioSegment.from_file(f"youtube_dub/media/{title}.m4a", format="m4a")
    with open(f"youtube_dub/media/{title}_chapters.json", 'r') as f:
        chapters = json.load(f)
    
    if not os.path.exists(f"youtube_dub/media/{title}_chapters"):
        os.makedirs(f"youtube_dub/media/{title}_chapters")
    
    for i, chapter in enumerate(chapters):
        start_time = chapter['start_time'] * 1000  # pydub works in milliseconds
        end_time = chapters[i + 1]['start_time'] * 1000 if i + 1 < len(chapters) else len(audio)
        chapter_audio = audio[start_time:end_time]
        chapter_audio.export(f"youtube_dub/media/{title}_chapters/{chapter['title'].replace(' ', '_')}.m4a", format="m4a")

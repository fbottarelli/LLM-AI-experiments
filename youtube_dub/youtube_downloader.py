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
    'outtmpl': '%(title)s'.replace(' ', '_') + '.%(ext)s',  # Output filename template without spaces
}

# Function to extract and print chapter information
import json

def print_chapters(info_dict):
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
    title = info_dict['title'].replace(' ', '_')
    with open(f"{title}_chapters.json", 'w') as f:
        json.dump(chapters, f, indent=4)

# Process each URL
def process_urls(urls):
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        for url in urls:
            info_dict = ydl.extract_info(url, download=False)
            title = info_dict['title'].replace(' ', '_')
            ydl.params['outtmpl'] = f"{title}.%(ext)s"
            ydl.download([url])
            print_chapters(info_dict)

if __name__ == "__main__":
    process_urls(URLS)

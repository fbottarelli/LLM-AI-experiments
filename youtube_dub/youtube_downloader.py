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
    'outtmpl': '%(title)s.%(ext)s',  # Output filename template
}

# Function to extract and print chapter information
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

# Process each URL
def process_urls(urls):
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        for url in urls:
            info_dict = ydl.extract_info(url, download=True)
            print_chapters(info_dict)

if __name__ == "__main__":
    process_urls(URLS)

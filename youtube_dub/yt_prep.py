import os
import subprocess
from pytube import YouTube
from moviepy.editor import VideoFileClip
from pydub import AudioSegment
from pydub.utils import make_chunks

def check_pytube():
    try:
        subprocess.run(['pip', 'show', 'pytube'], check=True)
    except subprocess.CalledProcessError:
        print("pytube is not installed. Installing now...")
        subprocess.run(['pip', 'install', 'pytube'], check=True)
def download_youtube_video(url):
    try:
        yt = YouTube(url)
        stream = yt.streams.filter(file_extension='mp4').get_highest_resolution()
        video_title = yt.title
        print(f"Downloading {video_title}...")
        stream.download(filename=f"{video_title}.mp4")
        print(f"Downloaded {video_title} successfully.")
        return video_title
    except Exception as e:
        print(f"Download error: {e}")
        exit(1)

def extract_audio(video_title):
    video_path = f"{video_title}.mp4"
    audio_path = f"{video_title}.mp3"
    video = VideoFileClip(video_path)
    video.audio.write_audiofile(audio_path, bitrate='320k')
    os.remove(video_path)
    return audio_path

def split_audio(audio_path, chunk_length_ms=10000):
    audio = AudioSegment.from_mp3(audio_path)
    chunks = make_chunks(audio, chunk_length_ms)
    base_name = audio_path.rsplit('.', 1)[0]
    for i, chunk in enumerate(chunks):
        chunk_name = f"{base_name}_part{i+1}.mp3"
        chunk.export(chunk_name, format="mp3")
    os.remove(audio_path)

def main():
    check_pytube()
    url = input("Please enter the YouTube video URL: ")
    video_title = download_youtube_video(url)
    if video_title:
        audio_path = extract_audio(video_title)
        split_audio(audio_path)

if __name__ == "__main__":
    main()

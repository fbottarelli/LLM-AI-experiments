import os
import youtube_dl
from moviepy.editor import VideoFileClip
from pydub import AudioSegment
from pydub.utils import make_chunks
def download_youtube_video(url):
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': '%(title)s.%(ext)s',
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
        info_dict = ydl.extract_info(url, download=False)
        video_title = info_dict.get('title', None)
    return video_title

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
    url = input("Please enter the YouTube video URL: ")
    video_title = download_youtube_video(url)
    audio_path = extract_audio(video_title)
    split_audio(audio_path)

if __name__ == "__main__":
    main()

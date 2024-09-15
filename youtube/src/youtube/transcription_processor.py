import os
from openai import OpenAI
from dotenv import load_dotenv
import yt_dlp

# Load environment variables
load_dotenv()

def get_transcript(url):
    ydl_opts = {
        'writesubtitles': True,
        'writeautomaticsub': True,
        'subtitleslangs': ['en'],
        'skip_download': True,
        'outtmpl': '%(id)s.%(ext)s',
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        video_id = info['id']
        
    subtitle_filename = f"{video_id}.en.vtt"
    
    if os.path.exists(subtitle_filename):
        with open(subtitle_filename, 'r', encoding='utf-8') as f:
            transcript = f.read()
        os.remove(subtitle_filename)  # Clean up the file
        return transcript
    else:
        return "Transcript not available."

def process_transcript(transcript):
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv("OPENROUTER_API_KEY"),
    )

    prompt = f"""Summarize the following transcript and provide key points:

    {transcript[:4000]}  # Limiting to 4000 characters to avoid token limits

    Provide a concise summary and list the main topics discussed."""

    try:
        completion = client.chat.completions.create(
            extra_headers={
                "HTTP-Referer": "https://your-app-url.com",  # Replace with your app's URL
                "X-Title": "YouTubeTranscriptAnalyzer",  # Replace with your app's name
            },
            model="openai/gpt-4o-mini",  # You can change this to other models supported by OpenRouter
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes video transcripts."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500  # Adjust as needed
        )
        return completion.choices[0].message.content.strip()
    except Exception as e:
        return f"Error processing transcript: {str(e)}"

def get_and_process_transcript(url):
    transcript = get_transcript(url)
    if transcript != "Transcript not available.":
        return process_transcript(transcript)
    else:
        return "Transcript not available for processing."
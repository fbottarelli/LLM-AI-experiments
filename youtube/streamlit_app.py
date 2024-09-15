import streamlit as st
from src.youtube.youtube_downloader import download_audio, get_chapters, format_chapters
from src.youtube.transcription_processor import get_and_process_transcript

st.title("YouTube Audio Downloader and Analyzer")

url = st.text_input("Enter YouTube URL:")

col1, col2 = st.columns(2)

with col1:
    if st.button("Download Audio and Show Chapters"):
        if url:
            with st.spinner("Downloading audio..."):
                filename = download_audio(url)
            st.success(f"Audio downloaded: {filename}")

            with st.spinner("Fetching chapters..."):
                chapters = get_chapters(url)
            
            if chapters:
                st.subheader("Chapters:")
                st.text(format_chapters(chapters))
            else:
                st.info("No chapters found for this video.")
        else:
            st.warning("Please enter a YouTube URL.")

with col2:
    if st.button("Analyze Transcript"):
        if url:
            with st.spinner("Fetching and analyzing transcript..."):
                analysis = get_and_process_transcript(url)
            st.subheader("Transcript Analysis:")
            st.write(analysis)
        else:
            st.warning("Please enter a YouTube URL.")
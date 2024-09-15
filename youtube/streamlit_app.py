import streamlit as st
from youtube_downloader import download_audio, get_chapters, format_chapters

st.title("YouTube Audio Downloader and Chapter Viewer")

url = st.text_input("Enter YouTube URL:")

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
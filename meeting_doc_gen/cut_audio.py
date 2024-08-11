import subprocess

def cut_mp3(input_mp3, output_mp3, duration="00:05:00"):
    """Cuts an MP3 file to a specified duration.

    Args:
        input_mp3: Path to the input MP3 file.
        output_mp3: Path to the output MP3 file.
        duration: Duration to cut, in HH:MM:SS format (default is 10 minutes).
    """

    try:
        subprocess.run(
            [
                "ffmpeg",
                "-i", input_mp3,
                "-t", duration,  # Set the duration to cut
                "-acodec", "copy",  # Copy audio codec without re-encoding
                output_mp3
            ],
            check=True
        )
        print(f"Successfully cut '{input_mp3}' to '{output_mp3}' (first {duration})")

    except FileNotFoundError:
        print("Error: ffmpeg not found. Please install ffmpeg.")
    except subprocess.CalledProcessError as e:
        print(f"Error during cutting: {e}")


if __name__ == "__main__":
    input_file = "meeting_doc_gen/media/audio/output.mp3"  # Replace with your input MP3 file
    output_file = "meeting_doc_gen/media/audio/output_cutted.mp3" 
    cut_mp3(input_file, output_file)
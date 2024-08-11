import subprocess

def convert_mkv_to_mp3(mkv_file, mp3_file):
    """Converts an MKV file to an MP3 file.

    Args:
        mkv_file: Path to the input MKV file.
        mp3_file: Path to the output MP3 file.
    """

    try:
        # Use ffmpeg to extract audio and convert to MP3
        subprocess.run(
            [
                "ffmpeg",
                "-i", mkv_file,
                "-vn",  # Disable video recording
                "-acodec", "libmp3lame",  # Use libmp3lame encoder
                "-ab", "192k",  # Set audio bitrate (adjust as needed)
                mp3_file
            ],
            check=True  # Raise an exception if ffmpeg fails
        )
        print(f"Successfully converted '{mkv_file}' to '{mp3_file}'")

    except FileNotFoundError:
        print("Error: ffmpeg not found. Please install ffmpeg.")
    except subprocess.CalledProcessError as e:
        print(f"Error during conversion: {e}")


if __name__ == "__main__":
    input_mkv = "/home/fd/repo/AI/generativeai/meeting_doc_gen/video/2024-08-09 12-27-11.mkv"  # Replace with your input MKV file
    output_mp3 = "output.mp3"  # Replace with your desired output MP3 file
    convert_mkv_to_mp3(input_mkv, output_mp3)
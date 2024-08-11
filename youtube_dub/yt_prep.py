
import vertexai
from vertexai.generative_models import GenerativeModel, Part

# TODO(developer): Update and un-comment below lines
# project_id = "PROJECT_ID"

vertexai.init(project=project_id, location=location)

model = GenerativeModel("gemini-1.5-flash-001")

prompt = 
audio_file_path = "media/gemini/media/filename.mp3"

# Read the audio file in binary mode
with open(audio_file_path, "rb") as audio_file:
    audio_bytes = audio_file.read()

audio_part = Part.from_data(audio_bytes, mime_type="audio/mp3")

contents = [audio_part, prompt]

# Counts tokens
print(model.count_tokens(contents))
response = model.generate_content(contents)
print(response.text)

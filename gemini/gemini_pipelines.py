import os
import vertexai
from vertexai.generative_models import GenerativeModel, Part
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

project_id = os.getenv("gemini_project_id")
location = os.getenv("gemini_location")

# Initialize Vertex AI
vertexai.init(project=project_id, location=location)

def text_understanding(input_text):
    model = GenerativeModel("gemini-1.5-pro-001")
    response = model.generate_content(
        f"Summarize: {input_text}, I want a very brief list of the techniques and an obsidian link to the specific technique, the obsidian link should start with RAG - "
    )
    return response.text

def document_understanding(pdf_file_path):
    model = GenerativeModel(model_name='gemini-1.5-pro-001')
    
    with open(pdf_file_path, "rb") as file:
        pdf_bytes = file.read()
    
    pdf = Part.from_data(pdf_bytes, mime_type="application/pdf")
    prompt = "What is shown in this document?"
    contents = [pdf, prompt]
    
    response = model.generate_content(contents)
    return response.text

def image_understanding(image_uri):
    model = GenerativeModel("gemini-1.5-flash-001")
    response = model.generate_content(
        [
            Part.from_uri(image_uri, mime_type="image/jpeg"),
            "What is shown in this image?",
        ]
    )
    return response.text

def audio_integration(audio_file_path, prompt):
    model = GenerativeModel("gemini-1.5-flash-001")
    
    with open(audio_file_path, "rb") as audio_file:
        audio_bytes = audio_file.read()
    
    audio_part = Part.from_data(audio_bytes, mime_type="audio/mp3")
    contents = [audio_part, prompt]
    
    response = model.generate_content(contents)
    return response.text

def video_integration(video_file_path, prompt):
    model = GenerativeModel("gemini-1.5-pro-001")
    
    with open(video_file_path, "rb") as video_file:
        video_bytes = video_file.read()
    
    video_part = Part.from_data(video_bytes, mime_type="video/mp4")
    contents = [video_part, prompt]
    
    response = model.generate_content(contents)
    return response.text


if __name__ == "__main__":
    basic_text = True
    python_script = False
    doc_pdf = False
    image_uri = False
    audio_integration = False
    video_integration = False
    if basic_text:
        # Test text understanding
        # ask the user for input text
        text_input = ""
        if text_input == "":
            text_input = input("Enter your input text: ")
        print("Text Understanding Result:")
        print(text_understanding(text_input))
        print("\n" + "="*50 + "\n")
    if python_script:
        # Test python script understanding
        python_script_path = "../other_repo/kotaemon/libs/ktem/ktem/pages/chat/__init__.py"
        if python_script_path == "":
            python_script_path = input("Enter your python script path: ")
        with open(python_script_path, "r") as file:
            python_text = file.read()
        print("Python Script Understanding Result:")
        print(text_understanding(python_text))
        print("\n" + "="*50 + "\n")
    if doc_pdf:
        # Test document understanding
        pdf_path = "path/to/your/document.pdf"
        print("Document Understanding Result:")
        print(document_understanding(pdf_path))
        print("\n" + "="*50 + "\n")
    if image_uri:
        # Test image understanding
        image_uri = "gs://cloud-samples-data/generative-ai/image/scones.jpg"
        print("Image Understanding Result:")
        print(image_understanding(image_uri))
        print("\n" + "="*50 + "\n")
    if audio_integration:
        # Test audio integration
        audio_path = "path/to/your/audio.mp3"
        audio_prompt = "Transcribe and summarize this audio"
        print("Audio Integration Result:")
        print(audio_integration(audio_path, audio_prompt))
        print("\n" + "="*50 + "\n")
    if video_integration:
        # Test video integration
        video_path = "path/to/your/video.mp4"
        video_prompt = "Summarize the content of this video"
        print("Video Integration Result:")
        print(video_integration(video_path, video_prompt))
    else:
        print("No supported pipeline selected")
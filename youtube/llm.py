import vertexai
from vertexai.generative_models import GenerativeModel
from youtube.prompt import get_prompt
import os
from dotenv import load_dotenv


load_dotenv()
project_id = os.getenv("gemini_project_id")
location = os.getenv("gemini_location")

def title_extractor(title):

    vertexai.init(project=project_id, location="us-central1")
    model = GenerativeModel("gemini-1.5-flash-001")

    title_extractor_prompt = get_prompt("title_extractor", youtube_title=title)
    response = model.generate_content(title_extractor_prompt)

    return response.text
import openai
from dotenv import load_dotenv
import obsidian_sorter.tags as tags

load_dotenv()  # Load environment variables from .env file

def find_tag(note_path):
    with open(note_path, 'r', encoding='utf-8') as file:
        first_line = file.readline().strip()
    if first_line.startswith('# '):
        return first_line[2:]
    return None


openai.api_key = os.getenv("OPENAI_API_KEY")

def classify_with_gpt(content_excerpt, predefined_topics):
    prompt = f"Classifica il seguente testo in uno dei seguenti argomenti: {', '.join(predefined_topics)}.\n\nTesto: {content_excerpt}"
    response = openai.Completion.create(
        engine="gpt-4o-mini",
        prompt=prompt,
        max_tokens=50,
        n=1,
        stop=None,
        temperature=0.7
    )
    classification = response.choices[0].text.strip()
    return classification

import os
import shutil

def process_notes(base_dir, predefined_topics, log_file_path):
    with open(log_file_path, 'w', encoding='utf-8') as log_file:
        for root, _, files in os.walk(base_dir):
            for file in files:
                if file.endswith('.md'):
                    note_path = os.path.join(root, file)
                    log_file.write(f"Processing: {note_path}\n")
                    
                    # Usa la prima parte della nota per la classificazione
                    with open(note_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    excerpt_length = 200  # puoi variare questa lunghezza a seconda delle tue esigenze
                    content_excerpt = content[:excerpt_length]

                    # Classifica usando ChatGPT
                    tag = classify_with_gpt(content_excerpt, predefined_topics)
                    log_file.write(f"Classified as: {tag}\n")

                    # Aggiungi il tag alla nota
                    add_tag(note_path, tag)
                    
                    # Sposta la nota nella cartella appropriata
                    target_directory = os.path.join(base_dir, tag)
                    os.makedirs(target_directory, exist_ok=True)
                    shutil.move(note_path, os.path.join(target_directory, file))

if __name__ == "__main__":
    base_directory = os.getenv('OBSIDIAN_VAULT_PATH')
    if not base_directory:
        raise ValueError("OBSIDIAN_VAULT_PATH not set in .env file")
    
    predefined_topics = ["knowledge", "life space", "work and study", "any other category"]  # Add your categories here
    log_file_path = os.path.join(base_directory, 'organizzazione_note.log')
    process_notes(base_directory, predefined_topics, log_file_path)
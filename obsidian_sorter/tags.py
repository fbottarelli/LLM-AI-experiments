import os
import litellm
from dotenv import load_dotenv
import yaml
import streamlit as st

# Load environment variables
load_dotenv()

def classify_and_tag(note_path):
    """Classifies the content of a note and tags it with one or more genres."""
    # List of topics with hierarchical structure
    genres = {
        "Technology": {
            "AI": ["aigen", "llm", "machine_learning", "deep_learning", "nlp", "optimization", "generative_ai", "chatgpt", "openai", "code_assistant", "ai_agent"],
            "Cloud": ["iac", "aws", "cloud", "modern_applications"],
            "Software_Development": ["api", "coding", "webdev", "desktop_dev", "mobile_dev"],
            "Data_Science": {
                "Statistics": ["descriptive_statistics", "inferential_statistics", "probability", "statistics", "generalized_linear_models", "time_series"],
                "Data_Analysis": ["tableau"],
                "Database": ["database", "datastream", "information_retrieval", "nosql", "sql"],
            },
            "Cybersecurity": ["cybersecurity"],
            "Electronics": ["electronics", "microcontroller", "raspberry_pi", "arduino"],
        },
        "Knowledge_and_Research": {
            "Languages": ["english_language"],
            "History": ["storia", "olanda"],
            "General_Knowledge": ["knowledge"],
        },
        "Work": ["work", "Miriade", "Miriade_AI"],
        "Personal": ["personal", "linkedin", "article", "book", "streamer", "holiday", "health"],
    }

    # Create a flattened representation of genres for the prompt
    flattened_genres = []
    for main_category, subcategories in genres.items():
        flattened_genres.append(main_category)
        if isinstance(subcategories, dict):
            for subcategory, items in subcategories.items():
                flattened_genres.append(f"{main_category}/{subcategory}")
                if isinstance(items, list):
                    for item in items:
                        flattened_genres.append(f"{main_category}/{subcategory}/{item}")
                elif isinstance(items, dict):
                    for subsubcategory, subitems in items.items():
                        flattened_genres.append(f"{main_category}/{subcategory}/{subsubcategory}")
                        for subitem in subitems:
                            flattened_genres.append(f"{main_category}/{subcategory}/{subsubcategory}/{subitem}")
        elif isinstance(subcategories, list):
            for item in subcategories:
                flattened_genres.append(f"{main_category}/{item}")

    # Create a lowercase version of flattened_genres for case-insensitive comparison
    lowercase_genres = [genre.lower() for genre in flattened_genres]

    with open(note_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Prepare the messages for the chat completion API
    messages = [
        {"role": "system", "content": f"""You are a classifier that categorizes text into one or more hierarchical genres. 
        The available genres are: {', '.join(flattened_genres)}. 
        Respond with the most relevant genre names, separated by commas. 
        Start with the main categories and provide more specific subcategories if applicable. 
        For example: 'Technology, Technology/AI, Technology/AI/machine_learning'. 
        If the text is not related to any of the genres, respond with 'miscellaneous'."""},
        {"role": "user", "content": f"Classify the following text:\n\n{content[:4000]}"}
    ]

    # Choose the model you want to use
    model_name = "openai/gpt-4o-mini"  # Replace with "anthropic/claude-v1" or "google/gemini-1.5-pro-001" as needed

    try:
        response = litellm.completion(
            model=model_name,
            messages=messages,
            max_tokens=100  # Adjust as needed
        )
        classified_genres = response.choices[0].message.content.strip().lower().split(',')
        classified_genres = [genre.strip() for genre in classified_genres]
    except Exception as e:
        print(f"Error during classification: {str(e)}")
        classified_genres = ["miscellaneous"]

    # Ensure the classified genres are in our predefined list (case-insensitive)
    valid_classified_genres = []
    for genre in classified_genres:
        if genre in lowercase_genres:
            index = lowercase_genres.index(genre)
            valid_classified_genres.append(flattened_genres[index])
        else:
            print(f"Warning: Classified genre '{genre}' not in predefined list.")

    if not valid_classified_genres:
        print(f"Warning: No valid genres found. Defaulting to 'miscellaneous'.")
        valid_classified_genres = ["miscellaneous"]
    else:
        # Remove 'miscellaneous' if other valid genres are present
        valid_classified_genres = [genre for genre in valid_classified_genres if genre.lower() != "miscellaneous"]

    # Get existing tags
    existing_tags = list_tags(note_path)

    # Remove existing genre tags
    non_genre_tags = [tag for tag in existing_tags if tag.lower() not in lowercase_genres]

    # Combine non-genre tags with new genre tags
    all_tags = set(non_genre_tags + valid_classified_genres)

    # Add the genre tags to the file
    add_tags(note_path, all_tags)
    print(f"File '{note_path}' classified as '{', '.join(valid_classified_genres)}' and tagged accordingly.")

def add_tags(note_path, tags):
    """Replaces all tags in the note's YAML front matter with the specified tags."""
    with open(note_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check if there's a YAML front matter
    if content.startswith('---'):
        end_of_yaml = content.find('---', 3)
        if end_of_yaml != -1:
            yaml_content = content[3:end_of_yaml]
            rest_of_content = content[end_of_yaml+3:]

            try:
                # Parse existing YAML content
                yaml_data = yaml.safe_load(yaml_content)
                if not isinstance(yaml_data, dict):
                    yaml_data = {}
            except yaml.YAMLError:
                yaml_data = {}

            # Replace existing tags with new tags
            yaml_data['tags'] = sorted(tags)
            updated_yaml_content = yaml.dump(yaml_data, sort_keys=False)

            updated_content = f'---\n{updated_yaml_content}---\n{rest_of_content}'
        else:
            # If YAML is not properly closed, treat as no YAML
            updated_content = create_yaml_front_matter(tags, content)
    else:
        # If no YAML, add it
        updated_content = create_yaml_front_matter(tags, content)

    with open(note_path, 'w', encoding='utf-8') as f:
        f.write(updated_content)

def add_tags(note_path, tags):
    """Replaces all tags in the note's YAML front matter with the specified tags."""
    with open(note_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check if there's a YAML front matter
    if content.startswith('---'):
        end_of_yaml = content.find('---', 3)
        if end_of_yaml != -1:
            yaml_content = content[3:end_of_yaml]
            rest_of_content = content[end_of_yaml+3:]

            try:
                # Parse existing YAML content
                yaml_data = yaml.safe_load(yaml_content)
                if not isinstance(yaml_data, dict):
                    yaml_data = {}
            except yaml.YAMLError:
                yaml_data = {}

            # Replace existing tags with new tags
            yaml_data['tags'] = sorted(tags)
            updated_yaml_content = yaml.dump(yaml_data, sort_keys=False)

            updated_content = f'---\n{updated_yaml_content}---\n{rest_of_content}'
        else:
            # If YAML is not properly closed, treat as no YAML
            updated_content = create_yaml_front_matter(tags, content)
    else:
        # If no YAML, add it
        updated_content = create_yaml_front_matter(tags, content)

    with open(note_path, 'w', encoding='utf-8') as f:
        f.write(updated_content)

def create_yaml_front_matter(tags, content):
    """Creates YAML front matter with the given tags."""
    yaml_data = {'tags': sorted(tags)}
    try:
        yaml_content = yaml.dump(yaml_data, sort_keys=False)
        updated_content = f'---\n{yaml_content}---\n\n{content}'
    except yaml.YAMLError as e:
        print(f"Error creating YAML front matter: {e}")
        updated_content = content
    return updated_content

def list_tags(note_path):
    """Lists all tags present in the note's YAML front matter."""
    with open(note_path, 'r', encoding='utf-8') as f:
        content = f.read()

    tags = []

    # Check for tags in YAML front matter
    if content.startswith('---'):
        end_of_yaml = content.find('---', 3)
        if end_of_yaml != -1:
            yaml_content = content[3:end_of_yaml]
            try:
                # Parse YAML content
                yaml_data = yaml.safe_load(yaml_content)
                if isinstance(yaml_data, dict) and 'tags' in yaml_data:
                    existing_tags = yaml_data['tags']
                    if isinstance(existing_tags, list):
                        tags = existing_tags
                    else:
                        tags = [existing_tags]
            except yaml.YAMLError as e:
                print(f"Error parsing YAML in {note_path}: {e}")
    return tags

def remove_tag(note_path, tag):
    """Removes a specified tag from the note's YAML front matter."""
    with open(note_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check if there's a YAML front matter
    if content.startswith('---'):
        end_of_yaml = content.find('---', 3)
        if end_of_yaml != -1:
            yaml_content = content[:end_of_yaml+3]
            rest_of_content = content[end_of_yaml+3:]

            # Parse existing YAML content
            yaml_data = yaml.safe_load(yaml_content)
            if 'tags' in yaml_data:
                existing_tags = yaml_data['tags']
                if isinstance(existing_tags, list):
                    updated_tags = [t for t in existing_tags if t != tag]
                else:
                    updated_tags = [] if yaml_data['tags'] == tag else [yaml_data['tags']]

                yaml_data['tags'] = updated_tags
                updated_yaml_content = yaml.dump(yaml_data, sort_keys=False)
                updated_content = f'---\n{updated_yaml_content}---\n{rest_of_content}'

                with open(note_path, 'w', encoding='utf-8') as f:
                    f.write(updated_content)

def update_tag(note_path, old_tag, new_tag):
    """Updates an existing tag in the note's YAML front matter."""
    with open(note_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check if there's a YAML front matter
    if content.startswith('---'):
        end_of_yaml = content.find('---', 3)
        if end_of_yaml != -1:
            yaml_content = content[:end_of_yaml+3]
            rest_of_content = content[end_of_yaml+3:]

            # Parse existing YAML content
            yaml_data = yaml.safe_load(yaml_content)
            if 'tags' in yaml_data:
                existing_tags = yaml_data['tags']
                if isinstance(existing_tags, list):
                    updated_tags = [new_tag if t == old_tag else t for t in existing_tags]
                else:
                    updated_tags = [new_tag] if yaml_data['tags'] == old_tag else [yaml_data['tags']]

                yaml_data['tags'] = updated_tags
                updated_yaml_content = yaml.dump(yaml_data, sort_keys=False)
                updated_content = f'---\n{updated_yaml_content}---\n{rest_of_content}'

                with open(note_path, 'w', encoding='utf-8') as f:
                    f.write(updated_content)

def process_file(file_path):
    """Processes a single markdown file, classifying and tagging it."""
    classify_and_tag(file_path)

def get_all_tags(directory_path):
    """Returns a list of all unique tags in the specified directory."""
    all_tags = set()
    for root, _, files in os.walk(directory_path):
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                all_tags.update(list_tags(file_path))
    return sorted(list(all_tags))
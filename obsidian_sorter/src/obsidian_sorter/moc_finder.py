import os
from dotenv import load_dotenv
import vertexai
from vertexai.generative_models import GenerativeModel

def find_moc_files(base_dir):
    moc_files = []
    for root, _, files in os.walk(base_dir):
        for file in files:
            if file.endswith('.md') and ('MOC' in file or 'moc' in file):
                moc_files.append(os.path.join(root, file))
    return moc_files

def split_list(lst, n):
    """Split a list into sublists of approximately equal length."""
    k, m = divmod(len(lst), n)
    return [lst[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(n)]

def get_categories(moc_names, model):
    prompt = f"""Given the following list of MOC (Map of Content) file names, create a list of 10-15 broad, general categories that these MOCs could be grouped into. Follow these guidelines:

1. Categories should be broad and encompass multiple MOCs.
2. Use consistent formatting (e.g., title case for all categories).
3. Avoid duplicates or very similar categories.
4. Do not use bullet points, numbers, or any other prefixes.
5. Each category should be on a new line.
6. Do not include any explanations or additional text.

MOC file names:
{', '.join(moc_names)}

Categories:"""
    
    response = model.generate_content(prompt)
    return [category.strip() for category in response.text.strip().split('\n') if category.strip()]

if __name__ == "__main__":
    load_dotenv()  # Load environment variables from .env file
    base_directory = os.getenv('OBSIDIAN_VAULT_PATH')
    
    if not base_directory:
        raise ValueError("OBSIDIAN_VAULT_PATH not set in .env file")
    
    moc_files = find_moc_files(base_directory)
    moc_names = [os.path.splitext(os.path.basename(file))[0] for file in moc_files]

    # Initialize Vertex AI
    project_id = "geminitesting-432015"  # Replace with your actual project ID
    location = "europe-west1"  # Adjust if needed
    vertexai.init(project=project_id, location=location)

    # Initialize the generative model
    model = GenerativeModel("gemini-1.5-flash-001")

    # Split the MOC names into sublists (e.g., 5 sublists)
    moc_sublists = split_list(moc_names, 5)

    all_categories = set()
    for sublist in moc_sublists:
        categories = get_categories(sublist, model)
        all_categories.update(categories)

    # Write results to files
    with open('data/moc_files_list.txt', 'w') as f:
        f.write(f"Found {len(moc_files)} MOC files:\n")
        for file in moc_files:
            f.write(f"{file}\n")

    with open('data/moc_categories.txt', 'w') as f:
        f.write("MOC Categories:\n")
        for category in sorted(all_categories):
            f.write(f"{category}\n")

    print(f"Found {len(moc_files)} MOC files. Results saved to 'data/moc_files_list.txt'")
    print(f"Generated {len(all_categories)} categories. Results saved to 'data/moc_categories.txt'")
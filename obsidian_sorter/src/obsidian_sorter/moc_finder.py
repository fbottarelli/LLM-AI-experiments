import os
from dotenv import load_dotenv

def find_moc_files(base_dir):
    moc_files = []
    for root, _, files in os.walk(base_dir):
        for file in files:
            if file.endswith('.md') and ('MOC' in file or 'moc' in file):
                moc_files.append(os.path.join(root, file))
    return moc_files

if __name__ == "__main__":
    load_dotenv()  # Load environment variables from .env file
    base_directory = os.getenv('OBSIDIAN_VAULT_PATH')
    
    if not base_directory:
        raise ValueError("OBSIDIAN_VAULT_PATH not set in .env file")
    
    moc_files = find_moc_files(base_directory)
    
    with open('moc_files_list.txt', 'w') as f:
        f.write(f"Found {len(moc_files)} MOC files:\n")
        for file in moc_files:
            f.write(f"{file}\n")
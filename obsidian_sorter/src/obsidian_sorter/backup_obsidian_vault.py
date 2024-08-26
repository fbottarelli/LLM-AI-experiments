import os
import tarfile
from datetime import datetime
from dotenv import load_dotenv

def backup_obsidian_vault(vault_path, backup_dir):
    # Ensure the backup directory exists
    os.makedirs(backup_dir, exist_ok=True)

    # Create a timestamp for the backup file name
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_filename = f"obsidian_vault_backup_{timestamp}.tar.gz"
    backup_path = os.path.join(backup_dir, backup_filename)

    print(f"Starting backup of Obsidian vault: {vault_path}")
    print(f"Backup will be saved to: {backup_path}")

    # Create the tar.gz archive
    with tarfile.open(backup_path, "w:gz") as tar:
        total_files = sum([len(files) for _, _, files in os.walk(vault_path)])
        processed_files = 0

        for root, dirs, files in os.walk(vault_path):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, start=os.path.dirname(vault_path))
                tar.add(file_path, arcname=arcname)
                processed_files += 1
                print(f"Compressing: {arcname} ({processed_files}/{total_files})")

    print(f"Backup completed successfully: {backup_path}")
    print(f"Total files compressed: {total_files}")

if __name__ == "__main__":
    load_dotenv()  # Load environment variables from .env file
    vault_path = os.getenv('OBSIDIAN_VAULT_PATH')
    backup_dir = '/home/fd/temp/vault_backups'
    
    if not vault_path:
        raise ValueError("OBSIDIAN_VAULT_PATH not set in .env file")
    
    backup_obsidian_vault(vault_path, backup_dir)
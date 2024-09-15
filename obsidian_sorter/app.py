import streamlit as st
import os
import json
from collections import Counter
from tags import process_file, get_all_tags, remove_tag, update_tag, list_tags
import zipfile
from datetime import datetime
import yaml

def generate_tag_statistics(directory_path):
    """Generates tag statistics for all markdown files in the directory."""
    tag_counts = Counter()
    file_counts = Counter()
    total_files = 0

    for root, _, files in os.walk(directory_path):
        for file in files:
            if file.endswith('.md'):
                total_files += 1
                file_path = os.path.join(root, file)
                tags = list_tags(file_path)
                tag_counts.update(tags)
                file_counts.update([len(tags)])

    stats = {
        "total_files": total_files,
        "total_unique_tags": len(tag_counts),
        "top_tags": dict(tag_counts.most_common(10)),
        "avg_tags_per_file": sum(file_counts.elements()) / total_files if total_files > 0 else 0,
        "files_without_tags": file_counts[0],
        "tag_distribution": dict(file_counts)
    }

    return stats  # Return only the stats dictionary

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
                    elif isinstance(existing_tags, str):
                        tags = [existing_tags]
            except yaml.YAMLError as e:
                print(f"Error parsing YAML in {note_path}: {e}")
    return tags

def display_tag_statistics(stats):
    """Displays tag statistics in the Streamlit app."""
    st.subheader("Tag Statistics Dashboard")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Files", stats["total_files"])
    col2.metric("Unique Tags", stats["total_unique_tags"])
    col3.metric("Avg Tags per File", f"{stats['avg_tags_per_file']:.2f}")

    st.subheader("Top 10 Tags")
    st.bar_chart(stats["top_tags"])

    st.subheader("Tag Distribution")
    distribution = {f"{k} tags": v for k, v in stats["tag_distribution"].items()}
    st.bar_chart(distribution)

    st.metric("Files without Tags", stats["files_without_tags"])

def get_markdown_files(directory_path):
    """Returns a list of all markdown files in the directory and its subdirectories."""
    markdown_files = []
    for root, _, files in os.walk(directory_path):
        for file in files:
            if file.endswith('.md'):
                markdown_files.append(os.path.join(root, file))
    return markdown_files

def create_backup(directory_path):
    """Creates a zip backup of the specified directory."""
    parent_dir = os.path.dirname(directory_path)
    folder_name = os.path.basename(directory_path)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    zip_filename = f"{folder_name}_backup_{timestamp}.zip"
    zip_path = os.path.join(parent_dir, zip_filename)

    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(directory_path):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, directory_path)
                zipf.write(file_path, arcname)

    return zip_path

def main():
    st.title("Obsidian Note Tagger")

    # Input for directory path
    directory_path = st.text_input("Enter the directory path containing markdown files:")

    if directory_path and os.path.isdir(directory_path):
        # Create a placeholder for the log window
        log_window = st.empty()

        # Function to update the log window
        def update_log(message):
            log_window.text_area("Operation Log", message, height=200)

        # Generate tag statistics
        stats = generate_tag_statistics(directory_path)

        # Display tag statistics
        st.subheader("Tag Statistics Dashboard")
        display_tag_statistics(stats)

        # Add a button to update statistics manually
        if st.button("Update Statistics"):
            update_log("Updating statistics...")
            stats = generate_tag_statistics(directory_path)
            display_tag_statistics(stats)
            update_log("Statistics updated successfully.")

        # Process single file or folder
        st.subheader("Process Single File or Folder")
        selected_path = st.text_input("Enter a file path or folder path to process:")
        if st.button("Process File/Folder"):
            if os.path.isfile(selected_path):
                update_log(f"Processing file: {selected_path}")
                process_file(selected_path)
                update_log(f"Processed file: {selected_path}")
            elif os.path.isdir(selected_path):
                files_processed = 0
                for file_path in get_markdown_files(selected_path):
                    update_log(f"Processing file: {file_path}")
                    process_file(file_path)
                    files_processed += 1
                update_log(f"Processed {files_processed} files in the directory and its subdirectories")
            else:
                update_log("Invalid file or folder path")

        # Process all files
        st.subheader("Process All Files")
        if st.button("Process All Files"):
            files_processed = 0
            for file_path in get_markdown_files(directory_path):
                update_log(f"Processing file: {file_path}")
                process_file(file_path)
                files_processed += 1
            update_log(f"Processed {files_processed} files in the directory and its subdirectories")

        # Process files without tags
        st.subheader("Process Files Without Tags")
        if st.button("Process Files Without Tags"):
            files_processed = 0
            for file_path in get_markdown_files(directory_path):
                if not list_tags(file_path):
                    update_log(f"Processing file without tags: {file_path}")
                    process_file(file_path)
                    files_processed += 1
            update_log(f"Processed {files_processed} files without tags")

        # Tag management
        st.subheader("Tag Management")
        all_tags = get_all_tags(directory_path)

        # Remove tag
        tag_to_remove = st.selectbox("Select a tag to remove", all_tags)
        if st.button("Remove Tag"):
            files_updated = 0
            for file_path in get_markdown_files(directory_path):
                if remove_tag(file_path, tag_to_remove):
                    files_updated += 1
                    update_log(f"Removed tag '{tag_to_remove}' from {file_path}")
            update_log(f"Removed tag '{tag_to_remove}' from {files_updated} files")

        # Update tag
        old_tag = st.selectbox("Select a tag to update", all_tags)
        new_tag = st.text_input("Enter the new tag name")
        if st.button("Update Tag"):
            files_updated = 0
            for file_path in get_markdown_files(directory_path):
                if update_tag(file_path, old_tag, new_tag):
                    files_updated += 1
                    update_log(f"Updated tag '{old_tag}' to '{new_tag}' in {file_path}")
            update_log(f"Updated tag '{old_tag}' to '{new_tag}' in {files_updated} files")

        # Backup system
        st.subheader("Backup System")
        if st.button("Create Backup"):
            update_log("Creating backup...")
            backup_path = create_backup(directory_path)
            update_log(f"Backup created successfully: {backup_path}")

    else:
        st.warning("Please enter a valid directory path")

if __name__ == "__main__":
    main()
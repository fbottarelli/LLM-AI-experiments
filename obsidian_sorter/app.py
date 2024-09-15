import streamlit as st
import os
from tags import process_file, get_all_tags, remove_tag, update_tag

def main():
    st.title("Obsidian Note Tagger")

    # Input for directory path
    directory_path = st.text_input("Enter the directory path containing markdown files:")

    if directory_path and os.path.isdir(directory_path):
        # Process single file
        st.subheader("Process Single File")
        files = [f for f in os.listdir(directory_path) if f.endswith('.md')]
        selected_file = st.selectbox("Select a file to process", files)
        if st.button("Process File"):
            file_path = os.path.join(directory_path, selected_file)
            process_file(file_path)
            st.success(f"Processed file: {selected_file}")

        # Process all files
        st.subheader("Process All Files")
        if st.button("Process All Files"):
            for file in files:
                file_path = os.path.join(directory_path, file)
                process_file(file_path)
            st.success("Processed all files in the directory")

        # Tag management
        st.subheader("Tag Management")
        all_tags = get_all_tags(directory_path)

        # Remove tag
        tag_to_remove = st.selectbox("Select a tag to remove", all_tags)
        if st.button("Remove Tag"):
            for file in files:
                file_path = os.path.join(directory_path, file)
                remove_tag(file_path, tag_to_remove)
            st.success(f"Removed tag '{tag_to_remove}' from all files")

        # Update tag
        old_tag = st.selectbox("Select a tag to update", all_tags)
        new_tag = st.text_input("Enter the new tag name")
        if st.button("Update Tag"):
            for file in files:
                file_path = os.path.join(directory_path, file)
                update_tag(file_path, old_tag, new_tag)
            st.success(f"Updated tag '{old_tag}' to '{new_tag}' in all files")

    else:
        st.warning("Please enter a valid directory path")

if __name__ == "__main__":
    main()
import streamlit as st
from blood_analysis.data_extraction import process_images

# Set the title of the app
st.title("Blood Test Image Processor")

# Input for directory
directory = st.text_input("Enter the directory of images:")

# Input for test name list
test_name_list = st.text_input("Enter test names (comma-separated):")

# Button to submit the request
if st.button("Process Images"):
    if directory and test_name_list:
        test_name_list = [name.strip() for name in test_name_list.split(",")]
        results = process_images(directory, test_name_list)
        st.success("Images processed successfully!")
        for result in results:
            st.write(result)
    else:
        st.warning("Please fill in all fields.")
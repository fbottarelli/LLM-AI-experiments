

########################################################
########################################################
### TXT
def extract_txt(txt_path: str, chunk: bool = False):
    """
    Extracts text from a local plain text file.

    Parameters:
    txt_path (str): The path to the text file from which to extract text.

    Returns:
    str: The extracted text from the file.
    """
    with open(txt_path, "r") as file:
        text = file.read()
    return text

def extract_md(md_path: str, chunk: bool = False):
    """
    Extracts text from a local markdown file.

    Parameters:
    md_path (str): The path to the markdown file from which to extract text.

    Returns:
    str: The extracted text from the file.
    """
    with open(md_path, "r") as file:
        text = file.read()
    return text

########################################################
########################################################
### PDF
from pypdf import PdfReader


def extract_pdf(pdf_path: str, chunk: bool = False):
    """
    Extracts text from a PDF file located on the local filesystem.

    Parameters:
    pdf_path (str): The path to the PDF file from which to extract text.

    Returns:
    str: The extracted text from the PDF file.
    """
    text = ""
    with open(pdf_path, 'rb') as file:
        reader = PdfReader(pdf_path)
        for page in reader.pages:
            text += page.extract_text()
    return text


from pdf2image import convert_from_path

def pdf_to_image(pdf_path: str):

    # Set poppler path
    images = convert_from_path(pdf_path, fmt='jpeg')
    
    for i, image in enumerate(images):
        image_key = f"{pdf_path}_page_{i+1}.jpg"
        image.save(image_key, format='JPEG')

    return f"PDF document ({pdf_path}) successfully converted to a series of images."

########################################################
########################################################
### DOCX

########################################################
########################################################
### PNG/JPEG
import base64
# Function to encode the image
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')



########################################################
########################################################
### GATEWAY

def gateway_ingestion_streamlit(file: UploadedFile, chunk: bool = False):
    """
    Choose the right function to extract text from the file by its extension.
    """
    if file.endswith(".txt"):
        return extract_txt(file)
    elif file.endswith(".pdf"):
        return extract_pdf(file)
    elif file.endswith(".md"):
        return extract_md(file)
    elif file.endswith(".jpeg") or file.endswith(".png"):
        return encode_image(file)
    else:
        raise ValueError("Unsupported file type")


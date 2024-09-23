

########################################################
########################################################
### TXT
def extract_txt(txt_path: str):
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

########################################################
########################################################
### PDF
from pypdf import PdfReader


def extract_pdf(pdf_path: str):
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
### GATEWAY
def gateway_ingestion(file: str):
    """
    Choose the right function to extract text from the file by its extension.
    """
    if file.endswith(".txt"):
        return extract_text_local(file)
    elif file.endswith(".pdf"):
        return extract_pdf_local(file)
    else:
        raise ValueError("Unsupported file type")


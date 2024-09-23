import boto3
from langchain_text_splitters import RecursiveCharacterTextSplitter
import re


def preprocess_text(input_text, patterns):
    """
    Apply a series of regex substitutions to the input text.

    This function iterates over a list of pattern-replacement pairs and applies
    them to the input text using regular expressions. This is useful for cleaning
    or preprocessing text by removing or replacing certain patterns.

    Parameters:
    - input_text (str): The text to be processed.
    - patterns (list of tuples): A list where each tuple contains a pattern to
      search for and the replacement string. For example, [(r'\s+', ' '), (r'\.', '')]
      would replace all sequences of whitespace with a single space and remove all periods.

    Returns:
    - str: The processed text after all replacements have been applied.
    """
    for pattern in patterns:
        input_text = re.sub(pattern[0], pattern[1], input_text)
    return input_text

def split_text(input_text, input_metadata):
    """
    Split the input text into smaller chunks based on specified size and overlap.

    This function uses a RecursiveCharacterTextSplitter instance to divide the input
    text into smaller parts. Each part is then packaged into a dictionary with its corresponding metadata.

    Parameters:
    - input_text (str): The text to be split.
    - input_metadata (dict): Metadata associated with the input text. This metadata
      is attached to each chunk of the split text.

    Returns:
    - list of dicts: A list where each element is a dictionary containing a chunk of
      the split text and its associated metadata.
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1500,
        chunk_overlap=200,
        length_function=len
    )
    text_splitted = text_splitter.split_text(input_text)
    dict_splitted = [{"page_content": chunk, "metadata": input_metadata} for chunk in text_splitted]
    return dict_splitted
import os
import hashlib
from PyPDF2 import PdfReader

def allowed_file(filename, allowed_extensions):
    """
    Check if the file has an allowed extension.

    :param filename: Name of the file
    :param allowed_extensions: Set of allowed file extensions
    :return: Boolean indicating whether the file is allowed
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

def calculate_file_hash(file_path):
    """
    Calculate a SHA-256 hash for the given file.

    :param file_path: Path to the file
    :return: Hexadecimal hash string
    """
    hash_algo = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(8192):
            hash_algo.update(chunk)
    return hash_algo.hexdigest()

def extract_pdf_pages(filepath):
    """
    Extract text from each page of a PDF file.

    :param filepath: Path to the PDF file
    :return: List of text content for each page
    """
    reader = PdfReader(filepath)
    pages = [page.extract_text() for page in reader.pages]
    return pages

def save_pages_to_storage(pages, storage_path):
    """
    Save the extracted text of PDF pages into separate text files.

    :param pages: List of text content for each page
    :param storage_path: Directory path to save the text files
    """
    os.makedirs(storage_path, exist_ok=True)
    for page_num, page_content in enumerate(pages, start=1):
        page_file = os.path.join(storage_path, f"page_{page_num}.txt")
        with open(page_file, "w", encoding="utf-8") as f:
            f.write(page_content)

def ensure_storage_folder(base_path, hash_value):
    """
    Ensure a storage folder exists for the given hash.

    :param base_path: Base directory for storage
    :param hash_value: Hash of the file (used as folder name)
    :return: Path to the storage folder
    """
    storage_path = os.path.join(base_path, hash_value)
    os.makedirs(storage_path, exist_ok=True)
    return storage_path

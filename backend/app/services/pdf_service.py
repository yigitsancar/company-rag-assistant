from pypdf import PdfReader
from pdf2image import convert_from_path
from pypdf import PdfReader
import pytesseract


def extract_text_with_pypdf(file_path: str) -> str:
    reader = PdfReader(file_path)

    text = ""

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text.strip()


def extract_text_with_ocr(file_path: str) -> str:
    images = convert_from_path(file_path)

    text = ""

    for image in images:
        page_text = pytesseract.image_to_string(
            image,
            lang="tur+eng"
        )

        if page_text:
            text += page_text + "\n"

    return text.strip()


def extract_text_from_pdf(file_path: str) -> str:
    text = extract_text_with_pypdf(file_path)

    if text:
        return text

    return extract_text_with_ocr(file_path)

def extract_pages_from_pdf(file_path: str):
    reader = PdfReader(file_path)

    pages = []

    for index, page in enumerate(reader.pages, start=1):
        page_text = page.extract_text()

        if page_text and page_text.strip():
            pages.append({
                "page_number": index,
                "text": page_text.strip()
            })

    return pages

import fitz

def extract_text(pdf_path):
    document = fitz.open(pdf_path)
    all_text = ""
    for page in document:
        all_text +=page.get_text()
    document.close()
    return all_text
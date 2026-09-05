from celery import shared_task
from api.models import PDF
from .parser import extract_text
from .cleaner import clean_text
from .chunker import chunk_text
from .embedder import embed_chunks
from .vector_store import create_collection, store_chunks

@shared_task
def process_pdf(pdf_id):
    pdf = PDF.objects.get(id=pdf_id)
    pdf_path = pdf.file.path
    raw_text = extract_text(pdf_path)
    cleaned_text = clean_text(raw_text)
    chunks = chunk_text(cleaned_text)
    vectors = embed_chunks(chunks)
    create_collection()
    store_chunks(chunks, vectors, pdf.id)
    pdf.extracted_text = cleaned_text
    pdf.save()
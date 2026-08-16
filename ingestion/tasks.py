from celery import shared_task
from api.models import PDF
from .parser import extract_text
from .cleaner import clean_text
from .chunker import chunk_text
from .embedder import embed_chunks
from .vector_store import create_collection, store_chunks

@shared_task
def process_pdf(pdf_id):
    print("1. Starting task")

    pdf = PDF.objects.get(id=pdf_id)

    pdf_path = pdf.file.path

    raw_text = extract_text(pdf_path)
    print("2. Extraction done")

    cleaned_text = clean_text(raw_text)
    print("3. Cleaning done")

    chunks = chunk_text(cleaned_text)
    print(f"4. Created {len(chunks)} chunks")

    vectors = embed_chunks(chunks)
    print(f"5. Created embeddings: {vectors.shape}")

    create_collection()
    print("6. Collection ready")

    store_chunks(chunks, vectors, pdf.id)
    print("7. Stored vectors in Qdrant")

    pdf.extracted_text = cleaned_text
    pdf.save()

    print("8. Task complete")
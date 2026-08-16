from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
import uuid

client = QdrantClient(url="http://localhost:6333")

COLLECTION_NAME = "memos"

def create_collection():
    collections = client.get_collections().collections

    if not any(c.name == COLLECTION_NAME for c in collections):
        client.create_collection(
            collection_name = COLLECTION_NAME,
            vectors_config = VectorParams(size=384,distance=Distance.COSINE)
        )

def store_chunks(chunks, vectors, pdf_id):
    points = []
    for i, (chunk, vector) in enumerate(zip(chunks,vectors)):
        points.append(
            PointStruct(
                id = str(uuid.uuid4()),
                vector = vector.tolist(),
                payload = {
                    "pdf_id": pdf_id,
                    "chunk_index": i,
                    "text": chunk,
                }
            )
        )
    client.upsert(
        collection_name =COLLECTION_NAME,
        points = points
    )
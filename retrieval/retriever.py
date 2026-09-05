from qdrant_client import QdrantClient
from ingestion.embedder import model

client = QdrantClient(url="http://localhost:6333")
COLLECTION_NAME = "memos"

def retrieve(query, limit=5):
    query_vector = model.encode(query).tolist()
    results = client.query_points(
        collection_name = COLLECTION_NAME,
        query = query_vector,
        limit = limit,
    )
    return results.points

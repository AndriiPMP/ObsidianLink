from qdrant_client import QdrantClient 
from qdrant_client.models import Distance, VectorParams, PointStruct

client = QdrantClient(host="localhost", port=6333)

client.create_collection(
    collection_name="obsidian_base",
    vectors_config=VectorParams(
        size=2048,
        distance=Distance.COSINE
    )
)


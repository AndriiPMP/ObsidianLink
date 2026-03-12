from qdrant_client import QdrantClient 
from qdrant_client.models import Distance, VectorParams, PointStruct
from hash_alg import generate_hash_filepath

client = QdrantClient(host="localhost", port=6333)

client.create_collection(
    collection_name="obsidian_base",
    vectors_config=VectorParams(
        size=2048,
        distance=Distance.COSINE
    )
)

def add_document(client, collection_name, vector, formated_path, full_path, content):

    id_number = generate_hash_filepath(formated_path)

    point = PointStruct(
        id=id_number,
        vector=vector,
        payload={
            "formated_path": formated_path,
            "path": full_path,
            "content": content
        }
    )

    client.upsert(
        collection_name=collection_name,
        points=[point]
    )

def search_similar(client, collection_name, query_vector, limit=3):
    results = client.search(
        collection_name=collection_name,
        query_vector=query_vector,
        limit=limit
    )

    return results
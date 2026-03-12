from qdrant_client import QdrantClient 
from qdrant_client.models import Distance, VectorParams, PointStruct
from hash_alg import generate_hash_filepath

client = QdrantClient(host="localhost", port=6333) # Подключаемся к квадранту

client.create_collection( # Создаём саму колекцию
    collection_name="obsidian_base",
    vectors_config=VectorParams(
        size=2048,
        distance=Distance.COSINE
    )
)

def add_document(client, collection_name, vector, formated_path, full_path, content):

    id_number = generate_hash_filepath(formated_path) # Генерируем хеш для каждого пути

    point = PointStruct(  # Указываем что именно помещаем в квадрант
        id=id_number,
        vector=vector,
        payload={
            "formated_path": formated_path,
            "full_path": full_path,
            "content": content
        }
    )

    client.upsert( # Потом непосредственно помещаем
        collection_name=collection_name,
        points=[point]
    )

def search_similar(client, collection_name, query_vector, limit=3):
    results = client.search( # Показываем что мы должны получить как результат
        collection_name=collection_name,
        query_vector=query_vector,
        limit=limit
    )

    return results # Возвращаем результат для переиспользования
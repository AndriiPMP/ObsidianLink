from qdrant_client.models import Distance, VectorParams, PointStruct
from script.hash_alg import generate_hash_filepath
from configuration import client


def create_collection_if_not_exists():
    if not client.collection.exists("obsidian_base"):
        client.create_collection( # Создаём саму колекцию
            collection_name="obsidian_base",
            vectors_config=VectorParams(
                size=2048,
                distance=Distance.COSINE
    )
)
        
create_collection_if_not_exists()


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




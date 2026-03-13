from files_info import get_files_data
from ai_integr import generate_embedding
from qdrant_integr import add_document, client

files_data = get_files_data()

COLLECTION_NAME = "obsidian_base"

vector = [] 

# Создаём новый вектор и помещаем его в хранилище вместе с метаданными
for file_data in files_data:
    content = file_data["content"]
    formated_path = file_data["formated_path"]
    full_path = file_data["path"]
    embedding = generate_embedding(content)
    add_document(
        client=client,
        collection_name=COLLECTION_NAME,
        vector=embedding,
        formated_path=formated_path,
        full_path=full_path,
        content=content
    )



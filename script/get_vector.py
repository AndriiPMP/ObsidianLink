from files_info import get_files_data
from ai_integr import generate_embedding
from qdrant_integr import add_document, client
import redis 
import json

r = redis.Redis(host='localhost', port=6379, db=0)

while True:
    item = r.lpop('embedding_queue')
    if item is None:
        break

file_items = json.loads(item)

COLLECTION_NAME = "obsidian_base"

vector = [] 


embedding = generate_embedding(file_items['content'])
add_document(
    client=client,
    collection_name=COLLECTION_NAME,
    vector=embedding,
    formated_path=file_items['formated_path'],
    full_path=file_items['path'],
    content=file_items['content']
)



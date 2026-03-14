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

def process_and_add_doc(task:dict):

    file_path = task.get("path")
    formated_path = task.get("formated_task")
    content = task.get("content")
    
    embedding = generate_embedding()
    add_document(
        client=client,
        collection_name=COLLECTION_NAME,
        vector=embedding,
        formated_path= file_path, 
        full_path=formated_path,
        content=content
    )



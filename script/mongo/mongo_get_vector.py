from script.others.ai_integr import generate_embedding
from redis_implement.redis_queue import get_next_task, task_completed
from script.mongo.mongo_integr import add_document, mongo_client


COLLECTION_NAME = "obsidian_base"

def index_files():

    while True:
        task = get_next_task()
        
        if task is None:
            print("   Индексация завершена.")
            break
        
        print(f"   Индексирую: {task.get('path')}")

        process_and_add_doc(task)      

        task_completed(task)

def process_and_add_doc(task: dict):

    file_path = task.get("path")

    formated_path = task.get("formated_path")
    
    content = task.get("content")

    embedding = generate_embedding(content)

    add_document(
        client=mongo_client,
        collection_name=COLLECTION_NAME,
        vector=embedding,
        formated_path=formated_path,
        full_path=file_path,
        content=content
    )



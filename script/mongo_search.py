from configuration import client, MONGODB_COLLECTION, MONGODB_VECTOR_INDEX
from script.ai_integr import generate_embedding
from redis_implement.redis_queue import get_next_task, task_completed
import os

collection_name = MONGODB_COLLECTION

def search_similar(client, collection_name, content, limit=3):
    query_vector = generate_embedding(content) 
    collection = client[collection_name]

    pipeline = [
        {
        "$vectorSearch":{
            "index": MONGODB_VECTOR_INDEX,
            "path": "embedding",
            "queryVector": query_vector,
            "numCandidates": max(limit * 20, 100),
            "limit": limit
        }
    },
    {
        "$project": {
            "_id": 1,
            "formated_path": 1,
            "full_path": 1,
            "content": 1,
            "score": {"$meta": "vectorSearchScore"},
            }
        },
    ]

    return list(collection.aggregate(pipeline))

def get_redis_content():
    task = get_next_task()
    content = task.get("content")

    return search_similar(
        client=client,
        collection_name=collection_name,
        conntent=content,
        limit=limit,
    )

def get_formated_paths_from_search(client, collection_name, content, limit=3):
    results = search_similar(client, collection_name, content, limit)
    paths=[]
    
    for result in results:
        formated_path = result.get("formated_path")
        if formated_path:
                if formated_path.endswith(".md"):
                    formated_path = formated_path[:-3]
                formated_path = formated_path.replace("\\", "/")
                paths.append(formated_path)

    return paths

def add_similar_links_to_file(task, paths):
    file_path = task.get("path")

    links = "\n\n"
    for path in paths:
        links += f" - [[{path}]]\n"

    with open(file_path, "a", encoding="utf-8") as f:
        f.write(links)

def process_links():
    while True:
        task = get_next_task()
        
        if task is None:
            print("   Обработка завершена.")
            break
        
        print(f"   Обрабатываю: {task.get('path')}")
        
        content = task.get("content")
        
        paths = get_formated_paths_from_search(
            client=client,
            collection_name=collection_name,
            content=content,
            limit=3
        )
        
        if paths:
            add_similar_links_to_file(task, paths)
            print(f"   Добавлено ссылок: {len(paths)}")
        
        task_completed(task)

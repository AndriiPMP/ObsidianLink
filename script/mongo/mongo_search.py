from configuration import mongo_client, MONGODB_COLLECTION, MONGODB_VECTOR_INDEX, MONGODB_DB
from script.others.ai_integr import generate_embedding
from redis_implement.redis_queue import get_next_task, task_completed

collection_name = MONGODB_COLLECTION

def search_similar(client, collection_name, content, limit=4):

    db = client[MONGODB_DB]

    query_vector = generate_embedding(content) 

    collection = db[collection_name]

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
            {
            "$match": {
                "score": {"$gte": 0.775}
            }
        },
    ]

    return list(collection.aggregate(pipeline))

def get_redis_content(limit=4):

    task = get_next_task()

    if task is None:
        return[

        ]
    content = task.get("content")
    if not content:
        return[]

    return search_similar(
        client=mongo_client,
        collection_name=collection_name,
        content=content,
        limit=limit,
    )

def get_formated_paths_from_search(client, collection_name, content, current_formated_path, limit=4):

    results = search_similar(client, collection_name, content, limit)

    paths=[]

    current_formated_path = current_formated_path.replace("\\", "/")
    
    if current_formated_path.endswith(".md"):
        current_formated_path = current_formated_path[:-3]

    for result in results:
        formated_path = result.get("formated_path")
        if not formated_path:
            continue
    

        if formated_path.endswith(".md"):
            formated_path = formated_path[:-3]
        
        formated_path = formated_path.replace("\\", "/")

        if formated_path == current_formated_path:
                continue
    
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
            client=mongo_client,
            collection_name=collection_name,
            content=content,
            current_formated_path=task.get("formated_path"),
            limit=4,
        )
        
        if paths:
            add_similar_links_to_file(task, paths)
            print(f"   Добавлено ссылок: {len(paths)}")
        
        task_completed(task)

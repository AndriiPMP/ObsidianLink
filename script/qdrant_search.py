from configuration import client
from ai_integr import generate_embedding
from redis_implement.redis_queue import get_next_task
import os



def search_similar(client, collection_name, content, limit=3):
    query_vector = generate_embedding(content) # Прямо внутри данной функции генерируем вектор

    results = client.search( # Показываем что мы должны получить как результат
        collection_name=collection_name,
        query_vector=query_vector,
        limit=limit
    )

    return results # Возвращаем результат для переиспользования

def get_redis_content():
    task:dict = get_next_task()
    content = task.get(content)

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
        formated_path = result.payload.get("formated_path")
        if formated_path:
            paths.append(formated_path)

    return paths

def add_similar_links_to_file(task, paths):
    paths = get_formated_paths_from_search(paths)
    file_path = task.get("path")

    links = "\n\n"
    for path in paths:
        links += f" - [[{path}]]\n"

    with open(file_path, "a", encoding=utf-8) as f:
        f.write(links)

import redis

r = redis.Redis(host='localhost', port=6379, db=0)

def process_file(task:dict):
    file_path = task.get("path")
    content = task.get("content")        

    print(f"[PROCESSING] {file_path}")
    print(f"[PROCESSING] {content}")
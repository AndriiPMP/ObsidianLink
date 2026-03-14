import redis
import json
from redis_queue_store import get_pending_tasks, save_queue
from script.files_info import get_files_data

queue_name = "tasks"

r = redis.Redis(host='localhost', port=6379, db=0)

def restore_queue():
    pending_tasks = get_pending_tasks()
    r.delete(queue_name)
    for task in pending_tasks:
        r.rpush(queue_name, json.dumps(task))


def create_new_queue():

    files_info = get_files_data()

    r.delete(queue_name)
    for file_info in files_info:
        r.rpush(queue_name, json.dumps(files_info))
    
    save_queue(files_info)

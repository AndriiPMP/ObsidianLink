import redis
import json
from script.files_info import get_files_data
from redis_queue_store import has_pending_tasks, get_pending_tasks, save_queue

r = redis.Redis(host='localhost', port=6379, db=0)

queue_name = "embedding_queue"

def init_queue():
    if has_pending_tasks():
        restore_queue()
    else: 
        create_new_queue()

files_info = get_files_data()

for file_info in files_info:
    r.rpush('embedding_queue', json.dumps(file_info))

r.save
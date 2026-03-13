import redis
import json
from script.files_info import get_files_data

r = redis.Redis(host='localhost', port=6379, db=0)

files_info = get_files_data()

for file_info in files_info:
    r.rpush('embedding_queue', json.dumps(file_info))

r.save
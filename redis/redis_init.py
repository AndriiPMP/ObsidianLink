import time
import json
from script.files_info import get_files_data
from redis_queue import get_next_task, task_completed, init_queue
from redis_proccess_files import process_file 
from configuration import r

queue_name = "embedding_queue"


files_info = get_files_data()

for file_info in files_info:
    r.rpush('embedding_queue', json.dumps(file_info))

r.save()



def main():
    init_queue()

    while True:
        task = get_next_task()
        if task:
            process_file(task)
            task_completed(task)
        else:
            time.sleep(5)
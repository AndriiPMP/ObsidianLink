import json
from redis_implement.redis_queue_store import (get_pending_tasks, 
                                               save_queue, 
                                               has_pending_tasks, 
                                               remove_pending_tasks)
from script.others.files_process import get_files_data
from configuration import r

queue_name = "tasks"

def init_queue():

    if has_pending_tasks():
        restore_queue()

    else:
        create_new_queue()

def restore_queue():

    pending_tasks = get_pending_tasks()

    r.delete(queue_name)

    for task in pending_tasks:
        r.rpush(queue_name, json.dumps(task))


def create_new_queue():

    files_info = get_files_data()

    r.delete(queue_name)
    
    for file_info in files_info:
        r.rpush(queue_name, json.dumps(file_info))
    
    save_queue(files_info)

def get_next_task():

    task_json = r.lpop(queue_name)
    
    if task_json:
        return json.loads(task_json)
    return None

def task_completed(task: dict):

    remove_pending_tasks(task)
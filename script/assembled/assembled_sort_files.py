from script.others.create_backUp import create_backup
from script.others.file_movement import sort_files_movement
from threading import Event
from redis_implement.redis_queue import init_queue
from script.others.files_for_movement import build_payloads

task_done = Event()

def sort_files():

    try:
        init_queue(build_payloads)
        create_backup()
        sort_files_movement()
    finally:
        task_done.set()
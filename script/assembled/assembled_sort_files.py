from script.others.create_backUp import create_backup
from script.others.file_movement import move_file_by_model
from threading import Event

task_done = Event()

def sort_files():

    try:
        create_backup()
        move_file_by_model()
    finally:
        task_done.set()
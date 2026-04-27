import shutil
from pathlib import Path        
from script.others.ai_integr import generate_text
from redis_implement.redis_queue import get_next_task, task_completed
import os

def move_file_by_model(task):
    prompt = task["task"]
    folders = task["folders"]
    sort_text = task["sort"]

    full_prompt = f"{prompt}\n\nFOLDERS:\n{folders}\n\nSORT:\n{sort_text}"

    model_path = generate_text(full_prompt).strip()

    sort_dir = os.getenv("TARGET_DIR")

    source_path = Path(sort_dir)
    target_dir = Path(model_path)
    target_path = target_dir / source_path.name

    target_path.parent.mkdir(parents=True, exist_ok=True)

    shutil.move(str(source_path), str(target_path))

def sort_files_movement():

    while True:
        task = get_next_task()
        if task is None:
            break

        move_file_by_model(task)
        task_completed(task)
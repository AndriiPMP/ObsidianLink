import json
from datetime import datetime
import os


redis_queue_dir = os.path.dirname(__file__)
redis_queue_store = os.path.join(redis_queue_dir, "queue_state.json")


def load_queue_state() -> dict:
    if not os.path.exists(redis_queue_store):
        return {"pending]": [], "last_updated": None}
    try: 
        with open(redis_queue_store, "r", encoding="utf-8") as f:
            return json.load(f)
    except(json.JSONDecodeError, IOError) as e:
        print(f"[WARNING] Не удалось прочитать redis_queue.json: {e}")
        return {"pending": [], "last_updated": None}
    

def save_queue(pending_tasks: list):

    state = {
        "pending": pending_tasks, 
        "last_updated": datetime.now().isoformat(),
        "count": len(pending_tasks)
    }

    try:
        with open(redis_queue_store, "w", encoding="utf-8") as f:
            json.dump(state, f, ensure_ascii=False, indent=2)
    except IOError as e:
         print(f"[ERROR] Не удалось сохранить queue_state.json: {e}")


def get_pending_tasks():
    state = load_queue_state()
    return state.get("pending", [])


def has_pending_tasks():
    pending = get_pending_tasks()
    return len(pending) > 0


def remove_pending_tasks(task: dict):
    pending = get_pending_tasks()
    task_path = task.get("path")
    update_pending = [t for t in pending if t.get("path") != task_path]
    save_queue(update_pending)



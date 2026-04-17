import json
import os

redis_queue_store = os.path.join(
    os.path.dirname(__file__),
    "..",
    "..",
    "redis_implement",
    "queue_state.json",
)

redis_queue_store = os.path.abspath(redis_queue_store)

def count_queue_items():
    with open(redis_queue_store, "r", encoding="utf-8") as f:
        data = json.load(f)

    return len(data)


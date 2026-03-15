import json
import pytest
from unittest.mock import patch
from configuration import r 
from redis_implement.redis_queue import restore_queue, queue_name, create_new_queue, get_next_task

def test_restore_queue():

    test_tasks = [
        {"path": "test/path1.md", "formated_path": "path1.md", "content": "content 1"},
        {"path": "test/path2.md", "formated_path": "path2.md", "content": "content 2"},
    ]

    r.delete(queue_name)

    with patch("redis_implement.redis_queue.get_pending_tasks", return_value=test_tasks):
        restore_queue()

    queue_len = r.llen(queue_name)
    assert queue_len == 2

    first_item = r.lindex(queue_name, 0)
    data = json.loads(first_item)
    assert data["path"] == "test/path1.md"

    second_item = r.lindex(queue_name, 1)
    data = json.loads(second_item)
    assert data["path"] == "test/path2.md"

    r.delete(queue_name)

def test_create_new_queue():
    r.delete(queue_name)
    
    with patch("redis_implement.redis_queue.save_queue"):
        create_new_queue()

    queue_len = r.llen(queue_name)
    assert queue_len > 0

    first_item = r.lindex(queue_name, 0)
    data = json.loads(first_item)

    assert "path" in data
    assert "formated_path" in data
    assert "content" in data

    r.delete(queue_name)

def test_get_next_task():
    r.delete(queue_name)
    r.rpush(queue_name, json.dumps({"path": "test1.md", "content": "content 1"}))
    r.rpush(queue_name, json.dumps({"path": "test2.md", "content": "content 2"}))

    task = get_next_task()

    assert task is not None
    assert task["path"] == "test1.md"
    assert task["content"] == "content 1"

    queue_len = r.llen(queue_name)
    assert queue_len == 1

    task = get_next_task()
    assert task["path"] == "test2.md"

    r.delete(queue_name)

    
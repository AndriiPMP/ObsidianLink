import json
import pytest
from datetime import datetime
from unittest.mock import patch
from redis_implement.redis_queue_store import (get_pending_tasks, 
                                               has_pending_tasks, 
                                               remove_pending_tasks, 
                                               load_queue_state,
                                               save_queue)

def test_get_pending_tasks_with_files():
    with patch("redis_implement.redis_queue_store.load_queue_state") as mock_load:
        mock_load.return_value = {
            "pending": [
                {"path": "file1.md", "action": "create"},
                {"path": "file2.md", "action": "update"},
                {"path": "folder/note3.md", "action": "delete"}                
            ],
            "last_updated": "2026-03-16T10:30:30",
            "count": 3
        }

        result = get_pending_tasks()

        assert len(result) == 3 
        assert result[0]["path"] == "file1.md"
        assert result[1]["action"] == "update"
        assert result[2]["path"] == "folder/note3.md"


def test_get_pending_task_empty():
    with patch("redis_implement.redis_queue_store.load_queue_state") as mock_load:
        mock_load.return_value = {
            "pending": [],
            "last_updated": None
        }

    result = get_pending_tasks()

    assert result == []

def test_has_pending_task_true():
    with patch("redis_implement.redis_queue_store.get_pending_tasks") as mock_get:
        mock_get.return_value = [
            {"path": "note1.md", "action": "create"},
            {"path": "note2.md", "action": "update"}
        ]

        result = has_pending_tasks()

        assert result is True

def test_has_panding_tasks_false():
    with patch("redis_implement.redis_queue_store.get_pending_tasks") as mock_get:
        mock_get.return_value = []

        result = has_pending_tasks()

        assert result is False

def test_remove_panding_tasks(tmp_path):
    temp_file = tmp_path / "queue_state.json"

    with patch("redis_implement.redis_queue_store.get_pending_tasks") as mock_get:
        mock_get.return_value = [
            {"path": "note1.md", "action": "create"},
            {"path": "note2.md", "action": "update"},
            {"path": "note3.md", "action": "delete"}            
        ]

        with patch("redis_implement.redis_queue_store.redis_queue_store", str(temp_file)):
            remove_pending_tasks({"path": "note2.md"})

        assert temp_file.exists

        with open(temp_file, "r", encoding="utf-8") as f:
            state = json.load(f)

        assert len(state["pending"]) == 2
        assert state["pending"][0]["path"] == "note1.md"
        assert state["pending"][1]["path"] == "note3.md"

def test_save_queue_with_files(tmp_path):
    temp_file = tmp_path / "queue_state.json"

    pending_tasks = [
        {"path": "note1.md", "action": "create"},
        {"path": "folder/note2.md", "action": "update"},
        {"path": "note3.md", "action": "delete"}        
    ]

    with patch("redis_implement.redis_queue_store.redis_queue_store", str(temp_file)):
        save_queue(pending_tasks)

    assert temp_file.exists()

    with open(temp_file, "r", encoding="utf-8") as f:
        state = json.load(f)

    assert state["pending"] == pending_tasks
    assert state["count"] == 3
    assert "last_updated" in state
    
    datetime.fromisoformat(state["last_updated"])

def test_save_queue_empty(tmp_path):
    temp_file = tmp_path / "queue_state.json"

    with patch("redis_implement.redis_queue_store.redis_queue_store", str(temp_file)):
        save_queue([])

    with open (temp_file, "r", encoding="utf-8") as f:
        state = json.load(f)

    assert state["pending"] == []
    assert state["count"] == 0

def test_load_queue_state(tmp_path):
    temp_file = tmp_path / "queue_state.json"

    test_data = {
        "pending": [
            {"path": "note1.md", "action": "create"},
            {"path": "note2.md", "action": "update"}            
        ],
        "last_updated": "2026-03-17T10:30:00",
        "count": 2
    }

    with open (temp_file, "w", encoding="utf-8") as f:
        json.dump(test_data, f)

    with patch("redis_implement.redis_queue_store.redis_queue_store", str(temp_file)):
        result = load_queue_state()

    assert result == test_data
    assert len(result["pending"]) == 2
    assert result["pending"][0]["path"] == "note1.md"

def test_load_queue_state_empty(tmp_path):
    temp_file = tmp_path / "queue_state.json"
    
    with patch("redis_implement.redis_queue_store.redis_queue_store", str(temp_file)):
        result = load_queue_state()

    assert result == {"pending": [], "last_updated": None}

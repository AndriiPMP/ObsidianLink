from unittest.mock import patch
from redis_implement.redis_queue_store import get_pending_tasks, has_pending_tasks

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

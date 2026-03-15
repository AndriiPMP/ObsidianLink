import json
import pytest
from unittest.mock import patch, MagicMock
from redis_implement.redis_init import init_files_queue
import time
from configuration import r

# @pytest.mark.timeout(50, method="thread")
def test_init_files_queue():
    r.delete("embedding_queue")

    with patch.object(r, 'save'):
        init_files_queue()

    queue_len = r.llen("embedding_queue")
    assert queue_len > 0

    first_item = r.lindex("embedding_queue", 0)
    data = json.loads(first_item)

    assert "path" in data
    assert "formated_path" in data
    assert "content" in data

    r.delete("embedding_queue")
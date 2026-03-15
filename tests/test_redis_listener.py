import pytest
import sys
from unittest.mock import patch, MagicMock

def test_redis_listener_script():
    mock_redis = MagicMock()
    mock_pubsub = MagicMock()

    messages = [
        {'type': 'subscribe', 'channel': b'__keyevent@__:lpop'},
        {'type': 'message', 'channel': b'__keyevent@__:lpop', 'data': b'lpop'},
        {'type': 'message', 'channel': b'__keyevent@__:lpop', 'data': b'lpop'},
    ]

    mock_pubsub.listen.return_value = iter(messages)
    mock_redis.pubsub.return_value = mock_pubsub

    if "redis_implement.redis_listener" in sys.modules:
        del sys.modules['redis_implement.redis_listener']

    with patch("configuration.r", mock_redis):
        import redis_implement.redis_listener

    assert mock_redis.save.call_count == 2
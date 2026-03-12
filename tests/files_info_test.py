import os
from script.files_info import get_file_paths

def test_get_file_paths():
    paths = get_file_paths()

    assert isinstance(paths, list)
    assert len(paths) > 0
    for path in paths:
        assert isinstance(path, str)
        assert os.path.exists(path)
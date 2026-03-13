import os
from script.files_info import (get_file_paths, 
format_paths, 
get_files_content, 
get_files_data, 
base_dir)

def test_get_file_paths():
    paths = get_file_paths()

    assert isinstance(paths, list)
    assert len(paths) > 0
    for path in paths:
        assert isinstance(path, str)
        assert os.path.exists(path)

def test_format_paths():
    formatted = format_paths([], base_dir)

    assert isinstance(formatted, list)
    assert len(formatted) > 0 
    for path in formatted:
        assert isinstance(path, str)
        assert not os.path.isabs(path)

def test_get_files_content():
    contents = get_files_content()

    assert isinstance(contents, list)
    assert len(contents) > 0
    for content in contents:
        assert isinstance(content, str)
        assert len(content) > 0 

def test_get_files_data():
    data = get_files_data()

    assert isinstance(data, list)
    assert len(data) > 0
    for item in data:
        assert isinstance(item, dict)
        assert "path" in item
        assert "formated_path" in item 
        assert "content" in item
        assert isinstance(item["path"], str)
        assert isinstance(item["formated_path"], str)
        assert isinstance(item["content"], str)
        assert os.path.exists(item["path"])
        assert not os.path.isabs(item["formated_path"])
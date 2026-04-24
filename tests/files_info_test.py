import os
import pytest
from script.others.files_info import (get_file_paths, 
format_paths, 
get_files_content, 
get_files_data, 
base_dir)

def test_get_file_paths(mocker):
    mock_walk = mocker.patch("script.files_info.os.walk")
    mock_walk.return_value = [
        (r"E:\План\IT", [], ["file1.md"]),
        (r"E:\План\IT\subdir", [], ["file2.md"])
    ]

    mock_exists = mocker.patch("os.path.exists", return_value=True)

    paths = get_file_paths()

    assert isinstance(paths, list)
    assert len(paths) > 0
    for path in paths:
        assert isinstance(path, str)
        assert os.path.exists(path)

    mock_walk.assert_called_once()


def test_format_paths(mocker):
    mock_get_file_formated = mocker.patch("script.files_info.get_file_paths")
    mock_get_file_formated.return_value = [
        r"E:\План\IT\file1.md",
        r"E:\План\IT\subdir\file2.md",
    ]

    mock_relpath = mocker.patch("os.path.relpath")
    mock_relpath.side_effect = lambda path, _: path.replace(r"E:\План\\", "")
    
    formatted = format_paths([], base_dir)

    assert isinstance(formatted, list)
    assert len(formatted) == 2
    for path in formatted:
        assert isinstance(path, str)
        


def test_get_files_content(mocker):
    mock_get_file_paths = mocker.patch("script.files_info.get_file_paths")
    mock_get_file_paths.return_value = [
        r"E:\План\IT\file1.md",
        r"E:\План\IT\file2.md",
    ]

    mock_file = mocker.MagicMock()
    mock_file.read.side_effect = ["content 1", "content 2"]
    mock_file.__enter__ = mocker.MagicMock(return_value=mock_file)
    mock_file.__exit__ = mocker.MagicMock(return_value=False)

    mocker.patch("builtins.open", return_value=mock_file)

    contents = get_files_content()

    assert contents == ["content 1", "content 2"]
    assert isinstance(contents, list)
    assert len(contents) > 0
    for content in contents:
        assert isinstance(content, str)
        assert len(content) > 0 


def test_get_files_data(mocker):
    mock_get_file_paths = mocker.patch("script.files_info.get_file_paths")
    mock_get_file_paths.return_value = [
        r"E:\План\IT\file1.md",
        r"E:\План\IT\file2.md",
    ]

    mock_format_paths = mocker.patch("script.files_info.format_paths")
    mock_format_paths.return_value = [
        r"IT\file1.md",
        r"IT\file2.md"
    ]

    mock_get_files_content = mocker.patch("script.files_info.get_files_content")
    mock_get_files_content.return_value = [
        "content 1",
        "content 2",
    ]

    data = get_files_data()

    assert isinstance(data, list)
    assert len(data) == 2
    for item in data:
        assert isinstance(item, dict)
        assert "path" in item
        assert "formated_path" in item 
        assert "content" in item
        assert isinstance(item["path"], str)
        assert isinstance(item["formated_path"], str)
        assert isinstance(item["content"], str)
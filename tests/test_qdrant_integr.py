import pytest
from script.qdrant_integr import create_collection_if_not_exists

def test_create_collection_if_not_exists(mocker):

    mock_exists = mocker.patch("script.configuration.client.collection.exists")
    mock_exists.return_value = False

    mock_create = mocker.patch("script.configuration.client.create_collection")

    create_collection_if_not_exists()

    mock_exists.assert_called_once_with("obsidian_base")

    mock_create.assert_called_once()

    call_kwargs = mock_create.call_args.kwargs
    assert call_kwargs["collection_name"] == "obsidian_base"
    assert call_kwargs["vectors_config"].size == 2048

def test_create_collection_already_exists(mocker):
    mock_exists = mocker.patch("script.configuration.client.collection.exists")
    mock_exists.return_value = False

    mock_create = mocker.patch("script.configuration.client.create_collection")

    create_collection_if_not_exists()

    mock_create.assert_not_called()
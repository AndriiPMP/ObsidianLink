import pytest
from script.mongo_integr import create_collection_if_not_exists

def test_create_collection_if_not_exists(mocker):

    mock_client = mocker.patch("script.qdrant_integr.client")
    mock_client.collection_exists.return_value = False

    create_collection_if_not_exists()

    mock_client.collection_exists.assert_called_once_with("obsidian_base")
    mock_client.create_collection.assert_called_once()

    call_kwargs = mock_client.create_collection.call_args.kwargs
    assert call_kwargs["collection_name"] == "obsidian_base"
    assert call_kwargs["vectors_config"].size == 2048

def test_create_collection_already_exists(mocker):
    mock_client = mocker.patch("script.qdrant_integr.client")
    mock_client.collection_exists.return_value = True

    create_collection_if_not_exists()

    mock_client.create_collection.assert_not_called()
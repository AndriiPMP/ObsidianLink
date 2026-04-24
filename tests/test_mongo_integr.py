from pymongo.operations import SearchIndexModel
from script.mongo.mongo_integr import (
        create_collection_if_not_exists,
        MONGODB_COLLECTION,
        MONGODB_VECTOR_INDEX,
        MONGODB_VECTOR_DIMENSIONS,
    )
from script.mongo.mongo_integr import create_collection_if_not_exists

def test_create_collection_if_not_exists(mocker):

    mock_client = mocker.patch("script.mongo_integr.mongo_client")
    mock_client.list_collection_names.return_value = []


    mock_client.list_collection_names.return_value = []
    mock_collection = mock_client.__getitem__.return_value
    mock_collection.list_search_indexes.return_value = []

    create_collection_if_not_exists()

    mock_client.list_collection_names.assert_called_once_with()
    mock_client.create_collection.assert_called_once_with("obsidian_base")
    mock_client.__getitem__.assert_called_once_with("obsidian_base")
    mock_collection.list_search_indexes.assert_called_once_with()
    mock_collection.create_search_index.assert_called_once()

    model = mock_collection.create_search_index.call_args.kwargs["model"]    
    assert isinstance(model, SearchIndexModel)
    assert model.document["name"] == "obsidian_vector_index"
    assert model.document["type"] == "vectorSearch"

    field = model.document["definition"]["fields"][0]
    assert field["path"] == "embedding"
    assert field["numDimensions"] == 4096
    assert field["similarity"] == "cosine"

def test_create_collection_already_exists(mocker):
    mock_client = mocker.patch("script.mongo_integr.mongo_client")
    mock_client.list_collection_names.return_value = ["obsidian_base"]

    mock_collection = mock_client.__getitem__.return_value
    mock_collection.list_search_indexes.return_value = [
        {"name": "obsidian_vector_index"}
    ]

    create_collection_if_not_exists()
    mock_client.list_collection_names.assert_called_once_with()
    mock_client.create_collection.assert_not_called()
    mock_client.__getitem__.assert_called_once_with("obsidian_base")
    mock_collection.list_search_indexes.assert_called_once_with()
    mock_collection.create_search_index.assert_not_called()
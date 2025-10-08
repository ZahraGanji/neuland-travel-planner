import os
from unittest.mock import MagicMock, patch

import pytest

from src.travel_planner.vector_store import (
    create_vector_store,
    load_vector_store,
    vector_store_exists,
)


# --- PYTEST TEST FUNCTIONS ---
# Replace the os.path.exists function with a fake object (mock_exists) just for this test
@patch("os.path.exists")
def test_vector_store_exists(mock_exists):
    """
    Tests if the vector_store_exists function correctly checks for files.
    """
    # the case where both index files exist
    mock_exists.return_value = True
    assert vector_store_exists() == True

    # the case where one or both files are missing
    mock_exists.return_value = False
    assert vector_store_exists() == False


@patch("src.travel_planner.vector_store.TextLoader")
@patch("src.travel_planner.vector_store.CharacterTextSplitter")
@patch("src.travel_planner.vector_store.HuggingFaceEmbeddings")
@patch("src.travel_planner.vector_store.FAISS")
@patch("os.path.exists", return_value=True)  # Assume book file exists
@patch("os.makedirs")
def test_create_vector_store_logic(
    mock_makedirs, mock_exists, mock_faiss, mock_embeddings, mock_splitter, mock_loader
):
    """
    Tests the logic of create_vector_store.
    This test mocks out all the heavy or external LangChain and file system operations
    to verify that the function calls them in the correct sequence.
    """
    # --- Setup Mocks ---
    # Create mock instances for the classes that are instantiated
    mock_loader.return_value.load.return_value = [
        MagicMock()
    ]  # Simulate loaded documents
    mock_splitter.return_value.split_documents.return_value = [
        MagicMock()
    ]  # Simulate split docs
    mock_embeddings.return_value = MagicMock()  # Simulate embeddings model

    mock_db_instance = MagicMock()
    mock_faiss.from_documents.return_value = mock_db_instance

    # --- Call Function ---
    create_vector_store()

    # --- Assertions ---
    # Verify that each major step was called once
    mock_loader.return_value.load.assert_called_once()
    mock_splitter.return_value.split_documents.assert_called_once()
    mock_faiss.from_documents.assert_called_once()
    mock_db_instance.save_local.assert_called_once()

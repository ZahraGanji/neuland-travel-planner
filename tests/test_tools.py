from unittest.mock import MagicMock, patch

import pytest
import requests

from src.travel_planner.tools import ask_book_tool, get_current_weather

# --- MOCK API RESPONSES ---
# This dictionary simulates a successful API response from OpenWeatherMap
MOCK_WEATHER_SUCCESS = {
    "weather": [{"description": "clear sky"}],
    "main": {"temp": 25.0},
    "name": "Paris",
    "sys": {"country": "FR"},
    "cod": 200,
}


# --- PYTEST TEST FUNCTIONS for Weather Tool ---
@patch("requests.get")
def test_get_current_weather_success(mock_get):
    """
    Tests the get_current_weather function for a successful API call.
    It uses @patch to 'mock' the requests.get call, preventing a real network request.
    """
    # Configure the mock to return a successful response object
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = MOCK_WEATHER_SUCCESS

    # Make raise_for_status do nothing for a successful test, the real raise_for_status() would raise an exception if the request failed
    mock_response.raise_for_status.return_value = None
    # Link the fake response to the fake requests.get
    mock_get.return_value = mock_response

    # Call the function we are testing
    result = get_current_weather("Paris")

    # Assert that the function returned the correctly formatted string
    assert result == "The current weather in Paris, FR is 25.0°C with clear sky."

    # Verify that the requests.get function was called once
    mock_get.assert_called_once()


@patch("requests.get")
def test_get_current_weather_city_not_found(mock_get):
    """
    Tests the get_current_weather function for a '404 City Not Found' error with the invalid city name.
    """
    # Configure the mock to simulate a 404 HTTP error
    mock_response = MagicMock()
    mock_response.status_code = 404
    # The side_effect simulates the exception being raised
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(
        response=mock_response
    )
    mock_get.return_value = mock_response

    # Call the function with a deliberately invalid city name
    result = get_current_weather("InvalidCityName")

    # Assert that the function returns the specific error message for a 404
    assert "Error: City 'InvalidCityName' not found." in result


@patch("requests.get")
def test_get_current_weather_generic_network_error(mock_get):
    """
    Tests the get_current_weather function for a generic network error (e.g., no internet).
    """
    # Configure the mock to raise a generic RequestException
    mock_get.side_effect = requests.exceptions.RequestException("Network is down")

    # Call the function
    result = get_current_weather("London")

    # Assert that the function catches the generic exception and returns a user-friendly message
    assert "An error occurred: Network is down" in result


# --- PYTEST TEST FUNCTIONS for Book Tool ---


@patch("src.travel_planner.tools.create_retriever_tool")
@patch("src.travel_planner.tools.load_vector_store")
def test_ask_book_tool_creation(mock_load_vector_store, mock_create_retriever_tool):
    """
    Tests the creation of the book tool.
    Mocks the vector store loading and the final tool creation to verify
    that the components are working correctly.
    """
    # --- Setup Mocks ---
    # Create a mock vector store object and a mock retriever
    mock_vector_store = MagicMock()
    mock_retriever = MagicMock()
    mock_vector_store.as_retriever.return_value = mock_retriever

    # Configure the mocked load_vector_store function to return our mock store
    mock_load_vector_store.return_value = mock_vector_store

    # --- Call Function ---
    ask_book_tool()

    # --- Assertions ---
    # 1. Verify that our code attempted to load the vector store
    mock_load_vector_store.assert_called_once()

    # 2. Verify that it created a retriever from the store with the correct settings
    mock_vector_store.as_retriever.assert_called_once_with(search_kwargs={"k": 3})

    # 3. Verify that the final LangChain tool was created with the correct retriever,
    #    name, and description, which are crucial for the agent's reasoning.
    mock_create_retriever_tool.assert_called_once_with(
        retriever=mock_retriever,
        name="ask_book",
        description="Finds and returns the most relevant passages from Mark Twain's book, 'The Innocents Abroad'. Useful for any questions about the content of the book 'The Innocents Abroad' by Mark Twain, Mark Twain's opinions, his travels, or the places and people he described.",
    )

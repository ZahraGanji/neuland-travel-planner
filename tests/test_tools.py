import pytest
import requests
from unittest.mock import MagicMock, patch
from src.travel_planner.tools import get_current_weather, ask_book_tool

# --- MOCK API RESPONSES ---
# This dictionary simulates a successful API response from OpenWeatherMap
MOCK_WEATHER_SUCCESS = {
    "weather": [{"description": "clear sky"}],
    "main": {"temp": 25.0},
    "name": "Paris",
    "sys": {"country": "FR"},
    "cod": 200
}

# --- PYTEST TEST FUNCTIONS for Weather Tool ---
@patch('requests.get')
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
    # Check if 'q=Paris' was in the parameters of the call
    assert "q=Paris" in mock_get.call_args.kwargs['params']

@patch('requests.get')
def test_get_current_weather_city_not_found(mock_get):
    """
    Tests the get_current_weather function for a '404 City Not Found' error with the invalid city name.
    """
    # Configure the mock to simulate a 404 HTTP error
    mock_response = MagicMock()
    mock_response.status_code = 404
    # The side_effect simulates the exception being raised
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(response=mock_response)
    mock_get.return_value = mock_response

    # Call the function with a deliberately invalid city name
    result = get_current_weather("InvalidCityName")

    # Assert that the function returns the specific error message for a 404
    assert "Error: City 'InvalidCityName' not found." in result

@patch('requests.get')
def test_get_current_weather_generic_network_error(mock_get):
    """
    Tests the get_current_weather function for a generic network error (e.g., no internet).
    """
    # Configure the mock to raise a generic RequestException
    mock_get.side_effect = requests.exceptions.RequestException("Network is down")

    # Call the function
    result = get_current_weather("London")

    # Assert that the function catches the generic exception and returns a user-friendly message
    assert "An error occurred while fetching weather: Network is down" in result


import os
from .vector_store import load_vector_store
from langchain.tools.retriever import create_retriever_tool
from .config import OPENWEATHERMAP_KEY
from langchain.tools import Tool
import requests

def get_current_weather(location: str) -> str:
    """
    a function that takes city name, calls the OpenWeatherMap API and Fetches the current weather information for a given location.

    Args:
        location: The city name for which to fetch the weather (e.g., "Paris").

    Returns:
        A formatted string with the weather information or an error message.
    """
    # define API endpoint and query parameters
    url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": location,
        "appid": OPENWEATHERMAP_KEY,
        "units": "metric"  # for Celsius
    }
    try:
        # Send the request to the OpenWeatherMap API
        request = requests.get(url, params=params)
        # Raise an error for bad responses
        request.raise_for_status()  
        # Convert the response to JSON
        data = request.json()
        # if the API succeeded
        if data["cod"] == 200:
            # Extract weather information
            weather_description = data["weather"][0]["description"]
            temperature = data["main"]["temp"]
            city = data["name"]
            country = data["sys"]["country"]
            return f"The current weather in {city}, {country} is {temperature}°C with {weather_description}."
        
        # If the API didn’t return 200
        else:
            return f"Error: Could not retrieve weather for {location}. Reason: {data.get('message', 'Unknown error')}"
    # Handle HTTP-specific errors
    except requests.exceptions.HTTPError as http_err:
        if request.status_code == 404:
            return f"Error: City '{location}' not found. Please check the spelling."
        return f"HTTP error occurred: {http_err}"
    # Handle other exceptions
    except Exception as err:
        return f"An error occurred: {err}"

        
# Create a LangChain Tool object from the weather function
weather_tool = Tool(
    name="get_current_weather",
    func=get_current_weather,
    description="Useful for getting the current weather for a specific city. Input should be a single city name (e.g., 'Paris', 'London')."
)       



def ask_book_tool():
    """
    Loads the vector store and creates a LangChain tool for querying the book.
    
    Returns:
        A LangChain retriever tool.
   """

    # Load the vector store
    vector_store = load_vector_store()

    # Create a retriever that fetches the top 3 most relevant text chunks
    retriever = vector_store.as_retriever(search_kwargs={"k": 3})

    # Create a tool for agent that uses the retriever to answer questions about the book
    tool = create_retriever_tool(
        retriever=retriever,
        name="ask_book",
        description="Finds and returns the most relevant passages from Mark Twain's book, 'The Innocents Abroad'. Useful for any questions about the content of the book 'The Innocents Abroad' by Mark Twain, Mark Twain's opinions, his travels, or the places and people he described."
    )

    return tool



#  Twain Travel Agent
**An AI-powered travel planner** that answers user queries by retrieving information from Mark Twain’s book *The Innocents Abroad* and calling a live weather API.  
This project was developed as a submission for the **Neuland AI home assignment**.

---
##  How It Works
This application uses a **Structured Chat Agent** powered by the Hugging Face model [`mistralai/Mixtral-8x7B-Instruct-v0.1`](https://huggingface.co/mistralai/Mixtral-8x7B-Instruct-v0.1)

The agent has access to two primary tools:

1. **📖 Book Search Tool**  
   Uses a **FAISS vector store** built from *The Innocents Abroad* to find the most relevant passages for a given query.  
   This implements a **Retrieval-Augmented Generation (RAG)** pipeline.

2. **🌦️ Weather Tool**  
   Calls the **OpenWeatherMap API** to retrieve **live, current weather data** for any location in the world.

When you submit a query, the agent will:

- Decide which tool (or tools) can best help answer the query
- Use the tools to gather the necessary information
- Combine and analyze the results into a clear, contextually accurate response  

For **out-of-scope questions**, the agent is instructed to **politely decline**.

## Project Structure
twain-travel-agent/
│
├── .github/
│ └── workflows/
│ └── test.yml 
│
├── data/
│ ├── innocents_abroad_clean.txt # The cleaned source text for the book, 
│ └── vector_store/ # Directory for the generated FAISS index
│
├── src/
│ └── travel_planner/
│ ├── init.py
│ ├── agent.py # Core agent logic 
│ ├── config.py # Manages environment variables, the API keys
│ ├── tools.py # Defines the weather and book search tools
│ └── vector_store.py # Logic for creating and loading the FAISS index
│
├── tests/
│ ├── init.py
│ ├── test_agent.py # Unit tests for the agent 
│ ├── test_tools.py # Unit tests for the weather and book tools
│ └── test_vector_store.py # Unit tests for the vector store logic
│
├── app.py # The Streamlit web user interface
├── main.py # The command-line interface (CLI) entry point
├── noxfile.py # Nox automation file for testing 
├── .env.example # Template for environment variables (Hugging Face token and open weather map API key)
├── requirements.txt # Project dependencies
└── README.md 

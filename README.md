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
```markdown
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
```
## Setup Instructions

### 1. Prerequisites
- Python **3.11+**
- An API key from [OpenWeatherMap](https://openweathermap.org/api)
- A Hugging Face API token with **write** permissions from [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)

### 2. Installation
Clone the repository:
```bash
git clone <your-repo-url>
cd twain-travel-agent
```

Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate 
```
Install dependencies:
```bash
pip install -r requirements.txt
```
### 2. Configure API Keys

Copy the example environment file:
```bash
cp .env.example .env
```
Open the newly created .env file and add your secret keys.

## Running the Application
### 1. Run the Web Application
The easier way to interact with the agent is through the Streamlit web interface:
```bash
streamlit run app.py
```
- The first time you launch, click the **"Build Knowledge Base"** button.  
  This is a **one-time step** that creates the vector store from the book.

- Once the vector store is built, you can start asking questions.

### 2. Run from the Command Line
You can also run the agent directly from your terminal.
First, build the vector store (one-time step):
```bash
python main.py --build
```
Then, ask a question:
```bash
python main.py "Your question goes here"
```

Example Queries
```bash
# Get live weather
python main.py "What's the current weather in Paris?"

# Ask about the book
python main.py "What did Mark Twain think about the Sphinx?"

# Use both tools in sequence
python main.py "I want to visit the places Twain went to in Italy — what's the weather like there now?"

# Test the out-of-scope guardrail
python main.py "Explain quantum physics"
```

## Running Tests
This project uses Nox to automate testing and quality checks.
```bash
# Run all unit tests
nox -s test
# Run static type checker (mypy)
nox -s typing
```

## Tech Stack
- **AI Framework:** LangChain
- **Model Hosting:** Hugging Face Hub (Inference API)
- **Vector Database:** FAISS (for local RAG)
- **Live Data:** OpenWeatherMap API
- **Web Interface:** Streamlit
- **Testing & Automation:** Nox, Pytest

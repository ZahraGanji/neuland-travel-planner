from .tools import tools
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from .config import HUGGINGFACE_TOKEN
from langchain_huggingface import HuggingFaceEndpoint
from langchain.agents import AgentExecutor, create_react_agent

def create_agent():
    """
    Creates and returns the AI agent with its tools and prompt.
    """
    #Create templated prompts for chat model
    prompt = ChatPromptTemplate.from_messages([("system", """
       You are a helpful travel planning assistant.
       Your purpose is to answer user questions based on two sources:
       1. A live weather API for current weather information.
       2. The text of Mark Twain's book, "The Innocents Abroad," for historical and travel insights.


       - If a question is about weather, use the 'get_current_weather' tool.
       - If a question is about Mark Twain's journey, locations, or opinions from the book, use the 'ask_book' tool.
       - For complex questions (e.g., "What's the weather like in the places Twain visited in Italy?"), you must use the tools in a sequence. First, find the places from the book, then get the weather for each.
       - If a question is outside of these topics (like "Explain quantum physics"), you must politely decline and state that you can only provide information about weather and Mark Twain's travels in "The Innocents Abroad".
       - Always provide a final, synthesized answer based on the tool outputs."""),
        ("user", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])

    # Initialize the LLM
    llm = HuggingFaceEndpoint(
        repo_id="meta-llama/Meta-Llama-3-8B",
        temperature=0.2,
        huggingfacehub_api_token=HUGGINGFACE_TOKEN,
    )

    # Create the ReAct agent, reasoning + acting agent
    agent = create_react_agent(llm, tools, prompt)

    # Create the agent executor which will run the agent
    # verbose=True shows the agent's thought process.
    # handle_parsing_errors=True makes the agent more robust.
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)

    return agent_executor

def run_agent(query: str):
    """
    Runs the agent with a given user query.

    Args:
        query (str): The user's question.

    Returns:
        dict: The result from the agent executor.
    """

    #call  the create_agent function
    agent_executor = create_agent()

    return agent_executor.invoke({"input": query})




from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from langchain.agents import AgentExecutor, create_structured_chat_agent
from langchain.tools.render import render_text_description
from langchain import hub
from .tools import weather_tool, ask_book_tool
from .config import HUGGINGFACE_TOKEN

def create_agent():
    """
    Creates and returns an AI agent that uses the "structured chat" method,
    which is a robust way to use tools with a wide variety of chat models.
    """
    # collect the list of tools the agent can use
    book_tool = ask_book_tool()
    all_tools = [weather_tool, book_tool]

    # Get the prompt template from LangChain Hub
    prompt = hub.pull("hwchase17/structured-chat-agent")

    # Create a more forceful set of instructions to constrain the model
    forceful_instructions = """You are a specialized travel planning assistant. Your ONLY capabilities are answering questions about Mark Twain's book "The Innocents Abroad" and providing live weather data using the tools provided.

    You MUST use a tool to find the information to answer a question.

    If a user asks a question that is not related to the book or the weather (e.g., "Explain quantum physics" or "What is the capital of France?"), you absolutely MUST NOT use your own general knowledge. You must respond with a message similar to: "I'm sorry, I can only answer questions about Mark Twain's 'The Innocents Abroad' and current weather conditions."
    """
        
    # Prepend the forceful instructions to the existing prompt template
    prompt.messages[0].prompt.template = forceful_instructions + "\n\n" + prompt.messages[0].prompt.template

    # Render the tools into a string format that the prompt template expects
    # and partially fill in the prompt with this information.
    tool_description = render_text_description(all_tools)
    tool_names = ", ".join([t.name for t in all_tools])
    
    prompt = prompt.partial(
        tools=tool_description,
        tool_names=tool_names,
    )

    # Initialize the Language Model from Hugging Face
    llm = HuggingFaceEndpoint(
        repo_id="mistralai/Mixtral-8x7B-Instruct-v0.1",
        temperature=0.2,
        huggingfacehub_api_token=HUGGINGFACE_TOKEN,
    )

    # Wrap the base LLM in the ChatHuggingFace adapter
    chat_model = ChatHuggingFace(llm=llm)

    # Create the structured chat agent, passing the wrapped chat_model
    agent = create_structured_chat_agent(chat_model, all_tools, prompt)
    
    # Create the agent executor to run the agent
    agent_executor = AgentExecutor(
        agent=agent, 
        tools=all_tools, 
        verbose=True,
        handle_parsing_errors=True 
    )
    
    return agent_executor

def run_agent(query: str):
    """
    Runs the agent with a given user query.
    """
    agent_executor = create_agent()
    # The structured chat agent expects a 'chat_history' variable.
    # We provide an empty list for these single-turn conversations.
    return agent_executor.invoke({
        "input": query,
        "chat_history": []
    })


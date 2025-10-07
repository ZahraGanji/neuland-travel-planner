import streamlit as st
from src.travel_planner.agent import run_agent
from src.travel_planner.vector_store import vector_store_exists, create_vector_store

# --- Page Configuration ---
st.set_page_config(
    page_title="Twain Travel Agent",
    page_icon="✈️",
    layout="centered",
    initial_sidebar_state="auto",
)

# --- App State Management ---
if 'vector_store_built' not in st.session_state:
    st.session_state.vector_store_built = vector_store_exists()

# --- UI Components ---
st.title("✈️ Twain Travel Agent")
st.markdown(
    "Your AI-powered assistant for planning travels inspired by Mark Twain's *The Innocents Abroad*. "
    "Ask about Twain's journey, his opinions, or get the current weather for any destination!"
)

# --- Vector Store Build Button ---
if not st.session_state.vector_store_built:
    st.warning("The knowledge base for the book has not been built yet. This is a one-time setup.")
    if st.button("Build Knowledge Base"):
        with st.spinner("Processing the book... This may take a few minutes."):
            create_vector_store()
            st.session_state.vector_store_built = True
            st.success("Knowledge base built successfully!")
            st.rerun() # to update the state

# --- Main Application Logic ---
if st.session_state.vector_store_built:
    # Input field for user query
    user_query = st.text_input("Ask your travel question:", placeholder="e.g., What did Twain think of the Sphinx?")

    if st.button("Ask the Agent"):
        if user_query:
            with st.spinner("The agent is thinking..."):
                try:
                    # Run the agent with the user's query
                    result = run_agent(user_query)
                    
                    # Display the final answer
                    st.success("Here's the agent's answer:")
                    st.write(result.get("output"))

                except Exception as e:
                    st.error(f"An error occurred: {e}")
        else:
            st.warning("Please enter a question.")
import streamlit as st
from src.travel_planner.agent import run_agent
from src.travel_planner.vector_store import vector_store_exists, build_vector_store

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

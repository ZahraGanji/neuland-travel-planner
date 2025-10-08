from unittest.mock import MagicMock, patch

import pytest

from src.travel_planner.agent import create_agent


# Mock every external dependency in agent.py with a patch decorator
@patch("src.travel_planner.agent.AgentExecutor")
@patch("src.travel_planner.agent.create_structured_chat_agent")
@patch("src.travel_planner.agent.ChatHuggingFace")
@patch("src.travel_planner.agent.HuggingFaceEndpoint")
@patch("src.travel_planner.agent.hub.pull")
@patch("src.travel_planner.agent.ask_book_tool")
@patch("src.travel_planner.agent.weather_tool", new_callable=MagicMock)
def test_create_agent_assembles_components_correctly(
    mock_weather_tool,
    mock_ask_book_tool,
    mock_hub_pull,
    mock_huggingface_endpoint,
    mock_chat_huggingface,
    mock_create_structured_chat_agent,
    mock_agent_executor,
):
    """
    Unit test for the create_agent function.
    This test verifies that all the components of the agent are initialized
    and assembled in the correct order with the correct parameters.
    """
    # --- 1. Setup Mocks ---

    mock_weather_tool.name = "get_current_weather"
    mock_book_tool = MagicMock()
    mock_book_tool.name = "ask_book"
    mock_ask_book_tool.return_value = mock_book_tool

    # Mock the prompt pulled from LangChain Hub
    mock_prompt = MagicMock()
    mock_prompt.messages[0].prompt.template = "Original Template"
    mock_hub_pull.return_value = mock_prompt

    # The .partial() method returns a new prompt object. We need to mock this behavior.
    mock_partial_prompt = MagicMock()
    mock_prompt.partial.return_value = mock_partial_prompt

    # Mock the language model and the agent constructor
    mock_llm_instance = MagicMock()
    mock_huggingface_endpoint.return_value = mock_llm_instance
    mock_chat_model_instance = MagicMock()
    mock_chat_huggingface.return_value = mock_chat_model_instance
    mock_agent_instance = MagicMock()
    mock_create_structured_chat_agent.return_value = mock_agent_instance

    # --- 2. Call the Function ---
    agent_executor_result = create_agent()

    # --- 3. Assertions ---

    # Verify that the tool functions were called as expected
    mock_ask_book_tool.assert_called_once()

    # Verify the correct prompt was pulled from the hub
    mock_hub_pull.assert_called_once_with("hwchase17/structured-chat-agent")

    # Verify that our custom instructions were correctly added to the prompt
    assert (
        "You are a specialized travel planning assistant"
        in mock_prompt.messages[0].prompt.template
    )
    assert "Original Template" in mock_prompt.messages[0].prompt.template

    # Verify that prompt.partial() was called
    mock_prompt.partial.assert_called_once()

    # Verify that the LLM was initialized correctly
    mock_huggingface_endpoint.assert_called_once()
    assert (
        mock_huggingface_endpoint.call_args.kwargs["repo_id"]
        == "mistralai/Mixtral-8x7B-Instruct-v0.1"
    )

    # Verify the chat model wrapper was used
    mock_chat_huggingface.assert_called_once_with(llm=mock_llm_instance)

    # Verify that the final agent was created with the right components
    mock_create_structured_chat_agent.assert_called_once()
    call_args, call_kwargs = mock_create_structured_chat_agent.call_args
    assert call_args[0] == mock_chat_model_instance
    assert mock_weather_tool in call_args[1]
    assert mock_book_tool in call_args[1]

    # Assert that the new prompt object returned by .partial() was used.
    assert call_args[2] is mock_partial_prompt

    # Verify that the AgentExecutor was created and returned
    mock_agent_executor.assert_called_once_with(
        agent=mock_agent_instance,
        tools=[mock_weather_tool, mock_book_tool],
        verbose=True,
        handle_parsing_errors=True,
    )
    assert agent_executor_result == mock_agent_executor.return_value

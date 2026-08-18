# general_handler.py - general handler agent that answers
# general queries with saved context from user and AI
# message for persistence.

from langchain_core.messages import HumanMessage, SystemMessage

from config import llm
from state import AgentState

GENERAL_SYSTEM_PROMPT = """
You are a helpful general-purpose assistant.

Answer the user's question clearly and naturally. Use the full conversation
history to maintain context and answer follow-up questions accurately.

Do not use content-writing tools. If the user asks about their previous request,
conversation history, or earlier details, inspect the available messages.
"""

def general_handler_node(state: AgentState) -> dict:
    """
    Handles general queries using the full conversation history.

    The router already stores the user's message. This node stores the
    assistant's response, preserving both messages in state.
    """
    messages = state["messages"]

    response = llm.invoke(
        [
            SystemMessage(content=GENERAL_SYSTEM_PROMPT),
            *messages,
        ]
    )

    return {
        "output": response.content,
        "messages": [response],
    }
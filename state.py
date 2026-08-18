# state.py - Creates a shared TypedDict

from typing import Annotated

from typing_extensions import Annotated, TypedDict
from langchain_core.messages import AnyMessage
from langgraph.graph.message import add_messages


class AgentState(TypedDict):
    user_input: str
    route: str
    output: str
    messages: Annotated[list[AnyMessage], add_messages]

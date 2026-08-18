# x_writer.py - Writes short posts with emojis and hashtags.

from langchain_core.messages import SystemMessage

from config import llm
from state import AgentState
from tools import internet_search_tool

x_tools = [
    internet_search_tool,
]

x_llm = llm.bind_tools(x_tools)

X_SYSTEM_PROMPT = """
You are an expert X/Twitter content writer.

Create engaging X posts based on the user's request.

Tool usage:
- Use internet_search_tool when current trends, news, hashtags, or real-time information
  would improve the post.
- Do not call the tool repeatedly with the same query.

When writing the final post:
- Keep the entire post under 280 characters.
- Use concise, engaging language.
- Include relevant emojis when appropriate.
- Include 1–3 relevant hashtags.
- Return only the final post.
- Do not include explanations, character counts, or quotation marks.

If current information is required, call the tool before writing the final post.
"""

def x_blog_writer_node(state: AgentState) -> dict:
    """
    Generates or continues an X/Twitter writing response.
    """
    response = x_llm.invoke(
        [
            SystemMessage(content=X_SYSTEM_PROMPT),
            *state["messages"],
        ]
    )

    update = {
        "messages": [response],
    }

    if not response.tool_calls and response.content:
        update["output"] = response.content

    return update
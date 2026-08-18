# seo_blog_writer.py - Bind both tools to LLM.

from langchain_core.messages import SystemMessage

from state import AgentState
from tools import research_tool, internet_search_tool
from config import llm

seo_tools = [
    research_tool,
    internet_search_tool,
]

seo_llm = llm.bind_tools(seo_tools)

SEO_SYSTEM_PROMPT = """
You are an expert SEO blog writer.

Create high-quality, accurate, long-form blog posts.

Tool usage:
- Use research_tool for in-depth articles, studies, and references.
- Use internet_search_tool for SEO keywords, current trends, and supporting information.
- Use research_tool only when deeper research is needed.
- Avoid repeatedly calling the same tool with the same query.

When writing the final blog post:
- Use a clear, compelling title.
- Include an introduction.
- Use descriptive Markdown headings.
- Use short paragraphs and bullet points where useful.
- Naturally incorporate relevant keywords.
- Maintain a helpful, authoritative tone.
- End with a clear call to action.
- Return only the completed blog post.

If you need more information, call the appropriate tool before writing the final answer.
"""

# Agent checks state messages for tool loop continuation.
# Agent writes structured blog with headings and CTA.

def seo_blog_writer_node(state: AgentState) -> dict:
    """
    Generates or continues an SEO blog-writing response.

    If the previous assistant message requested a tool, the existing
    messages are passed back to the model so it can continue the loop
    after receiving the tool result.
    """
    response = seo_llm.invoke(
        [
            SystemMessage(content=SEO_SYSTEM_PROMPT),
            *state["messages"],
        ]
    )

    update = {
        "messages": [response],
    }

    # Only store final text as output.
    # Tool-call messages are handled by the graph loop.
    if not response.tool_calls and response.content:
        update["output"] = response.content

    return update
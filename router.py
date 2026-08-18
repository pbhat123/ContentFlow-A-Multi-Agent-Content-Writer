# router.py - Returns a valid route while persisting user input into 'messages'

from langchain_core.messages import HumanMessage, SystemMessage

from config import llm
from state import AgentState

ROUTER_SYSTEM_PROMPT = """
You are a request router.

Classify the user's request into exactly one of these labels:

seo_blog_writer
x_blog_writer
general

Return only the label. Do not include explanations, punctuation, or formatting.

Use seo_blog_writer for long-form blog posts, SEO content, keyword research, or article writing.
Use x_blog_writer for tweets, X posts, Twitter threads, hashtags, or short social media content.
Use general for greetings, questions, conversation, or anything else.
"""

def router_node(state: AgentState) -> dict:
    user_input = state["user_input"]

    response = llm.invoke(
        [
            SystemMessage(content=ROUTER_SYSTEM_PROMPT),
            HumanMessage(content=user_input),
        ]
    )

    route = response.content.strip().lower()

    valid_routes = {
        "seo_blog_writer",
        "x_blog_writer",
        "general",
    }

    if route not in valid_routes:
        route = "general"

    return {
        "route": route,
        "messages": [HumanMessage(content=user_input)],
    }
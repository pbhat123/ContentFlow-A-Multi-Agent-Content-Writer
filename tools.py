# tools.py - setup and define 2 tools:
# 1. Research_tool (finds articles/references)
# 2. Internet_search_tool (finds SEO keywords/trending topics)

# setup both tools

import getpass
import json
import os

import serpapi
from tavily import TavilyClient
from langchain_core.tools import tool


def get_api_key(env_name: str, prompt: str) -> str:
    key = os.getenv(env_name)

    if not key:
        key = getpass.getpass(prompt)

    if not key:
        raise ValueError(f"{env_name} is required.")

    os.environ[env_name] = key
    return key


serpapi_key = get_api_key(
    "SERPAPI_KEY",
    "Enter your SerpAPI key: ",
)

tavily_key = get_api_key(
    "TAVILY_API_KEY",
    "Enter your Tavily API key: ",
)

serpapi_client = serpapi.Client(api_key=serpapi_key)
tavily_client = TavilyClient(api_key=tavily_key)

# Define both tools

# Research_tool (finds articles/references)
@tool
def research_tool(query: str) -> str:
    """Find in-depth articles, academic papers, and references for a topic."""
    results = serpapi_client.search(
        {
            "engine": "google_scholar",
            "q": query,
            "num": 10,
        }
    )

    references = results.get("organic_results", [])

    if not references:
        return "No research results found."

    formatted_results = [
        {
            "title": item.get("title"),
            "link": item.get("link"),
            "snippet": item.get("snippet"),
            "publication_info": item.get("publication_info"),
        }
        for item in references
    ]

    return json.dumps(formatted_results, indent=2, default=str)

# Internet_search_tool (finds SEO keywords/trending topics)
@tool
def internet_search_tool(query: str) -> str:
    """Search for SEO keywords, current trends, and trending topics."""
    results = tavily_client.search(
        query=query,
        search_depth="basic",
        max_results=5,
        include_answer=True,
    )

    return json.dumps(results, indent=2, default=str)
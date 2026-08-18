# config.py - setup llm call

import getpass
import os

from langchain_openai import ChatOpenAI

def get_openai_api_key() -> str:
    """Read the OpenAI API key securely from user input."""
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        api_key = getpass.getpass("Enter your OpenAI API key: ")

    if not api_key:
        raise ValueError("An OpenAI API key is required.")

    os.environ["OPENAI_API_KEY"] = api_key
    return api_key

def create_llm() -> ChatOpenAI:
    get_openai_api_key()

    return ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0,
    )

llm = create_llm()
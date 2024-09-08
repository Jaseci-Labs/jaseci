"""Serper API Integration."""

import json
import os

from jaclang.compiler.semtable import SemInfo

from mtllm.types import Tool

import requests

API_HEADERS = {
    "X-API-KEY": os.getenv("SERPER_API_KEY"),
    "Content-Type": "application/json",
}
assert API_HEADERS["X-API-KEY"], "Please set the SERPER_API_KEY environment variable."


def serper_search_tool(query: str) -> str:
    """Searches the Serper API."""
    payload = json.dumps(
        {
            "q": query,
        }
    )
    response = requests.request(
        "POST", "https://google.serper.dev/search", headers=API_HEADERS, data=payload
    )
    return response.text


search = Tool(
    serper_search_tool,
    SemInfo(
        None,
        "search",
        "ability",
        "Perform a Web Search",
    ),
    [SemInfo(None, "query", "str", "Query to search")],
)


def serper_scrape_webpage(url: str) -> str:
    """Scrapes the Serper API."""
    payload = json.dumps(
        {
            "url": url,
        }
    )
    response = requests.request(
        "POST", "https://scrape.serper.dev", headers=API_HEADERS, data=payload
    )
    return response.text


scrape = Tool(
    serper_scrape_webpage,
    SemInfo(
        None,
        "scrape",
        "ability",
        "Scrape Information from a Webpage",
    ),
    [SemInfo(None, "url", "str", "URL to scrape")],
)

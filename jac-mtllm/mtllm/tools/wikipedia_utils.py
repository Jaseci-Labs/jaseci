"""Wikipedia Tools for the MTLLM framework."""

from jaclang.compiler.semtable import SemInfo

from mtllm.types import Tool

import wikipedia as wikipedia_lib


def get_wikipedia_summary(title: str) -> str:
    """Gets the summary of the related article from Wikipedia."""
    try:
        return wikipedia_lib.summary(title)
    except Exception:
        options = wikipedia_lib.search(title, results=5, suggestion=True)
        raise Exception(f"Could not get summary for {title}. Similar titles: {options}")


wikipedia_summary = Tool(
    get_wikipedia_summary,
    SemInfo(
        None,
        "wikipedia_summary",
        "ability",
        "Gets the Summary of the related article from Wikipedia",
    ),
    [SemInfo(None, "title", "str", "Title to search")],
)

wikipedia_get_related_titles = Tool(
    wikipedia_lib.search,
    SemInfo(
        None,
        "wikipedia_get_related_titles",
        "ability",
        "Gets the related titles from Wikipedia",
    ),
    [SemInfo(None, "title", "str", "Title to search")],
)


def wikipedia_get_page(title: str) -> dict:
    """Gets the page from Wikipedia."""
    try:
        pg = wikipedia_lib.page(title)
        return {
            "title": pg.title,
            "content": pg.content,
            "url": pg.url,
            "summary": pg.summary,
        }
    except wikipedia_lib.DisambiguationError as e:
        raise Exception(f"Could not get page for {title}. Similar titles: {e.options}")


wikipedia_get_whole_page = Tool(
    wikipedia_get_page,
    SemInfo(
        None,
        "wikipedia_get_whole_page",
        "ability",
        "Gets the whole page from Wikipedia",
    ),
    [SemInfo(None, "title", "str", "Title to search")],
)

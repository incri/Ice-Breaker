from langchain_community.utilities import SerpAPIWrapper


def get_search_url(text: str) -> str:
    """Search for a Wikipedia page URL using Google Search (via SerpAPI)."""
    search = SerpAPIWrapper()
    res = search.run(f"{text} site:en.wikipedia.org")
    return res

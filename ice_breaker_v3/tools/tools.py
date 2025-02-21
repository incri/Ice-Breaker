from langchain.serpapi import SerpAPIWrapper


def get_search_url(text: str) -> str:
    """search for person in wikipedia"""
    search = SerpAPIWrapper()
    res = search.run(f"{text}")
    return res

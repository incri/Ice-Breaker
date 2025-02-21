import requests


def get_wikipedia_data(person_name: str):
    """Fetches Wikipedia summary and image for a given person."""
    url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "format": "json",
        "titles": person_name,
        "prop": "extracts|pageimages",
        "exintro": True,
        "explaintext": True,
        "redirects": True,
        "pithumbsize": 500,
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        pages = data["query"]["pages"]
        page_id = next(iter(pages))
        page_data = pages[page_id]

        summary_text = page_data.get("extract", "No summary available.")
        thumbnail_url = page_data.get("thumbnail", {}).get("source", None)

        return {"summary": summary_text, "thumbnail": thumbnail_url}
    else:
        return {"error": f"Failed to fetch Wikipedia data: {response.status_code}"}

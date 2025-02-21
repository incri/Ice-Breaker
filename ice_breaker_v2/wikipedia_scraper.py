import requests


def get_wikipedia_data(person_name):
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

        thumbnail_url = page_data.get("thumbnail", {}).get("source", None)

        return {"response": data, "thumbnail": thumbnail_url}
    else:
        return {"error": response.status_code}

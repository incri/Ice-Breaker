import requests


def get_wikipedia_data(person_name):
    # Wikipedia API endpoint for querying the data
    url = f"https://en.wikipedia.org/w/api.php"

    # Parameters for the API request
    params = {
        "action": "query",
        "format": "json",
        "titles": person_name,
        "prop": "extracts|pageimages",  # Include pageimages to fetch image
        "exintro": True,  # Get only the introduction part
        "explaintext": True,  # Get plain text, not HTML
        "redirects": True,  # Follow redirects (in case there's a page redirect)
        "pithumbsize": 500,  # Limit image size
    }

    # Send the GET request to the Wikipedia API
    response = requests.get(url, params=params)

    # Check if the response is valid
    if response.status_code == 200:
        data = response.json()

        # Print the complete JSON response
        print("Complete response from Wikipedia API:")
        print(data)

        # Extract the page information
        pages = data["query"]["pages"]

        # Get the page ID (it will be a key, the value is the page content)
        page_id = next(iter(pages))
        page_data = pages[page_id]

        # If a valid extract is available, print it
        if "extract" in page_data:
            print(f"\nIntroduction of {person_name}:")
            print(page_data["extract"])

        # Check if an image is available
        if "thumbnail" in page_data:
            print(f"\nImage URL for {person_name}:")
            print(page_data["thumbnail"]["source"])
        else:
            print(f"No image found for {person_name}.")
    else:
        print(f"Error: {response.status_code}")


# Example usage
person_name = input("Enter the name of the person: ")
get_wikipedia_data(person_name)

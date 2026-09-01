import json
from urllib.parse import urlencode
from urllib.request import Request, urlopen

SEARCH_API_URL = "https://search.bus-hit.me/search"

def real_web_search(query):
    params = urlencode({
        "q": query,
        "format": "json",
        "language": "en"
    })

    url = f"{SEARCH_API_URL}?{params}"

    request = Request(
        url,
        headers={"User-Agent": "SR-Nexus/1.0"}
    )

    with urlopen(request, timeout=10) as response:
        data = json.loads(response.read().decode("utf-8"))

    results = []

    for item in data.get("results", [])[:10]:
        results.append({
            "title": item.get("title", ""),
            "url": item.get("url", ""),
            "description": item.get("content", "")
        })

    return results

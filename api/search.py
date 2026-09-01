import json
from urllib.request import Request, urlopen


# Put your NEW Serper API key here
SERPER_API_KEY = "YOUR_NEW_API_KEY"


def real_web_search(query):

    if not SERPER_API_KEY or SERPER_API_KEY == "YOUR_NEW_API_KEY":
        return []

    payload = json.dumps({
        "q": query,
        "num": 10
    }).encode("utf-8")

    request = Request(
        "https://google.serper.dev/search",
        data=payload,
        headers={
            "X-API-KEY": SERPER_API_KEY,
            "Content-Type": "application/json"
        },
        method="POST"
    )

    with urlopen(request, timeout=15) as response:

        data = json.loads(
            response.read().decode("utf-8")
        )

    results = []

    for item in data.get("organic", [])[:10]:

        results.append({
            "title": item.get("title", ""),
            "url": item.get("link", ""),
            "description": item.get("snippet", "")
        })

    return results        results.append({
            "title": item.get("title", ""),
            "url": item.get("link", ""),
            "description": item.get("snippet", "")
        })

    return results

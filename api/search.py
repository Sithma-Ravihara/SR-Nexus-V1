import os
import json
from urllib.request import Request, urlopen


def real_web_search(query):

    api_key = os.environ.get("ec08a4b3c6f32493e8719090424e67af2c080c39")

    if not api_key:
        return []

    data = json.dumps({
        "q": query,
        "num": 10
    }).encode("utf-8")

    request = Request(
        "https://google.serper.dev/search",
        data=data,
        headers={
            "X-API-KEY": api_key,
            "Content-Type": "application/json"
        },
        method="POST"
    )

    with urlopen(request, timeout=15) as response:
        result = json.loads(
            response.read().decode("utf-8")
        )

    results = []

    for item in result.get("organic", [])[:10]:

        results.append({
            "title": item.get("title", ""),
            "url": item.get("link", ""),
            "description": item.get("snippet", "")
        })

    return results

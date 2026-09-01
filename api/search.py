import json
from urllib.parse import urlencode
from urllib.request import Request, urlopen


# මේක දැනට placeholder එකක්.
# Working search provider එක තෝරගත්තට පස්සේ මෙතන URL එක දානවා.
SEARCH_API_URL = ""


def real_web_search(query):
    if not SEARCH_API_URL:
        return []

    params = urlencode({
        "q": query,
        "format": "json"
    })

    url = f"{SEARCH_API_URL}?{params}"

    request = Request(
        url,
        headers={
            "User-Agent": "SR-Nexus/1.0"
        }
    )

    with urlopen(request, timeout=10) as response:
        data = json.loads(
            response.read().decode("utf-8")
        )

    results = []

    for item in data.get("results", [])[:10]:
        results.append({
            "title": item.get("title", ""),
            "url": item.get("url", ""),
            "description": item.get(
                "content",
                item.get("description", "")
            )
        })

    return results

from http.server import BaseHTTPRequestHandler
import json
from urllib.parse import urlparse, parse_qs
from urllib.request import urlopen
from urllib.parse import urlencode


SEARXNG_URL = "https://YOUR-SEARXNG-INSTANCE/search"


def real_web_search(query):
    params = urlencode({
        "q": query,
        "format": "json",
        "language": "en"
    })

    url = f"{SEARXNG_URL}?{params}"

    with urlopen(url, timeout=10) as response:
        data = json.loads(response.read().decode("utf-8"))

    results = []

    for item in data.get("results", [])[:10]:
        results.append({
            "title": item.get("title", ""),
            "url": item.get("url", ""),
            "description": item.get("content", "")
        })

    return results


class handler(BaseHTTPRequestHandler):

    def do_GET(self):

        parsed = urlparse(self.path)
        params = parse_qs(parsed.query)

        query = params.get("q", [""])[0].strip()

        if not query:
            response = {
                "query": "",
                "count": 0,
                "results": []
            }

        else:
            try:
                results = real_web_search(query)

                response = {
                    "query": query,
                    "count": len(results),
                    "results": results
                }

            except Exception as e:
                response = {
                    "query": query,
                    "count": 0,
                    "results": [],
                    "error": "Real web search temporarily unavailable"
                }

        body = json.dumps(
            response,
            ensure_ascii=False
        ).encode("utf-8")

        self.send_response(200)

        self.send_header(
            "Content-Type",
            "application/json; charset=utf-8"
        )

        self.send_header(
            "Access-Control-Allow-Origin",
            "*"
        )

        self.send_header(
            "Content-Length",
            str(len(body))
        )

        self.end_headers()

        self.wfile.write(body)

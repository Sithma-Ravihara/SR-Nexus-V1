from http.server import BaseHTTPRequestHandler
import json
from urllib.parse import urlparse, parse_qs
import sys
import os

# Project root එක Python path එකට add කිරීම
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from backend.search import search_documents
from backend.ranking import rank_results


DOCUMENTS = [
    {
        "title": "Python Programming",
        "content": "Python is a popular programming language used for web development, AI, automation and data science.",
        "url": "https://www.python.org/"
    },
    {
        "title": "Artificial Intelligence",
        "content": "Artificial Intelligence allows computers to perform tasks that normally require human intelligence.",
        "url": "#"
    },
    {
        "title": "Web Development",
        "content": "Web development includes HTML, CSS, JavaScript and backend technologies.",
        "url": "#"
    },
    {
        "title": "Technology",
        "content": "Technology includes computers, software, artificial intelligence and modern digital systems.",
        "url": "#"
    },
    {
        "title": "Python Web Development",
        "content": "Python can be used for backend web development with frameworks such as FastAPI and Django.",
        "url": "https://www.python.org/"
    }
]


class handler(BaseHTTPRequestHandler):

    def do_GET(self):

        parsed = urlparse(self.path)
        params = parse_qs(parsed.query)

        query = params.get("q", [""])[0]

        if not query.strip():
            response = {
                "query": "",
                "count": 0,
                "results": []
            }

        else:

            # Step 1: Search
            results = search_documents(
                query,
                DOCUMENTS
            )

            # Step 2: Rank results
            results = rank_results(
                query,
                results
            )

            response = {
                "query": query,
                "count": len(results),
                "results": results
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

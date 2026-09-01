from http.server import BaseHTTPRequestHandler
import json
from urllib.parse import urlparse, parse_qs
import sys
import os

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from backend.ranking import rank_results
from api.search import real_web_search


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

                # Real Web Search
                results = real_web_search(query)

                # SR Nexus Ranking
                results = rank_results(
                    query,
                    results
                )

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
                    "error": "Web search temporarily unavailable"
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

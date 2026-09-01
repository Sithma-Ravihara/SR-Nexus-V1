import json
from urllib.parse import urlencode
from urllib.request import Request, urlopen


SEARCH_URL = "https://html.duckduckgo.com/html/"


def real_web_search(query):

    params = urlencode({
        "q": query
    })

    url = SEARCH_URL + "?" + params

    request = Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (compatible; SR-Nexus/1.0)"
        }
    )

    with urlopen(request, timeout=15) as response:
        html = response.read().decode(
            "utf-8",
            errors="ignore"
        )

    results = []

    # Simple HTML extraction
    from html.parser import HTMLParser

    class SearchParser(HTMLParser):

        def __init__(self):
            super().__init__()
            self.results = []
            self.current = None
            self.in_title = False
            self.in_description = False

        def handle_starttag(self, tag, attrs):

            attrs = dict(attrs)

            if tag == "a" and "result__a" in attrs.get(
                "class", ""
            ):
                self.current = {
                    "title": "",
                    "url": attrs.get("href", ""),
                    "description": ""
                }
                self.in_title = True

            elif (
                tag == "a"
                and "result__snippet" in attrs.get(
                    "class", ""
                )
            ):
                self.in_description = True

        def handle_data(self, data):

            if self.current:

                if self.in_title:
                    self.current["title"] += data

                elif self.in_description:
                    self.current["description"] += data

        def handle_endtag(self, tag):

            if tag == "a":

                if self.in_title:
                    self.in_title = False

                    if self.current:
                        self.results.append(
                            self.current
                        )
                        self.current = None

                self.in_description = False

    parser = SearchParser()
    parser.feed(html)

    return parser.results[:10]

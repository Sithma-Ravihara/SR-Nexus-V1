from http.server import BaseHTTPRequestHandler
import json
from urllib.parse import urlparse, parse_qs
import re


# ========================================
# SEARCH DOCUMENTS
# ========================================

def search_documents(query, documents):

    query = query.lower().strip()

    if not query:
        return []

    query_words = re.findall(
        r"\b\w+\b",
        query
    )

    results = []

    for document in documents:

        title = document.get(
            "title",
            ""
        ).lower()

        content = document.get(
            "content",
            ""
        ).lower()


        # Exact match
        if query in title or query in content:

            results.append(document)

            continue


        # Word matching
        title_words = set(
            re.findall(
                r"\b\w+\b",
                title
            )
        )

        content_words = set(
            re.findall(
                r"\b\w+\b",
                content
            )
        )


        if any(
            word in title_words or
            word in content_words
            for word in query_words
        ):

            results.append(document)


    return results


# ========================================
# RANK RESULTS
# ========================================

def rank_results(query, results):

    query = query.lower().strip()

    query_words = set(
        re.findall(
            r"\b\w+\b",
            query
        )
    )


    def score(result):

        title = result.get(
            "title",
            ""
        ).lower()

        content = result.get(
            "content",
            ""
        ).lower()


        title_words = set(
            re.findall(
                r"\b\w+\b",
                title
            )
        )

        content_words = set(
            re.findall(
                r"\b\w+\b",
                content
            )
        )


        points = 0


        # Exact title match
        if query in title:
            points += 20


        # Exact content match
        if query in content:
            points += 10


        # Word matches
        for word in query_words:

            if word in title_words:
                points += 8

            elif word in content_words:
                points += 3


        return points


    return sorted(
        results,
        key=score,
        reverse=True
    )


# ========================================
# SR NEXUS DOCUMENT DATABASE
# ========================================

DOCUMENTS = [

    {
        "title": "Python Programming",
        "content": (
            "Python is a popular programming language "
            "used for web development, AI, automation "
            "and data science."
        ),
        "url": "https://www.python.org/"
    },

    {
        "title": "Python Web Development",
        "content": (
            "Python can be used for backend web "
            "development with frameworks such as "
            "FastAPI and Django."
        ),
        "url": "https://fastapi.tiangolo.com/"
    },

    {
        "title": "Artificial Intelligence",
        "content": (
            "Artificial intelligence is a field of "
            "computer science focused on creating "
            "systems that can perform intelligent tasks."
        ),
        "url": "https://www.ibm.com/topics/artificial-intelligence"
    },

    {
        "title": "Web Development",
        "content": (
            "Web development involves creating websites "
            "and web applications using HTML, CSS, "
            "JavaScript and backend technologies."
        ),
        "url": "https://developer.mozilla.org/"
    },

    {
        "title": "FastAPI",
        "content": (
            "FastAPI is a modern Python framework for "
            "building high performance APIs."
        ),
        "url": "https://fastapi.tiangolo.com/"
    },

    {
        "title": "JavaScript",
        "content": (
            "JavaScript is a programming language widely "
            "used to create interactive web pages and "
            "modern web applications."
        ),
        "url": "https://developer.mozilla.org/en-US/docs/Web/JavaScript"
    }

]


# ========================================
# VERCEL HANDLER
# ========================================

class handler(BaseHTTPRequestHandler):

    def do_GET(self):

        parsed = urlparse(
            self.path
        )

        params = parse_qs(
            parsed.query
        )

        query = params.get(
            "q",
            [""]
        )[0].strip()


        # Empty search
        if not query:

            response = {
                "query": "",
                "count": 0,
                "results": []
            }

        else:

            # Search
            results = search_documents(
                query,
                DOCUMENTS
            )


            # Ranking
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


        # HTTP response
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
            "Access-Control-Allow-Methods",
            "GET, OPTIONS"
        )

        self.send_header(
            "Access-Control-Allow-Headers",
            "*"
        )

        self.send_header(
            "Content-Length",
            str(len(body))
        )

        self.end_headers()

        self.wfile.write(body)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from search import search_documents
from ranking import rank_results


app = FastAPI(
    title="SR Nexus Search API",
    version="2.0.0"
)


# ========================================
# CORS
# ========================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ========================================
# SEARCH DATABASE
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
            "building APIs with high performance."
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
# HOME
# ========================================

@app.get("/")
def home():

    return {
        "name": "SR Nexus Search API",
        "status": "online",
        "version": "2.0.0"
    }


# ========================================
# SEARCH
# ========================================

@app.get("/api/search")
def search(q: str = ""):

    query = q.strip()


    # Empty query
    if not query:

        return {
            "query": "",
            "count": 0,
            "results": []
        }


    # Search documents
    results = search_documents(
        query,
        DOCUMENTS
    )


    # Rank results
    results = rank_results(
        query,
        results
    )


    return {
        "query": query,
        "count": len(results),
        "results": results
    }

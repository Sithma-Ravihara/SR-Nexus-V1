from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="SR Nexus Search API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {
        "name": "SR Nexus Search API",
        "status": "online"
    }


@app.get("/api/search")
def search(q: str = ""):

    q = q.strip()

    if not q:
        return {
            "query": "",
            "results": []
        }

    return {
        "query": q,
        "results": [
            {
                "title": f"SR Nexus result for {q}",
                "url": "#",
                "description": "Search engine backend is working."
            }
        ]
  }

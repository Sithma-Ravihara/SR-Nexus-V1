def search_documents(query, documents):
    query = query.lower().strip()

    if not query:
        return []

    return [
        document
        for document in documents
        if query in document.get("title", "").lower()
        or query in document.get("content", "").lower()
    ]

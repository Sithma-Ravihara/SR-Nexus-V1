def search_documents(query, documents):
    query = query.strip().lower()

    if not query:
        return []

    query_words = query.split()
    results = []

    for document in documents:
        title = document.get("title", "")
        content = document.get("content", "")
        url = document.get("url", "")

        text = f"{title} {content}".lower()

        score = 0

        # Exact query match
        if query in title.lower():
            score += 10

        if query in content.lower():
            score += 5

        # Individual word matching
        for word in query_words:
            if word in title.lower():
                score += 4

            if word in content.lower():
                score += 2

        if score > 0:
            results.append({
                "title": title,
                "url": url,
                "description": content,
                "score": score
            })

    return results

import re


def search_documents(query, documents):
    query = query.lower().strip()

    if not query:
        return []

    query_words = re.findall(r"\b\w+\b", query)

    results = []

    for document in documents:
        title = document.get("title", "").lower()
        content = document.get("content", "").lower()

        # Exact phrase match
        if query in title or query in content:
            results.append(document)
            continue

        # Word-based matching
        title_words = set(re.findall(r"\b\w+\b", title))
        content_words = set(re.findall(r"\b\w+\b", content))

        if any(word in title_words or word in content_words for word in query_words):
            results.append(document)

    return results

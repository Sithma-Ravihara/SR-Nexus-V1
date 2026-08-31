import re


def rank_results(query, results):

    query = query.lower().strip()
    query_words = re.findall(r"\b\w+\b", query)

    def score(result):

        title = result.get("title", "").lower()
        content = result.get("content", "").lower()

        title_words = set(re.findall(r"\b\w+\b", title))
        content_words = set(re.findall(r"\b\w+\b", content))

        points = 0

        # Exact phrase in title
        if query in title:
            points += 20

        # Exact phrase in content
        if query in content:
            points += 5

        # Individual query words
        for word in query_words:

            if word in title_words:
                points += 10

            if word in content_words:
                points += 3

        return points

    return sorted(
        results,
        key=score,
        reverse=True
    )

import re


def rank_results(query, results):

    query = query.lower().strip()

    if not query:
        return []


    query_words = set(
        re.findall(r"\b\w+\b", query)
    )


    def score(result):

        title = result.get(
            "title", ""
        ).lower()

        content = result.get(
            "content",
            result.get("description", "")
        ).lower()


        title_words = set(
            re.findall(r"\b\w+\b", title)
        )

        content_words = set(
            re.findall(r"\b\w+\b", content)
        )


        points = 0


        # Exact query in title
        if query in title:
            points += 20


        # Exact query in content
        if query in content:
            points += 10


        # Individual query words
        for word in query_words:

            if word in title_words:
                points += 8

            elif word in content_words:
                points += 3


        return points


    ranked = sorted(
        results,
        key=score,
        reverse=True
    )


    return ranked

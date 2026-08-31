def rank_results(query, results):

    query = query.lower().strip()

    def score(result):
        title = result.get("title", "").lower()
        content = result.get("content", "").lower()

        points = 0

        if query in title:
            points += 10

        if query in content:
            points += 5

        return points

    return sorted(
        results,
        key=score,
        reverse=True
    )

def calculate_risk(serverity: str):

    scores = {
        "low": 20,
        "medium": 50,
        "high": 80,
        "critical": 100
    }

    return scores.get(serverity.lower(), 0)
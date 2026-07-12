def calculate_risk(severity: str) -> int:

    scores = {
        "low": 20,
        "medium": 50,
        "high": 80,
        "critical": 100
    }

    return scores.get(severity.lower(), 0)
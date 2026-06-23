def calculate_risk(severity):

    scores = {
        "low": 20,
        "medium": 50,
        "high": 80,
        "critical": 100
    }

    return scores.get(severity, 0)
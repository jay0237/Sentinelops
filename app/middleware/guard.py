from better_profanity import profanity

blocked_words = {
    "hack": 8,
    "bypass": 7,
    "exploit": 9,
    "malware": 10,
    "phishing": 9,
    "ddos": 8,
    "ransomware": 10,
    "trojan": 9,
    "worm": 7
}


def scan_prompt(prompt: str):

    prompt_lower = prompt.lower()

    for word, score in blocked_words.items():

        if word in prompt_lower:

            return {
                "safe": False,
                "threat_level": "high",
                "score": score,
                "reason": f"Blocked Word Detected: {word}"
            }

    if profanity.contains_profanity(prompt):

        return {
            "safe": False,
            "threat_level": "medium",
            "score": 5,
            "reason": "Toxic Content Detected"
        }

    return {
        "safe": True,
        "threat_level": "low",
        "score": 0,
        "reason": "Prompt is Safe"
    }
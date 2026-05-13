from better_profanity import profanity

blocked_words = [
    "hack",
    "bypass",
    "exploit",
    "exploit"
    "vulnerability",
    "malware",
    "phishing",
    "ddos",
    "ransomware",
    "trojan",
    "worm"
]

def scan_prompt (prompt: str):

    prompt_lower = prompt.lower()

    for word in blocked_words:
        if word in prompt_lower:
            return{
                "safe": False,
                "reason": f"Blocked Word Detected: {word} "
            }

            if profanity.contains_profanity(prompt):
                return {
                    "safe": False,
                    "reason": "Toxic Content has been detected"
                }

                return {
                    "safe": True,
                    "reason": "Your Prompt is Safe"
                }


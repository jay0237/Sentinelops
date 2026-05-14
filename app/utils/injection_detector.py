injection_patterns = [
    "ignore previous instructions",
    "reveal system prompt",
    "bypass security",
    "act as root",
    "ignore all rules"
]

def detect_prompt_injection(prompt: str):

    prompt_lower = prompt.lower()

    for pattern in injection_patterns:

        if pattern in prompt_lower:

            return {
                "injection_detected": True,
                "reason": f"Injection detected for pattern: {pattern}"
            }

    return {
        "injection_detected": False
    }
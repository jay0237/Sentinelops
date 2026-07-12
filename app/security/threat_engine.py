import re
from typing import Any

from sqlalchemy.orm import Session

from app.security.rule_loader import load_rules
from app.security.risk_score import calculate_risk
from app.security.severity import SEVERITY_ORDER


def _match_rule(text: str, rule: Any) -> bool:
    rule_type = (rule.rule_type or "keyword").lower()

    if rule_type == "regex":
        pattern = rule.pattern or rule.keyword

        try:
            return bool(re.search(pattern, text, re.IGNORECASE))
        except re.error:
            return False

    return rule.keyword.lower() in text


def _serialize_rule(rule: Any) -> dict[str, Any]:
    return {
        "id": rule.id,
        "keyword": rule.keyword,
        "category": rule.category,
        "severity": rule.severity,
        "reason": rule.reason,
        "is_active": rule.is_active,
        "rule_type": rule.rule_type,
        "pattern": rule.pattern,
        "created_at": rule.created_at,
    }


def scan_threat(text: str, db: Session, original_text: str | None = None):
    original_prompt = original_text or text
    sanitized_text = text
    normalized_text = sanitized_text.lower()

    rules = load_rules(db)
    matches = [rule for rule in rules if _match_rule(normalized_text, rule)]

    if not matches:
        return {
            "safe": True,
            "severity": "low",
            "reason": "No Threat Detected",
            "category": "None",
            "risk_score": 0,
            "original_text": original_prompt,
            "sanitized_text": sanitized_text,
            "matched_rules": [],
        }

    highest = max(matches, key=lambda rule: SEVERITY_ORDER.get(rule.severity.lower(), 0))

    return {
        "safe": False,
        "severity": highest.severity.lower(),
        "reason": highest.reason,
        "category": highest.category,
        "risk_score": calculate_risk(highest.severity),
        "original_text": original_prompt,
        "sanitized_text": sanitized_text,
        "matched_rules": [_serialize_rule(rule) for rule in matches],
    }


# Backward compatibility
analyze_text = scan_threat
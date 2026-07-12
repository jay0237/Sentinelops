from pydantic import BaseModel, ConfigDict, Field

from app.schemas.threat_rule import ThreatRuleResponse


class PromptScanRequest(BaseModel):
    text: str = Field(min_length=1)


class ScanResponse(BaseModel):
    safe: bool
    severity: str
    category: str
    reason: str
    risk_score: int
    original_text: str
    sanitized_text: str
    matched_rules: list[ThreatRuleResponse]

    model_config = ConfigDict(from_attributes=True)
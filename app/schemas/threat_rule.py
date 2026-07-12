from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, model_validator


class ThreatRuleBase(BaseModel):
    keyword: str = Field(min_length=1)
    category: str = Field(min_length=1)
    severity: str = Field(min_length=1)
    reason: str = Field(min_length=1)
    is_active: bool = True
    rule_type: str = "keyword"
    pattern: Optional[str] = None

    @model_validator(mode="after")
    def validate_rule_definition(self):
        rule_type = self.rule_type.lower()

        if rule_type not in {"keyword", "regex"}:
            raise ValueError("rule_type must be either 'keyword' or 'regex'")

        if rule_type == "regex" and not self.pattern:
            raise ValueError("pattern is required when rule_type is 'regex'")

        self.rule_type = rule_type
        return self


class ThreatRuleCreate(ThreatRuleBase):
    pass


class ThreatRuleResponse(ThreatRuleBase):
    id: int
    created_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
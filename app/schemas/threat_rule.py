from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ThreatRuleBase(BaseModel):
    keyword: str
    category: str
    severity: str
    reason: str
    is_active: bool = True


class ThreatRuleCreate(ThreatRuleBase):
    pass


class ThreatRuleResponse(ThreatRuleBase):
    id: int
    created_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)
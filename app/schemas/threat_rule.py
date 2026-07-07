from pdyantic import BaseModel

class ThreatRule(BaseModel):
    keyword: str
    category: str
    severity: str
    reason: str

class ThreatRuleCreate(ThreatRule):
    id: int
    keyword: str
    category: str
    severity: str
    reason:str
    is_active: bool

    class Config:
        form_mode = True
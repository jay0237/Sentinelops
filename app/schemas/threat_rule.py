from pdyantic import BaseModel

class ThreatRule(BaseModel):
    keyword: str
    category: str
    severity: str
    reason: str

    
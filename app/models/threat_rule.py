from sqlchemy import Column, String, Boolean, DataTime
from sqlchemy.sql import func

from app.config.base import Base

class ThreatRule(Base):

    __tablename__ = "threat_rules"

    id = Column(Integer, primary_key=True, index=True)
    keyword = Column(String, nullable=False, unique=True)
    category = Column(String, nullable=False)
    severity = Column(String, nullable=False)
    reason = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DataTime(timezone=True), server_default=func.now())
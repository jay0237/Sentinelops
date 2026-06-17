from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

from app.config.base import Base

class PromptLog(Base):

    __tablename__ = "prompt_logs"

    id = Column(Integer, primary_key=True)

    prompt = Column(String)

    status = Column(String)

    reason = Column(String)

    severity = Column(String)

    timestamp = Column(
        DateTime,
        default=datetime.utcnow
    )
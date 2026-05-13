from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime

from app.config.base import Base

class PromptLog (Base):

    __tablename__ = "prompt_logs"

    id = Column(Integer, primary_key=True, index=True)

    prompt = Column(String)

    status = Column(String)

    reason = Column(String)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )



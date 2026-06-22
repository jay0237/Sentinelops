from sqlalchemy import Column, Integer, String, Boolean
from app.config.base import Base

class ApiKey(Base):

    __tablename__ = "api_keys"

    id = Column(Integer, primary_key=True)

    key = Column(String, unique=True)

    owner = Column(String)

    is_active = Column(Boolean, default=True)
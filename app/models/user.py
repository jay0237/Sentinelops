from sqlalchemy import Column, Integer, String
from app.config.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=False)
    email = Column(String, unique=True, index=False)
    password = Column(String, nullable=False)
    

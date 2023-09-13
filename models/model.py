from sqlalchemy import Column, Integer, String
from core.config import Base
from pydantic import BaseModel

class UserCreate(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(40))
    senha = Column(String(12))
    email = Column(String(80))

class Token(BaseModel):
    access_token: str
    token_type: str



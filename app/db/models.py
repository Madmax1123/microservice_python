from sqlalchemy import Column, Integer, String
from app.db.base import Base

class user(Base):
    __tablename__ = 'users'
    id = Column('', Integer, primary_key=True, autoincrement=True)
    nome = Column('name', String, nullable=False)
    senha = Column('senha', String, nullable=False)
    email = Column('email', String, nullable=False)
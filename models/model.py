from sqlalchemy import Column, Integer, String
from config.config import Base

class CadastroConf(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(40))
    senha = Column(String(12))
    email = Column(String(80))
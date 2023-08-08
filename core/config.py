from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# define a rota do banco de dados
DATABASE_URL = "mysql+pymysql://user:userpass@localhost:3306/db"

# Chave secreta para JWT
JWT_SECRET = 'plEhYlIHpMxIwJrvwxAzTd9zxy4sRtL-UEkW9C_213s'
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Se conecta ao banco de dados
engine = create_engine(DATABASE_URL)

# Cria uma instancia da sessao configurada ao engine
SessionLocal = sessionmaker(bind=engine)

# Cria uma instância de uma classe base para os models que representa a tabela no banco de dados
Base = declarative_base()

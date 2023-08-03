from config.config import Base, engine
from models.model import CadastroConf

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine) 
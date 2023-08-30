from passlib.context import CryptContext


CRIPTO = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_pass(senha: str) -> str:
    return CRIPTO.hash(senha)
from passlib.context import CryptContext


CRIPTO = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(password: str, hash_password: str) -> bool:
    return CRIPTO.verify(password, hash_password)

def hash_pass(senha: str) -> str:
    return CRIPTO.hash(senha)
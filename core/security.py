from passlib.context import CryptContext


CRIPTO = CryptContext(schemes=["bcrypt"], deprecated="auto")
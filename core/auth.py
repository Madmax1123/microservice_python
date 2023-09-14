from datetime import datetime, timedelta, timezone
from core.config import JWT_SECRET, ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SessionLocal
from core.security import verify_password
from models.model import UserCreate
import jwt


def create_access_token(sub: dict, expires_delta: timedelta | None = None):
    to_encode = sub.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=ALGORITHM)
    return encoded_jwt


def authlogin(username: str, password: str):
    db = SessionLocal()
    user = db.query(UserCreate).filter(UserCreate.nome == username).first()

    if not user:
        return None
    if not verify_password(password, user.senha):
        return None

    return user


from datetime import datetime, timedelta, timezone
from .config import JWT_SECRET, ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM
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

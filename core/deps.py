from core.config import JWT_SECRET, ALGORITHM, SessionLocal, API_ROUTE
from core.security import verify_password
from models.model import UserCreate
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.exceptions import HTTPException
from fastapi import status, Depends
from typing import Annotated
import jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{API_ROUTE}")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciais invalidas",
        headers={"WWW-Authenticate": "Bearer"},
    )        
    payload = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM])

    db = SessionLocal()
    user = db.query(UserCreate).filter(UserCreate.nome == UserCreate.nome).first()
    password = ""
    password_user = verify_password(password, user.senha)

    return user

def get_current_active_user(
    current_user: Annotated[UserCreate, Depends(get_current_user)]
):
    if not current_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
    return current_user
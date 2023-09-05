from core.config import JWT_SECRET, ALGORITHM, SessionLocal
from core.security import verify_password
from models.model import CadastroConf
from fastapi.security import OAuth2PasswordBearer
from fastapi.exceptions import HTTPException
from fastapi import status, Depends
from typing import Annotated
import jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciais invalidas",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        db = SessionLocal()
        user = db.query(CadastroConf).filter(CadastroConf.nome == form_data.username).first()
        password_user = verify_password(form_data.password, user.senha)
    except :
        raise credentials_exception
    if user or password_user is None:
        raise credentials_exception
    return user

def get_current_active_user(
    current_user: Annotated[CadastroConf, Depends(get_current_user)]
):
    if current_user.disabled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
    return current_user
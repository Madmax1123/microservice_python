from datetime import datetime, timedelta
from typing import Annotated
from fastapi import FastAPI, status, Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from fastapi.exceptions import HTTPException
from core.auth import create_access_token
from core.config import SessionLocal, ACCESS_TOKEN_EXPIRE_MINUTES, API_ROUTE
from core.security import verify_password, hash_pass
from core.deps import get_current_active_user, get_current_user
from models.model import UserCreate, Token
from schema import Cadastro



# Rota para test
app = FastAPI()

# Rota para fazer cadastro de um novo usuario com um auto increment de id
@app.post('/cadastro', status_code=status.HTTP_201_CREATED)
def create_user(user: Cadastro):
    # Criar uma instância do modelo CadastroConf com os dados do usuário recebido
    new_user = UserCreate(nome=user.nome, senha=hash_pass(user.senha), email=user.email)

    # Abre uma sessao
    db = SessionLocal()
    existing_user = db.query(UserCreate).filter_by(email=user.email).first()
    if existing_user:
        db.close()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="E-mail already used",
            headers={"WWW-Authenticate": "Bearer"}
        )
    else:
        # pega os dados e adiociona na db
        db.add(new_user)
         # coloca na db
        db.commit()
        db.close()
    return new_user


# Rota para fazer login utilizando e-mail e senha existentes
@app.post(f'{API_ROUTE}', status_code=status.HTTP_200_OK)
def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    # Abre uma sessao
    db = SessionLocal()
    user = db.query(UserCreate).filter(form_data.username == form_data.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not verify_password(form_data.password, user.senha):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = ACCESS_TOKEN_EXPIRE_MINUTES
    access_token = create_access_token(
        sub={"sub": user.nome}
    )
    if user:
        db.close()
    return {"access_token": access_token, "token_type": "bearer"}

# Rota para alterar senha utilizando o e-mail
@app.put('/esqueci_minha_pass', status_code=status.HTTP_200_OK)
def red_pass(email, senha):
    # Abre uma sessao
    db = SessionLocal()

    # faz uma busca do usuario por e-mail
    user = db.query(UserCreate).filter_by(email=email).first()

    # Se o usuario for encontrado e a senha tiver sido colocada, ela sera alterada
    if user:
        user.senha = senha
        db.commit()
        db.close()
        return "senha alterada"

@app.delete(f'{API_ROUTE}/users/delete', status_code=status.HTTP_200_OK)
def delete_user_by_id(
    current_user: Annotated[None, Depends(get_current_active_user)], user_id
    ):    
    # Abre uma sessao
    db = SessionLocal()

    # Busca o usuario pelo id
    user = db.query(UserCreate).filter_by(id=user_id).first()

    # Se o usuario foi encontrado, ele vai ser excluido
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"USER NOT FOUND OR ALREADY DELETED WITH ID {user_id}")
    else:
        db.delete(user)
        db.commit()
        db.close()      
    return {f"Usuario {user_id} deletado"}
    
    

# Lista o id, nome, email e senha dos usuarios
@app.get(f'/users', status_code=status.HTTP_302_FOUND)
def get_all_users(get_user: Annotated[None, Depends(get_current_user)]   ):
    db = SessionLocal()
    users = db.query(UserCreate).all()
    return users



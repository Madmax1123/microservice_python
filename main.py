from datetime import datetime, timedelta
from typing import Annotated
from fastapi import FastAPI, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.exceptions import HTTPException
from core.auth import create_access_token
from core.config import SessionLocal, ACCESS_TOKEN_EXPIRE_MINUTES
from core.security import hash_pass
from models.model import CadastroConf, Token
from schema import Cadastro



# Rota para test
app = FastAPI()

# Rota para fazer cadastro de um novo usuario com um auto increment de id
@app.post('/cadastro', status_code=status.HTTP_201_CREATED)
def create_user(user: Cadastro):
    # Criar uma instância do modelo CadastroConf com os dados do usuário recebido
    new_user = CadastroConf(nome=user.nome, senha=hash_pass(user.senha), email=user.email)

    # Abre uma sessao
    db = SessionLocal()
    # pega os dados e adiociona na db
    db.add(new_user)
    # coloca na db
    db.commit()
    db.refresh(new_user)
    db.close()
    return new_user


# Rota para fazer login utilizando e-mail e senha existentes
@app.post('/login', status_code=status.HTTP_200_OK)
def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    # Abre uma sessao
    db = SessionLocal()
    user = db.query(CadastroConf).filter(CadastroConf.nome == form_data.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
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
    user = db.query(CadastroConf).filter_by(email=email).first()

    # Se o usuario for encontrado e a senha tiver sido colocada, ela sera alterada
    if user:
        user.senha = senha
        db.commit()
        db.close()
        return "senha alterada"

@app.delete('/users/delete', status_code=status.HTTP_204_NO_CONTENT)
def delete_user_by_id(user_id):
    # Abre uma sessao
    db = SessionLocal()

    # Busca o usuario pelo id
    user = db.query(CadastroConf).filter_by(id=user_id).first()

    # Se o usuario foi encontrado, ele vai ser excluido
    if user:
        db.delete(user)
        db.commit()
        db.close()
    return {"Usuario deletado"}
    

# Lista o id, nome, email e senha dos usuarios
@app.get('/users', status_code=status.HTTP_302_FOUND)
def get_all_users():
    db = SessionLocal()
    users = db.query(CadastroConf).all()
    return users


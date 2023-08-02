from fastapi import FastAPI, HTTPException

# import da classe Cadastro de usuario
from model import Cadastro


#arquivo contendo os usuarios
users = [
    {
        "id": 1,
        "nome": "name1",
        "senha": "password1",
        "email": "email1@email.com"
    },
    {
        "id": 2,
        "nome": "name2",
        "senha": "password2",
        "email": "email2@email.com"
    },
    {
        "id": 3,
        "nome": "name3",
        "senha": "password3",
        "email": "email3@email.com"
    }
]


# Rota para test
app = FastAPI()
@app.get('/noob')
def check():
    return True 


# Listando o nome, email e senha dos usuarios
@app.get('/users/')
def get_all_users():
    return users


# Rota para fazer cadastro de um novo usuario com um auto increment de id
@app.post('/cadastro/')
def create_user(user: Cadastro):
    # Passando pelo tamanho dos usuarios (id) e somando mais um
    user_id = len(users) + 1 
    user.id = user_id
    users.append(user.dict())
    return user


# Rota para fazer login utilizando e-mail e senha existentes
@app.get('/login/')
def get_users(email: str, senha: str):
    for user in users:
        if user['email'] == email and user['senha'] == senha:
            return user['email'], user['senha']
    raise HTTPException(status_code=404, detail="BOTA A CREDENCIAL CERTA AI")


# Rota para alterar senha utilizando o e-mail
@app.put('/esqueci_minha_pass')
def red_pass(email: str, senha: str):
    for user in users:
        # Passando pelos usuarios utilizando o e-mail
        if user['email'] == email:
            # Redefinindo para a senha colocada no campo
            user['senha'] = senha
            return {"senha alterada"}
    # Erro caso o usuario nao seja encontrado
    raise HTTPException(status_code=404, detail="Usuario nao encontrado")


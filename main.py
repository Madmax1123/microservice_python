from fastapi import FastAPI, HTTPException, status
from config.config import SessionLocal
from models.model import CadastroConf
# import da classe Cadastro de usuario
from schema import Cadastro


#arquivo contendo os usuarios
"""
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
"""

# Rota para test
app = FastAPI()
@app.get('/noob')
def check():
    return True 


# Listando o nome, email e senha dos usuarios
@app.get('/users/')
def get_all_users():
    db = SessionLocal()
    users = db.query(CadastroConf).all()
    return users


# Rota para fazer cadastro de um novo usuario com um auto increment de id
@app.post('/cadastro/', status_code=status.HTTP_201_CREATED, response_model=Cadastro)
def create_user(user: Cadastro):
    # Criar uma instância do modelo CadastroConf com os dados do usuário recebido
    new_user = CadastroConf(nome=user.nome, senha=user.senha, email=user.email)

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
@app.get('/login/')
def get_users(email: str, senha: str):
    # Abre uma sessao
    db = SessionLocal()
    user = db.query(CadastroConf).filter_by(email=email, senha=senha).first()
    
    if user:
        db.close()
    return user

@app.delete('/users/delete/')
def delete_user_by_id(user_id: int):
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
    


# Rota para alterar senha utilizando o e-mail
@app.put('/esqueci_minha_pass')
def red_pass(email: str, senha: str):
    # abri uma sessao no banco de dados
    db = SessionLocal()

    # faz uma busca do usuario por e-mail
    user = db.query(CadastroConf).filter_by(email=email).first()

    # Se o usuario for encontrado e a senha tiver sido colocada, ela sera alterada
    if user:
        user.senha = senha
        db.commit()
        db.close()
        return "senha alterada"
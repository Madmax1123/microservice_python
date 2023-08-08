from fastapi import FastAPI, status
from core.config import SessionLocal
from fastapi.security import OAuth2PasswordBearer
from models.model import CadastroConf
# import da classe Cadastro de usuario
from schema import Cadastro

# Rota para test
app = FastAPI()

# Rota para fazer cadastro de um novo usuario com um auto increment de id
@app.post('/cadastro', status_code=status.HTTP_201_CREATED)
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
@app.get('/login', status_code=status.HTTP_302_FOUND)
def get_users(email: str, senha: str):
    # Abre uma sessao
    db = SessionLocal()
    user = db.query(CadastroConf).filter_by(email=email, senha=senha).first()
    
    if user:
        db.close()
    return user

# Rota para alterar senha utilizando o e-mail
@app.put('/esqueci_minha_pass', status_code=status.HTTP_200_OK)
def red_pass(email: str, senha: str):
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
    

# Lista o id, nome, email e senha dos usuarios
@app.get('/users', status_code=status.HTTP_302_FOUND)
def get_all_users():
    db = SessionLocal()
    users = db.query(CadastroConf).all()
    return users


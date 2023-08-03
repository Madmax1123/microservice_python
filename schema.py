from pydantic import BaseModel
from typing import Optional

# classe cadastro do usuario
class Cadastro(BaseModel):
    # Setando o id como opicional, assim nao precisando botar ele em um cadastro
    id: Optional[int] = None
    nome: str
    senha: str
    email: str

#BaseModel Pydantic
#Definir e validar os dados de entrada e saída da API
from pydantic import BaseModel, Field, ConfigDict, field_validator
from typing import Optional
#Representa os dados para criar um produto através da API

class CriarProduto(BaseModel):
    nome: str = Field(min_length=1, max_length=100)
    descricao: str = Field(max_length=255)
    preco: float = Field(gt=0)
    estoque: int = Field(ge=0)

class AtualizarProduto(BaseModel):
    nome: Optional[str] = Field(default=None, min_length=1, max_length=100)
    descricao: Optional [str] = Field(default=None, max_length=255)
    preco: Optional [float] = Field(default=None, gt=0)
    estoque: Optional [int] =Field(default=None, ge=0) 

class Token(BaseModel):
    access_token: str
    token_type: str

class CriarUsuario(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    senha: str

    @field_validator("senha")
    @classmethod
    def validar_senha(cls, valor):
        if len(valor) < 6:
            raise ValueError("A senha deve ter pelo menos 6 caracteres")
        return valor
    
class UsuarioResposta(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    username: str


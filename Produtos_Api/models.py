
#Importação dos tipos das colunas que existirão nas colunas do banco de dados
from sqlalchemy import Column, Integer, String, Float

#Mapped representa um atributo que será mapeado para uma coluna do banco de dados
#mapped_column define as características da coluna do banco de dados
from sqlalchemy.orm import mapped_column, Mapped

#importação da base criada em database.py
from database import Base

#Essa classe representa a entidade produto no ORM
#Produto (Objeto python)
#Produtos (Tabela MySQL)

class Produto(Base):
    #nome da tabela que será representada no banco
    __tablename__ = "produtos"

    #chave primária da tabela produtos
    #MySQL Gerará automaticamente seu valor
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    #Nome do Produto
    #Varchar(100), obrigatório
    nome: Mapped[str] = mapped_column(String(100), nullable=False)

    #Descrição do Produto
    descricao: Mapped[str] = mapped_column(String(255), nullable=False)

    #Preço do Produto 
    preco: Mapped[float] = mapped_column(Float, nullable=False)

    #Quantidade disponível:
    estoque: Mapped[int] = mapped_column(Integer, nullable=False)

class Usuario(Base):
 __tablename__ = "usuarios"
 id: Mapped[int] = mapped_column(Integer,primary_key=True, autoincrement=True)

 username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)

 senha_hash: Mapped[str] = mapped_column(String(255), nullable=False)

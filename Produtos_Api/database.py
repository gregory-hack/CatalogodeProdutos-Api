import os

# Criação do SQLAlchemy para interagir com o banco de dados
from sqlalchemy import create_engine

#Session Maker para criar sessões de banco de dados
from sqlalchemy.orm import sessionmaker

#Declarative Base para criar modelos de banco de dados
from sqlalchemy.orm import DeclarativeBase

from dotenv import load_dotenv

class Base (DeclarativeBase):
    pass 

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
   raise RuntimeError("Defina a DATABASE_URL no arquivo .env")

#Engine: confuguração entre o SQLAlchemy e o banco de dados
engine = create_engine(DATABASE_URL)

#Fábrica de sessões
#Cada Endpoint poderá abrir uma sessão para conversar com o banco de dados
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_banco():
    db =SessionLocal()
    try:
        yield db
    finally:
     db.close()


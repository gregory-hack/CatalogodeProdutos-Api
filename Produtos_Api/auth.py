import os
from datetime import datetime, timedelta, timezone

import jwt
from jwt.exceptions import InvalidTokenError
from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pwdlib import PasswordHash
from sqlalchemy.orm import Session

from database import get_banco
from models import Usuario

# Carrega as variáveis do arquivo .env
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise RuntimeError("Defina SECRET_KEY no arquivo .env")

ALGORITHM = "HS256"
EXPIRA_MINUTOS = 30

# Transforma a senha em hash e confere depois
password_hash = PasswordHash.recommended()

# Informa ao FastAPI e ao Swagger que o token vem do endpoint /login
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def gerar_hash(senha: str) -> str:
    return password_hash.hash(senha)


def verificar_senha(senha: str, senha_hash: str) -> bool:
    return password_hash.verify(senha, senha_hash)


def criar_token(username: str) -> str:
    # "sub" identifica o dono do token, "exp" define quando ele expira
    expira = datetime.now(timezone.utc) + timedelta(minutes=EXPIRA_MINUTOS)
    payload = {"sub": username, "exp": expira}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def usuario_logado(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_banco)
):
    erro = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="token inválido ou expirado",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        #confere a assinatura e a validade do token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise erro
    except InvalidTokenError:
        raise erro

    usuario = db.query(Usuario).filter(Usuario.username == username).first()
    if usuario is None:
        raise erro

    return usuario
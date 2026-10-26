
#Compilar: uvicorn main:app --reload
#Depends: fornece uma sessão do banco aos endpoints

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from auth import gerar_hash, verificar_senha, criar_token, usuario_logado

#Session: Sesssão do SQLAlchemy 

from sqlalchemy.orm import Session

#Importamos nossa configuração do banco de dados
from database import Base, engine, SessionLocal, get_banco

#importação do APIRouter para definir tag e prefixo uma vez somente
from fastapi import APIRouter

#Importação do ORM do produto:
from models import Produto, Usuario

#Importar o pydantic usado para receber os dados.
from schemas import CriarProduto, AtualizarProduto, Token, CriarUsuario, UsuarioResposta

#adição do CORS.
from fastapi.middleware.cors import CORSMiddleware

#Criar as tabelas que nao existem no banco de dados
#Utilizando os modelos ORM
Base.metadata.create_all(bind=engine)

tags_metada = [
    {"name": "Autenticação", "description": "Cadastro de usuários e login"},
    {"name": "Produtos", "description": "permite criar, consultar, atualizar e excluir um produto"} 

]


#Criação da Api
app = FastAPI( 
    
    title = "API de Produtos",
    description = "API para cadastro de produtos utilizando MySQL, FastAPI, Pydantic e SQLAlchemy",
    version = "1.0.0",
    openapi_tags=tags_metada,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000"],
    allow_methods=["GET", "POST", "PATCH", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)

router_produtos = APIRouter(prefix="/produtos", tags=["Produtos"])


@router_produtos.post(
    "",
    status_code=201,
    dependencies=[Depends(usuario_logado)],
    responses={
        401: {"description": "Token ausente, inválido ou expirado"},
    },
)

def criar_produto(
    p: CriarProduto,
    db: Session = Depends(get_banco)
):
    # p é o objeto Pydantic
    # Criar objeto modelo do ORM Produto
    novoProduto = Produto(
        nome=p.nome,
        descricao=p.descricao,
        preco=p.preco,
        estoque=p.estoque
    )

    # Adiciona novo objeto na sessão do banco de dados
    db.add(novoProduto)

    # Confirma a operação no banco de dados e persiste
    db.commit()

    # Atualiza o objeto com informações do banco, como o id gerado
    db.refresh(novoProduto)

    return novoProduto

@router_produtos.get("")
def listar_produtos(db: Session = Depends(get_banco)):

    # Consulta todos os produtos no banco de dados
    produtos = db.query(Produto).all()
    return produtos

@router_produtos.get("/{produto_id}",responses={404: {"description": "Produto não encontrado"}},)
def buscar_produto(
    produto_id: int,
    db: Session = Depends(get_banco)
):
    #procura um produto que a coluna ID seja igual ao ID recebido pela URL
    produto = (
        db.query(Produto).filter(Produto.id == produto_id).first()
    )

    if produto is None:
        raise HTTPException(
            status_code=404,
            detail="produto não encontrado"
        )

    return produto
            
@router_produtos.patch("/{produto_id}",responses={
    400: {"description": "Nenhum campo enviado para atualizar"},
    404: {"description": "Produto não encontrado"},
}
)
def atualizar_produto(
    produto_id: int,
    dados: AtualizarProduto,
    db: Session = Depends(get_banco)
):
    produto = (
        db.query(Produto).filter(Produto.id == produto_id).first()
    )

    if produto is None:
        raise HTTPException(
            status_code=404,
            detail="produto não encontrado"
        )

    campos = dados.model_dump(exclude_unset=True, exclude_none=True)

    if not campos:
        raise HTTPException(
            status_code=400,
            detail="Envie um campo para atualizar"
        )
    
    for campo, valor in campos.items():
        setattr(produto, campo, valor)

    db.commit()
    db.refresh(produto)

    return produto

@router_produtos.delete("/{produto_id}", status_code=204, responses={404: {"description": "Produto não encontrado"}})

def deletar_produto(
    produto_id: int,
    db: Session = Depends(get_banco)
):
    produto = (
        db.query(Produto).filter(Produto.id == produto_id).first()
    )

    if produto is None:
        raise HTTPException(
        status_code=404,
        detail="produto não encontrado"

    )

    db.delete(produto)
    db.commit()


@app.post(
    "/login",
    response_model=Token,
    tags=["Autenticação"],
    responses={401: {"description": "Usuário ou senha incorretos"}},
)

def login(
    form: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_banco)
):
    usuario = (
        db.query(Usuario).filter(Usuario.username == form.username).first()
    )


    if usuario is None or not verificar_senha(form.password, usuario.senha_hash):
        raise HTTPException(
            status_code=401,
            detail="usuário ou senha incorretos",
            headers={"WWW-Authenticate":"Bearer"},
        )

    return {
        "access_token": criar_token(usuario.username),
        "token_type": "bearer"
    }

@app.post(
    "/usuarios",
    response_model=UsuarioResposta,
    status_code=status.HTTP_201_CREATED,
    tags=["Autenticação"],
    responses={409: {"description": "Usuário já existe"}}
    )
def cadastrar_usuario(
    u: CriarUsuario,
    db: Session = Depends(get_banco)
):
    existente = (
        db.query(Usuario).filter(Usuario.username == u.username).first()
    )

    if existente is not None:
        raise HTTPException(
            status_code=409,
            detail="usuário já existe"
        )

    # Guarda o hash da senha, nunca a senha original
    novo = Usuario(
        username=u.username,
        senha_hash=gerar_hash(u.senha)
    )      
    db.add(novo)
    db.commit()
    db.refresh(novo)

    return novo

app.include_router(router_produtos)

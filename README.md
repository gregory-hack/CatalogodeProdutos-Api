## Autor

|Nome| Gregory Antunes Hack|
|---|--------|
|RU:| 3699000|


# API de Produtos

API REST para cadastro e gerenciamento de um catálogo de produtos, desenvolvida com **FastAPI**, **SQLAlchemy** e **MySQL**, com autenticação por **JWT**.

Projeto da Atividade Prática de *Arquitetura e Desenvolvimento de APIs* (Uninter, 2026).

## Sumário
1. [Autor](#autor)
2. [Descrição](#descrição)
3. [Tecnologias](#tecnologias)
4. [Estrutura do projeto](#estrutura-do-projeto)
5. [Pré-requisitos](#pré-requisitos)
6. [Instalação](#instalação)
7. [Configuração](#configuração)
8. [Executando a API](#executando-a-api)
9. [Endpoints](#endpoints)
10. [Modelo de dados e validações](#modelo-de-dados-e-validações)
11. [Autenticação](#autenticação)
12. [CORS](#cors)
13. [Exemplos de requisição](#exemplos-de-requisição)
14. [Roteiro de testes](#roteiro-de-testes)
15. [Decisões de projeto](#decisões-de-projeto)
16. [Limitações conhecidas](#limitações-conhecidas)
17. [Solução de problemas](#solução-de-problemas)
---

## Descrição

A API permite cadastrar, consultar, atualizar e excluir produtos de um catálogo (nome, descrição, preço e estoque). Os dados são gravados em um banco MySQL e permanecem armazenados entre as execuções da aplicação.

A criação de produtos é protegida: apenas usuários autenticados podem cadastrar. O usuário se cadastra, faz login e recebe um token JWT, que deve ser enviado no cabeçalho `Authorization` das rotas protegidas.

## Tecnologias

| Item | Tecnologia |
|---|---|
| Linguagem | [![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org) |
| Framework | [![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com) |
| Servidor | [![Uvicorn](https://img.shields.io/badge/Uvicorn-499848?style=for-the-badge)](https://www.uvicorn.org) |
| Banco de dados | [![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white)](https://www.mysql.com) |
| ORM | [![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white)](https://www.sqlalchemy.org) [![PyMySQL](https://img.shields.io/badge/PyMySQL-4479A1?style=for-the-badge)](https://pymysql.readthedocs.io) |
| Validação | [![Pydantic](https://img.shields.io/badge/Pydantic-E92063?style=for-the-badge&logo=pydantic&logoColor=white)](https://docs.pydantic.dev) |
| Autenticação | [![JWT](https://img.shields.io/badge/JWT-000000?style=for-the-badge&logo=jsonwebtokens&logoColor=white)](https://jwt.io) [![PyJWT](https://img.shields.io/badge/PyJWT-4B5563?style=for-the-badge)](https://pyjwt.readthedocs.io) |
| Hash de senha | [![Argon2](https://img.shields.io/badge/Argon2-4B5563?style=for-the-badge)](https://github.com/P-H-C/phc-winner-argon2) [![pwdlib](https://img.shields.io/badge/pwdlib-4B5563?style=for-the-badge)](https://frankie567.github.io/pwdlib/) |
| Variáveis de ambiente | [![python-dotenv](https://img.shields.io/badge/python--dotenv-4B5563?style=for-the-badge)](https://github.com/theskumar/python-dotenv) |
| Documentação e testes | [![Swagger UI](https://img.shields.io/badge/Swagger_UI-85EA2D?style=for-the-badge&logo=swagger&logoColor=black)](https://swagger.io/tools/swagger-ui/) [![OpenAPI](https://img.shields.io/badge/OpenAPI-6BA539?style=for-the-badge)](https://www.openapis.org) |
| Consulta ao banco | [![MySQL Workbench](https://img.shields.io/badge/MySQL_Workbench-4479A1?style=for-the-badge&logo=mysql&logoColor=white)](https://www.mysql.com/products/workbench/) |



## Estrutura do projeto

```
Catálogo de Produtos-Api/
├── .gitignore
├── README.md
├── requirements.txt
└── Produtos_Api/
    ├── .env.example      # modelo das variáveis de ambiente
    ├── main.py           # aplicação, rotas e configuração de CORS
    ├── auth.py           # hash de senha, criação e validação do token JWT
    ├── database.py       # conexão com o banco e sessão
    ├── models.py         # modelos ORM (tabelas produtos e usuarios)
    ├── schemas.py        # esquemas Pydantic (entrada, saída e validação)
    └── banco.sql         # script de criação do banco e das tabelas
```

O arquivo `.env` (com os valores reais) é criado localmente e **não** é versionado.

## Pré-requisitos

- Python 3.10 ou superior (desenvolvido com Python 3.14)
- MySQL 8 em execução (por exemplo, com o MySQL Workbench para consultar os dados)
- Git

## Instalação

Na raiz do repositório (pasta `Catálogo de Produtos-Api`):

**1. Criar e ativar o ambiente virtual**

```bash
python -m venv .venv
```

Windows (PowerShell):

```powershell
.venv\Scripts\Activate
```

Linux ou macOS:

```bash
source .venv/bin/activate
```

**2. Instalar as dependências**

```bash
pip install -r requirements.txt
```

## Configuração

### 1. Banco de dados

Crie o banco e as tabelas executando o script `Produtos_Api/banco.sql`.

Pelo terminal, a partir da raiz do repositório:

```powershell
mysql -u root -p -e "source Produtos_Api/banco.sql"
```

Prompt de Comando (cmd), Linux ou macOS:

```bash
mysql -u root -p < Produtos_Api/banco.sql
```

Ou pelo MySQL Workbench: *File > Open SQL Script*, escolha `banco.sql` e execute tudo.

O script cria o banco `api_produtos` e as tabelas `produtos` e `usuarios`. Se as tabelas não existirem, a API também as cria sozinha ao iniciar, a partir dos modelos do SQLAlchemy.

### 2. Variáveis de ambiente

Entre na pasta `Produtos_Api` e copie o arquivo de exemplo:

```bash
cd Produtos_Api
copy .env.example .env      # Windows
cp .env.example .env        # Linux ou macOS
```

Abra o `.env` e preencha:

```
SECRET_KEY=valor_gerado_abaixo
DATABASE_URL=mysql+pymysql://USUARIO:SENHA@localhost/api_produtos
```

- **`SECRET_KEY`**: chave usada para assinar os tokens JWT. Gere uma com:

  ```bash
  python -c "import secrets; print(secrets.token_hex(32))"
  ```

- **`DATABASE_URL`**: usuário, senha e banco do seu MySQL. Se a senha tiver caracteres especiais (como `@`, `:`, `/` ou `#`), codifique-os na URL (por exemplo, `@` vira `%40`).


## Executando a API

Dentro da pasta `Produtos_Api` (onde está o `main.py`):

```bash
uvicorn main:app --reload
```

A API fica disponível em `http://127.0.0.1:8000`.

| Recurso | Endereço |
|---|---|
| Swagger UI (documentação interativa) | http://127.0.0.1:8000/docs |
| ReDoc | http://127.0.0.1:8000/redoc |

O comando precisa ser executado dentro de `Produtos_Api`, porque os módulos são importados a partir dessa pasta.

## Endpoints

| Método | Rota | Finalidade | Protegida | Respostas |
|---|---|---|---|---|
| POST | `/usuarios` | Cadastrar usuário | Não | 201 / 409 / 422 |
| POST | `/login` | Autenticar e receber o token | Não | 200 / 401 |
| GET | `/produtos` | Listar produtos | Não | 200 |
| GET | `/produtos/{id}` | Consultar um produto | Não | 200 / 404 |
| POST | `/produtos` | Criar produto | **Sim** | 201 / 401 / 422 |
| PATCH | `/produtos/{id}` | Atualizar campos de um produto | Não | 200 / 400 / 404 / 422 |
| DELETE | `/produtos/{id}` | Excluir produto | Não | 204 / 404 |

As respostas de erro seguem o formato JSON `{"detail": "mensagem"}`. Nos erros de validação (422), `detail` traz a lista dos campos inválidos e o motivo.

## Modelo de dados e validações

### Tabela `produtos`

| Campo | Tipo no banco | Regra de validação |
|---|---|---|
| `id` | INT, chave primária, auto incremento | gerado pelo banco |
| `nome` | VARCHAR(100) | obrigatório, de 1 a 100 caracteres |
| `descricao` | VARCHAR(255) | obrigatório, até 255 caracteres |
| `preco` | FLOAT | obrigatório, maior que 0 |
| `estoque` | INT | obrigatório, maior ou igual a 0 |

### Tabela `usuarios`

| Campo | Tipo no banco | Regra de validação |
|---|---|---|
| `id` | INT, chave primária, auto incremento | gerado pelo banco |
| `username` | VARCHAR(50), único | de 3 a 50 caracteres |
| `senha_hash` | VARCHAR(255) | a senha enviada deve ter ao menos 6 caracteres; só o hash é gravado |

### Atualização parcial (PATCH)

Todos os campos são opcionais, e as mesmas regras valem para os que forem enviados. Um corpo vazio (`{}`) retorna 400.

## Autenticação

A autenticação usa **JWT** (algoritmo HS256), com validade de **30 minutos**.

**Fluxo**

1. O usuário se cadastra em `POST /usuarios`. A senha é gravada como hash Argon2, nunca em texto puro.
2. Em `POST /login`, envia `username` e `password` (formulário). A API confere a senha e devolve o `access_token`.
3. Nas rotas protegidas, o cliente envia o cabeçalho `Authorization: Bearer <token>`.
4. A API valida a assinatura, a expiração e a existência do usuário. Se algo falhar, responde **401**.

**Como testar sem expor credenciais**

Não existe usuário padrão. Crie um usuário de teste com qualquer nome e senha, por exemplo `usuario_teste` e `senha123456` (a senha precisa de pelo menos 6 caracteres).

No Swagger (`/docs`):

1. Execute `POST /usuarios` com o usuário de teste.
2. Clique em **Authorize** (cadeado no topo), informe `username` e `password` e confirme. Os campos `client_id` e `client_secret` ficam vazios.
3. Execute `POST /produtos`. Com o login feito, o resultado é 201. Sem login (ou depois de *Logout*), o resultado é 401.

## CORS

A política de CORS está configurada no `main.py`:

| Item | Valor |
|---|---|
| Origens permitidas | `http://localhost:8000` |
| Métodos permitidos | GET, POST, PATCH, DELETE |
| Cabeçalhos permitidos | Authorization, Content-Type |

O CORS é um mecanismo do navegador: uma página servida por outra origem só consegue chamar a API se a origem dela estiver autorizada. Foi adotada uma lista restrita de origens, sem liberar qualquer origem (`*`), com apenas os métodos e cabeçalhos necessários ao CRUD e à autenticação por token. Para usar um front-end em outro endereço, adicione a origem dele em `allow_origins`, no `main.py`.

Requisições feitas pelo Swagger partem da mesma origem da API e, por isso, não dependem do CORS.

## Exemplos de requisição

Os exemplos usam `curl` (Linux, macOS ou Git Bash). No Windows, o jeito mais simples de testar é pelo Swagger.

**Cadastrar usuário**

```bash
curl -X POST http://127.0.0.1:8000/usuarios \
  -H "Content-Type: application/json" \
  -d '{"username": "usuario_teste", "senha": "senha123"}'
```

**Login (retorna o token)**

```bash
curl -X POST http://127.0.0.1:8000/login \
  -d "username=usuario_teste&password=senha123"
```

Resposta:

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer"
}
```

**Criar produto (protegido)**

```bash
curl -X POST http://127.0.0.1:8000/produtos \
  -H "Authorization: Bearer SEU_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"nome": "Mouse sem fio", "descricao": "Mouse óptico 2.4 GHz", "preco": 79.90, "estoque": 25}'
```

Resposta (201):

```json
{
  "id": 1,
  "nome": "Mouse sem fio",
  "descricao": "Mouse óptico 2.4 GHz",
  "preco": 79.9,
  "estoque": 25
}
```

**Listar e consultar**

```bash
curl http://127.0.0.1:8000/produtos
curl http://127.0.0.1:8000/produtos/1
```

**Atualizar apenas o preço**

```bash
curl -X PATCH http://127.0.0.1:8000/produtos/1 \
  -H "Content-Type: application/json" \
  -d '{"preco": 59.90}'
```

**Excluir**

```bash
curl -X DELETE http://127.0.0.1:8000/produtos/1
```

Resposta: 204, sem corpo.

## Roteiro de testes

Os testes podem ser feitos pelo Swagger (`/docs`), seguindo esta ordem:

| # | Requisição | Resultado esperado |
|---|---|---|
| 1 | `POST /produtos` sem login | 401 |
| 2 | `POST /usuarios` com senha de 3 caracteres | 422 |
| 3 | `POST /usuarios` com dados válidos | 201 |
| 4 | `POST /usuarios` repetindo o mesmo usuário | 409 |
| 5 | `POST /login` com senha errada | 401 |
| 6 | `POST /login` com a senha correta | 200 com `access_token` |
| 7 | `POST /produtos` após o Authorize | 201 |
| 8 | `POST /produtos` com `preco` negativo | 422 |
| 9 | `GET /produtos` | 200 |
| 10 | `GET /produtos/{id}` com id existente | 200 |
| 11 | `GET /produtos/9999` | 404 |
| 12 | `PATCH /produtos/{id}` com `{"preco": 59.90}` | 200 |
| 13 | `PATCH /produtos/{id}` com `{}` | 400 |
| 14 | `PATCH /produtos/9999` | 404 |
| 15 | `DELETE /produtos/{id}` com id existente | 204 |
| 16 | `DELETE` repetido, com o mesmo id | 404 |

Para conferir a persistência, consulte o banco no MySQL Workbench:

```sql
USE api_produtos;
SELECT * FROM produtos;
SELECT id, username, senha_hash FROM usuarios;
```

A coluna `senha_hash` mostra um texto ilegível, o que confirma que a senha não é gravada em texto puro.

## Decisões de projeto

- **FastAPI:** valida os dados de entrada com Pydantic e gera a documentação OpenAPI (Swagger) automaticamente, o que facilita os testes e as evidências.
- **SQLAlchemy (ORM):** cada classe de `models.py` representa uma tabela (`Produto` é a tabela `produtos`, `Usuario` é a tabela `usuarios`), e cada atributo mapeado representa uma coluna. As consultas são feitas com objetos Python, sem SQL escrito à mão nas rotas.
- **MySQL:** banco relacional com persistência real, mantendo os dados entre execuções.
- **PATCH em vez de PUT:** a atualização é parcial, e o cliente envia só os campos que quer alterar. Isso combina com um catálogo, em que preço e estoque mudam com frequência.
- **Código 422 para dados inválidos:** é o código padrão do FastAPI quando o JSON está bem formado, mas o conteúdo é inválido. O 400 é usado quando o PATCH chega sem nenhum campo.
- **JWT e Argon2:** o token dispensa guardar sessão no servidor, e as senhas são armazenadas apenas como hash.
- **Segredos em variáveis de ambiente:** a senha do banco e a chave do JWT ficam no `.env`, fora do repositório. O `.env.example` mostra a estrutura esperada.

## Limitações conhecidas

- Somente o `POST /produtos` exige login. `PATCH` e `DELETE` estão abertos, e podem ser protegidos com a mesma dependência de autenticação (`usuario_logado`).
- O cadastro de usuários (`POST /usuarios`) é aberto: qualquer pessoa pode criar uma conta.
- A listagem não tem filtros nem paginação.
- O preço usa `FLOAT`. Para valores monetários em produção, o tipo `DECIMAL` é mais adequado.
- Não há refresh token: depois de 30 minutos é preciso fazer login de novo.

## Solução de problemas

| Mensagem ou sintoma | Causa provável |
|---|---|
| `Defina a DATABASE_URL no arquivo .env` | O `.env` não existe em `Produtos_Api`, está com outro nome (como `.env.txt`) ou a variável está escrita errada. |
| `ModuleNotFoundError: No module named 'auth'` | O `uvicorn` foi executado fora da pasta `Produtos_Api`. |
| `Access denied for user` ou `Can't connect to MySQL server` | Usuário ou senha incorretos na `DATABASE_URL`, ou o MySQL não está em execução. |
| Senha com caractere especial não conecta | Codifique o caractere na URL (`@` vira `%40`). |
| `401` no `POST /produtos` logo após o login | O token expirou (validade de 30 minutos). Faça o Authorize de novo. |



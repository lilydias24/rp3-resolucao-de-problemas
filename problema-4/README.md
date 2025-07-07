# Sistema de Gerenciamento de Histórias de Usuário com LLMs

Este projeto é uma API desenvolvida em FastAPI para cadastro de produtos, autenticação de usuários e (futuramente) gerenciamento de requisitos ágeis, com integração a LLMs.

## Funcionalidades

- Cadastro e autenticação de usuários
- Cadastro de produtos
- (Em breve) Gestão de épicos, histórias, backlog, etc.
- Testes automatizados com cobertura e relatórios visuais
- **Aspectos (AOP):** logging, tratamento de erros e autorização por papel

---

## Pré-requisitos

- Python 3.12+
- [Poetry](https://python-poetry.org/) para gerenciamento de dependências

---

## Instalação

1. Clone o repositório:
   ```sh
   git clone <url-do-repo>
   cd grupo-05/problema-4
   ```

2. Instale as dependências:
   ```sh
   poetry install
   ```

---

## Como rodar a aplicação

1. Ative o ambiente virtual do Poetry:
   ```sh
   poetry shell
   ```

2. Execute a API:
   ```sh
   uvicorn main:app --reload
   ```

3. Acesse a documentação interativa:
   - [http://localhost:8000/docs](http://localhost:8000/docs)
   - [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## Como rodar os testes

O projeto já vem com testes automatizados usando pytest, incluindo testes de aspectos (AOP).

### Rodando os testes no terminal

```sh
poetry run pytest -v
```

### Rodando os testes com relatório HTML e cobertura de código

Gere um relatório visual dos testes e da cobertura de código:

```sh
poetry run pytest --cov=src --cov-report=html --html=report.html
```

- O resultado dos testes estará em `report.html` (abra no navegador).
- O relatório de cobertura estará em `htmlcov/index.html` (abra no navegador).

### Rodando os testes com relatório CSV

Gere um relatório CSV dos testes:

```sh
poetry run pytest --csv=tests/report.csv
```

- O resultado dos testes estará em `tests/report.csv` (abra no Excel, Google Sheets, etc.).

---

## Utilização de Aspectos (AOP)

Este projeto utiliza **Aspect-Oriented Programming (AOP)** para separar preocupações transversais, como logging, tratamento de erros e autorização, do código de negócio principal.

### Aspectos implementados

- **Logging (`log_operations`)**: Registra automaticamente operações importantes, facilitando auditoria e debug.
- **Tratamento de erros (`handle_errors`)**: Garante que exceções sejam capturadas e respostas amigáveis sejam retornadas ao usuário.
- **Autorização (`require_role`)**: Restringe o acesso a endpoints por papel do usuário (ex: só admin pode criar produto).

### Como os aspectos são aplicados

Os aspectos são aplicados aos endpoints principais usando o pacote `aspectlib` e o método `weave`. Por exemplo:

```python
from aspectlib import weave
from src.aspects.logging import log_operations
from src.aspects.error_handling import handle_errors
from src.aspects.authorization import require_role

weave(create_product, log_operations)
weave(create_product, handle_errors)
weave(create_product, require_role('admin'))  # Só admin pode criar produto
weave(register, log_operations)
weave(register, handle_errors)
weave(login, log_operations)
weave(login, handle_errors)
```

Assim, garantimos que todos os endpoints críticos estejam protegidos por logging, tratamento de erros e autorização, sem poluir o código de negócio.

### Benefícios

- **Manutenção facilitada**: Alterações em logging, tratamento de erros ou regras de autorização são feitas em um só lugar.
- **Código mais limpo**: O código de negócio fica livre de repetições e preocupações transversais.
- **Auditoria e rastreabilidade**: Todas as operações importantes são registradas automaticamente.
- **Segurança**: Restrições de acesso centralizadas e testadas.

---

## Testes de Aspectos

O projeto inclui testes automatizados para garantir o funcionamento dos aspectos:

- **Logging:** Garante que operações importantes são registradas.
- **Tratamento de erros:** Garante que exceções são capturadas e retornam respostas amigáveis.
- **Autorização:** Garante que apenas usuários com o papel correto podem acessar determinados endpoints.

Exemplo de teste de autorização:
```python
from src.routers.product import create_product
from src.db.models import User
from src.schemas.product import ProductCreate
import pytest
from fastapi import HTTPException

def test_authorization_allows_admin():
    user = User(user_id=1, email="admin@example.com", name="Admin", password_hash="hash", is_active=True)
    user.role = 'admin'
    product_data = ProductCreate(name="Produto Teste", description="desc", valueProposition="prop", platforms=["web"])
    create_product(product_data, db=..., current_user=user)  # Não deve levantar exceção

def test_authorization_denies_non_admin():
    user = User(user_id=2, email="user@example.com", name="User", password_hash="hash", is_active=True)
    user.role = 'user'
    product_data = ProductCreate(name="Produto Teste", description="desc", valueProposition="prop", platforms=["web"])
    with pytest.raises(HTTPException) as excinfo:
        create_product(product_data, db=..., current_user=user)
    assert excinfo.value.status_code == 403
```

---

## Estrutura do projeto

```
problema-4/
├── main.py
├── src/
│   └── ... (código da aplicação)
├── aspects/
│   ├── logging.py
│   ├── error_handling.py
│   └── authorization.py
├── tests/
│   └── ... (testes automatizados, inclusive de aspectos)
├── report.html
├── htmlcov/
│   └── index.html
├── pyproject.toml
└── README.md
```

---

## Licença

[MIT](LICENSE) (ou outra, se aplicável)

---

## Contato

Dúvidas ou sugestões? Abra uma issue ou entre em contato com os mantenedores do projeto.

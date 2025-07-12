# Sistema de Gerenciamento de Histórias de Usuário com LLMs

Este projeto é uma API desenvolvida em FastAPI para cadastro de produtos, autenticação de usuários e (futuramente) gerenciamento de requisitos ágeis, com integração a LLMs.

## Funcionalidades

- Cadastro e autenticação de usuários
- Cadastro de produtos
- Geração de épicos, histórias e requisitos via LLM
- Testes automatizados com cobertura e relatórios visuais
- **Aspectos (AOP):** logging, tratamento de erros, autorização por papel e notificação

---

## Histórias de Usuários 

---
**Descrição**

Você deve desenvolver um sistema que ajude Product Owners (POs) na criação, refinamento e exportação histórias de usuário e requisitos a partir de Large Language Models (LLMs).

**Histórias de Usuário**

✅1. Como Product Owner, quero cadastrar um novo produto com algumas informações básicas para iniciar o processo de geração de histórias de usuário e requisitos. Exemplos de informações: <br>
    -> Nome. <br>
    -> Descrição. <br>
    -> Personas envolvidas. <br>
    -> Proposta de valor (problema que o produto resolve). <br>
    -> Canais/Plataformas (web, mobile, etc.). <br>

✅2. Como Product Owner, quero que o sistema gere automaticamente uma hierarquia de Épicos para o projeto.
🔚3. Como Product Owner, quero poder revisar e sugerir melhorias para os épicos gerados, garantindo que esteja alinhada com as necessidades do produto.
✅4. Como Product Owner, quero que o sistema gere, através de Large Language Models (LLMs), um conjunto de histórias de usuário para o produto cadastrado, permitindo uma base inicial de trabalho. O sistema deve: <br>
    -> Utilizar um prompt pré-definido para guiar a geração, mas permitir que o PO ajuste o prompt conforme necessário. <br>
    -> Garantir que as histórias geradas sejam relevantes para o produto e suas personas. <br>

🔚5. Como Product Owner, quero poder revisar e sugerir melhorias para as histórias de usuário para ajustar detalhes de negócio.
🔚6. Como Product Owner, quero gerar requisitos funcionais correspondentes às histórias aprovadas com suas respectivas prioridades, para garantir que o desenvolvimento esteja alinhado com as necessidades do produto.
❌7. Como Product Owner, quero rastrear o histórico de revisões de cada épico/história/requisito para manter a rastreabilidade de decisões.
⚠️8. Como Product Owner, quero gerar um backlog de produto a partir das histórias e requisitos aprovados, para organizar o trabalho da equipe de desenvolvimento.
⚠️9. Como Product Owner, quero poder revisar e sugerir melhorias para os backlogs gerados, garantindo que estejam alinhados com as necessidades do produto.


**Regras de Negócio**

1. Todas as interações com LLMs devem ser registradas por mecanismo de logging detalhado, incluindo data, hora, usuário, prompt utilizado e resumo da resposta gerada.
2. Todas as ações devem ser autenticadas.
3. Cada grupo deve propor no mínimo mais um aspecto transversal para o projeto. <br>
**Obs :** A lista acima não é exaustiva e pode ser expandida conforme necessário.


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

Este projeto utiliza **Aspect-Oriented Programming (AOP)** para separar preocupações transversais, como logging, tratamento de erros, autorização e notificação do código de negócio principal.

### Aspectos implementados

- **Logging (`logging_aspect`)**: Registra automaticamente operações importantes, facilitando auditoria e debug.
- **Tratamento de erros (`handle_errors`)**: Garante que exceções sejam capturadas e respostas amigáveis sejam retornadas ao usuário.
- **Autorização (`require_role`)**: Restringe o acesso a endpoints por papel do usuário (ex: só admin pode criar produto).
- **Notificação (`notification_aspect`)**: Permite notificar eventos importantes do sistema (ex: criação de produto, login, geração de conteúdo).

### Como os aspectos são aplicados

Os aspectos são aplicados diretamente como **decoradores** nas funções de negócio e endpoints principais. Exemplo:

```python
from aspects.logging import logging_aspect
from aspects.error_handling import handle_errors
from aspects.authorization import require_role
from aspects.notification import notification_aspect

@router.post("/products")
@require_role('admin')
@handle_errors
@logging_aspect
@notification_aspect
def create_product(...):
    ...
```

- **A ordem dos decoradores importa:**
  - O de erro deve ser o mais externo.
  - Depois logging, autorização, notificação, etc.

### Pontos críticos cobertos
- **Produto:** criação de produto (negócio e endpoint)
- **Autenticação:** registro, login, recuperação de usuário
- **LLM:** geração de épicos, histórias e requisitos
- **Banco de dados:** logging de sessão
- **Notificação:** eventos de criação, login, geração de conteúdo

### Benefícios

- **Manutenção facilitada**: Alterações em logging, tratamento de erros, regras de autorização ou notificação são feitas em um só lugar.
- **Código mais limpo**: O código de negócio fica livre de repetições e preocupações transversais.
- **Auditoria e rastreabilidade**: Todas as operações importantes são registradas automaticamente.
- **Segurança**: Restrições de acesso centralizadas e testadas.
- **Notificações**: Eventos importantes podem ser facilmente notificados/logados.

---

## Testes de Aspectos

O projeto inclui testes automatizados para garantir o funcionamento dos aspectos:

- **Logging:** Garante que operações importantes são registradas.
- **Tratamento de erros:** Garante que exceções são capturadas e retornam respostas amigáveis.
- **Autorização:** Garante que apenas usuários com o papel correto podem acessar determinados endpoints.
- **Notificação:** Garante que eventos importantes são notificados.

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
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── product.py
│   │   ├── auth.py
│   │   ├── llm.py
│   │   └── dashboard.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── product.py
│   │   ├── user.py
│   │   └── llm.py
│   ├── db/
│   │   ├── __init__.py
│   │   ├── session.py
│   │   ├── models.py
│   │   └── base.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── LLM.py
│   │   ├── epics.py
│   │   └── LLM_interactive.py
│   └── config/
│       └── ...
├── aspects/
│   ├── __init__.py
│   ├── logging.py
│   ├── error_handling.py
│   ├── authorization.py
│   ├── notification.py
│   ├── db_session.py
│   └── (LLM.py, llm_aspects.py)  # Se forem aspectos, senão mova para utils
├── tests/
│   └── ...
├── README.md
└── ...
```

---

## Licença

[MIT](LICENSE) (ou outra, se aplicável)

---

## Contato

Dúvidas ou sugestões? Abra uma issue ou entre em contato com os mantenedores do projeto.

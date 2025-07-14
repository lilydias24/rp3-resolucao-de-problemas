# Sistema de Gerenciamento de Histórias de Usuário com LLMs

Este projeto é uma API desenvolvida em FastAPI para cadastro de produtos, autenticação de usuários e gerenciamento de requisitos ágeis, com integração a LLMs e uma interface CLI completa.

## Funcionalidades

- Cadastro e autenticação de usuários
- Cadastro de produtos
- Geração de épicos, histórias e requisitos via LLM
- **Sistema de Revisão/Sugestão** com workflow completo de aprovação
- **Sistema de Rastreamento de Revisões** para auditoria completa
- **Geração Automática de Backlog** com múltiplas estratégias
- **Interface CLI** completa com cores e formatação visual
- **CRUD completo** para todas as entidades (produtos, épicos, histórias, requisitos, backlogs, itens)
- Testes automatizados com cobertura e relatórios visuais
- **Aspectos (AOP):** logging, tratamento de erros, autorização por papel e notificação

---

## Interface CLI

O projeto inclui uma interface de linha de comando (CLI) completa desenvolvida com Typer e formatação colorida.

### Como usar o CLI

1. **Executar o CLI:**
   ```bash
   python main.py cli
   # ou
   python cli.py menu
   ```

2. **Comandos diretos:**
   ```bash
   python cli.py register  # Registrar usuário
   python cli.py login     # Fazer login
   python cli.py menu      # Menu principal
   ```

### Funcionalidades do CLI

- **Autenticação:** Registro e login de usuários
- **Produtos:** CRUD completo com formatação visual
- **Épicos:** CRUD completo + gerenciamento de revisões
- **Histórias de Usuário:** CRUD completo + histórico de revisões
- **Requisitos:** CRUD completo + histórico de revisões
- **Backlogs:** CRUD completo + geração automática
- **Itens de Backlog:** CRUD completo
- **Geração via LLM:** Épicos, histórias e requisitos

### Sistema de Cores

O CLI utiliza um sistema de cores completo para melhor experiência do usuário:

- **Cabeçalhos:** Ciano brilhante
- **Sucesso:** Verde com ícone ✓
- **Erro:** Vermelho com ícone ✗
- **Aviso:** Amarelo com ícone ⚠
- **Informação:** Azul com ícone ℹ
- **Menus:** Magenta para títulos, branco para opções
- **Dados:** Formatação específica para IDs, nomes, status, etc.

### Exemplo de uso do CLI

```bash
# 1. Registrar e fazer login
python cli.py register
python cli.py login

# 2. Acessar menu principal
python cli.py menu

# 3. Navegar pelos menus
# Produtos -> Cadastrar produto
# Épicos -> Criar épico
# Geração via LLM -> Gerar épicos
# Backlogs -> Gerar backlog automaticamente
```

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
✅3. Como Product Owner, quero poder revisar e sugerir melhorias para os épicos gerados, garantindo que esteja alinhada com as necessidades do produto.
✅4. Como Product Owner, quero que o sistema gere, através de Large Language Models (LLMs), um conjunto de histórias de usuário para o produto cadastrado, permitindo uma base inicial de trabalho. O sistema deve: <br>
    -> Utilizar um prompt pré-definido para guiar a geração, mas permitir que o PO ajuste o prompt conforme necessário. <br>
    -> Garantir que as histórias geradas sejam relevantes para o produto e suas personas. <br>

✅5. Como Product Owner, quero poder revisar e sugerir melhorias para as histórias de usuário para ajustar detalhes de negócio.
✅6. Como Product Owner, quero gerar requisitos funcionais correspondentes às histórias aprovadas com suas respectivas prioridades, para garantir que o desenvolvimento esteja alinhado com as necessidades do produto.
✅7. Como Product Owner, quero rastrear o histórico de revisões de cada épico/história/requisito para manter a rastreabilidade de decisões.
✅8. Como Product Owner, quero gerar um backlog de produto a partir das histórias e requisitos aprovados, para organizar o trabalho da equipe de desenvolvimento.
✅9. Como Product Owner, quero poder revisar e sugerir melhorias para os backlogs gerados, garantindo que estejam alinhados com as necessidades do produto.


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

### Opção 1: API FastAPI

1. Ative o ambiente virtual do Poetry:
   ```sh
   poetry shell
   ```

2. Execute a API:
   ```sh
   uvicorn main:app --reload
   # ou
   python main.py
   ```

3. Acesse a documentação interativa:
   - [http://localhost:8000/docs](http://localhost:8000/docs)
   - [http://localhost:8000/redoc](http://localhost:8000/redoc)

### Opção 2: Interface CLI

1. Execute o CLI:
   ```sh
   python main.py cli
   # ou
   python cli.py menu
   ```

2. Siga as instruções na tela para navegar pelos menus.

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
- **Rastreamento de Revisões (`revision_tracking`)**: Registra automaticamente mudanças em entidades para auditoria.

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
- **Revisões:** rastreamento de mudanças em épicos, histórias e requisitos

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
- **Rastreamento de Revisões:** Garante que mudanças são registradas corretamente.

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

## Sistema de Revisão/Sugestão

O sistema de revisão/sugestão permite um workflow completo de aprovação e refinamento de épicos, histórias de usuário e requisitos.

### Funcionalidades

- **Status de Revisão**: draft, in_review, approved, rejected, needs_revision, implemented
- **Comentários e Sugestões**: Sistema completo de feedback com rastreamento
- **Ações de Revisão**: submit_for_review, approve, reject, request_revision, mark_implemented
- **Histórico de Status**: Rastreamento completo de mudanças de status

### Endpoints Principais

- `POST /review/comments` - Criar comentário de revisão
- `POST /review/{entity_type}/{entity_id}/action` - Executar ação de revisão
- `GET /review/{entity_type}/{entity_id}/info` - Informações de revisão
- `GET /review/{entity_type}/{entity_id}/summary` - Resumo completo

### Uso via CLI

```bash
python cli.py menu
# Navegar para Épicos -> Gerenciar Revisões
```

---

## Sistema de Rastreamento de Revisões

O sistema de rastreamento registra automaticamente todas as mudanças feitas em épicos, histórias de usuário e requisitos.

### Funcionalidades

- **Rastreamento Automático**: Mudanças capturadas via aspecto AOP
- **Histórico Completo**: Quem fez o quê, quando e por quê
- **Comparação de Estados**: Antes e depois de cada mudança
- **Auditoria Total**: Rastreabilidade completa das decisões

### Endpoints de Histórico

- `GET /products/epics/{epic_id}/revisions` - Histórico de revisões do épico
- `GET /products/stories/{story_id}/revisions` - Histórico de revisões da história
- `GET /products/requirements/{requirement_id}/revisions` - Histórico de revisões do requisito

### Uso via CLI

```bash
python cli.py menu
# Épicos -> Opção 6 -> Informe ID do épico
# Histórias -> Opção 6 -> Informe ID da história
# Requisitos -> Opção 6 -> Informe ID do requisito
```

---

## Geração Automática de Backlog

O sistema de geração automática de backlog cria backlogs de forma inteligente a partir de histórias e requisitos aprovados.

### Estratégias de Geração

- **Priority Based**: Baseado em prioridade com fatores adicionais
- **Epic Based**: Agrupado por épicos
- **Story Only**: Apenas histórias de usuário
- **Requirement Only**: Apenas requisitos
- **Mixed**: Histórias e requisitos misturados

### Funcionalidades

- **Filtros Avançados**: Prioridade mínima, número máximo de itens
- **Opções de Configuração**: Peso para tipos, multiplicador de prioridade
- **Preview de Geração**: Visualizar antes de confirmar
- **Métricas Automáticas**: Estimativa de esforço e valor de negócio

### Endpoints Principais

- `POST /backlog-generation/preview` - Preview da geração
- `POST /backlog-generation/generate` - Gerar backlog
- `POST /backlog-generation/generate/quick` - Geração rápida
- `GET /backlog-generation/strategies` - Estratégias disponíveis

### Uso via CLI

```bash
python cli.py menu
# Navegar para Backlogs
# Opção 6: Gerar backlog automaticamente
# Opção 7: Preview de geração de backlog
# Opção 8: Ver itens aprovados
```

---

## Estrutura do projeto

```
problema-4/
├── main.py                 # Ponto de entrada da API
├── cli.py                  # Interface CLI completa
├── src/
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── product.py
│   │   ├── auth.py
│   │   ├── llm.py
│   │   ├── dashboard.py
│   │   ├── review.py       # Sistema de revisão
│   │   └── backlog_generation.py  # Geração de backlog
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── product.py
│   │   ├── user.py
│   │   ├── llm.py
│   │   ├── review.py       # Schemas de revisão
│   │   └── backlog_generation.py  # Schemas de backlog
│   ├── db/
│   │   ├── __init__.py
│   │   ├── session.py
│   │   ├── models.py
│   │   └── base.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── LLM.py
│   │   ├── epics.py
│   │   ├── colors.py       # Sistema de cores para CLI
│   │   ├── backlog_generator.py  # Gerador de backlog
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
│   └── revision_tracking.py  # Rastreamento de revisões
├── tests/
│   ├── test_aspects_*.py   # Testes de aspectos
│   ├── test_review_system.py  # Testes do sistema de revisão
│   ├── test_backlog_generation.py  # Testes de geração de backlog
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

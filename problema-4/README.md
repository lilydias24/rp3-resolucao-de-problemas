# Sistema de Gerenciamento de Histórias de Usuário com LLMs

Este projeto é uma API desenvolvida em FastAPI para cadastro de produtos, autenticação de usuários e (futuramente) gerenciamento de requisitos ágeis, com integração a LLMs.

## Funcionalidades

- Cadastro e autenticação de usuários
- Cadastro de produtos
- (Em breve) Gestão de épicos, histórias, backlog, etc.
- Testes automatizados com cobertura e relatórios visuais

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

O projeto já vem com testes automatizados usando pytest.

### Rodando os testes no terminal

```sh
poetry run pytest
```

### Rodando os testes com relatório HTML e cobertura de código

Gere um relatório visual dos testes e da cobertura de código:

```sh
poetry run pytest --cov=src --cov-report=html --html=report.html
```

- O resultado dos testes estará em `report.html` (abra no navegador).
- O relatório de cobertura estará em `htmlcov/index.html` (abra no navegador).

---

## Dicas para desenvolvimento

- Use o comando acima sempre que fizer mudanças importantes para garantir a qualidade do código.
- Os relatórios HTML facilitam a visualização de falhas e pontos não cobertos pelos testes.
- Para uma experiência ainda melhor, utilize plugins como `pytest-sugar` ou integre com sua IDE.

---

## Estrutura do projeto

```
problema-4/
├── main.py
├── src/
│   └── ... (código da aplicação)
├── tests/
│   └── ... (testes automatizados)
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

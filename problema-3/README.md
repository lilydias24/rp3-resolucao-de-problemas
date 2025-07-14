-> Objetivo
Recomendar carreiras para estudantes com base em:

- Interesses
- Habilidades
- Desempenho escolar
- Tendências de mercado

Usando:

- Regras lógicas (como em Prolog, mas feitas em Python)
- Banco de dados SQLite
- Arquitetura orientada a objetos
- Justificativas explicáveis por regra + fato

-> Estrutura atual do sistema : 

`/problema-3/`  
`├── main.py`                     # Menu principal e execução 
`├── __init__.py`                             
`├── pyproject.toml`             # Configuração do projeto e dependências
`├── utils/`  
`│   ├── __init__.py`            
`│   ├── cores.py`               # Definição de cores para interface
`│   ├── exportador_csv.py`      # Exportação de relatórios em CSV
`│   ├── gestor.py`              # Gerenciamento de regras
`│   ├── gestor_interface.py`    # Interface do gestor acadêmico
`│   ├── importar_regras.py`     # Importação de regras do JSON
`│   ├── interface.py`           # Interface do sistema
`│   ├── popular_banco.py`       # População inicial do banco
`│   └── regras.json`            # Arquivo de configuração das regras
`├── data/`  
`│   ├── __init__.py`            
`│   ├── banco.db`               # Banco de dados SQLite
`│   ├── conexao.py`             # Conexão com o banco
`│   ├── criar_banco.py`         # Criação das tabelas
`│   ├── relatorio_db.py`        # Geração de relatórios
`│   ├── transacao.py`           # Gerenciamento de transações
`│   └── validacao.py`           # Validação de dados
`├── logic/`  
`│   ├── __init__.py`
`│   ├── controlador.py`         # Controlador principal
`│   ├── estudante.py`           # Lógica de estudantes
`│   ├── motor.py`               # Motor de inferência
`│   └── recomendacao.py`        # Lógica de recomendações
`├── reports/`  
`│   ├── __init__.py`            
`│   ├── gerar_relatorios.py`    # Geração de relatórios
`│   ├── graficos.py`            # Geração de gráficos
`│   ├── graficos/`              # Diretório de gráficos gerados
`│   └── relatorios/`            # Diretório de relatórios gerados
`└── tests/`  
`    ├── __init__.py`
`    ├── test_estudante.py`       # Testes da lógica de estudantes
`    ├── test_exemplo.py`         # Testes de exemplo
`    ├── test_motor.py`           # Testes do motor de inferência
`    └── test_validacao.py`       # Testes de validação de dados

-> Ferramentas úteis : 

black -> formata e identa o código com base em boas práticas em Python
poetry -> gestão de dependências

Comandos úteis:
```bash
# Instalação de ferramentas
pip install black
pip install poetry

# Formatação de código
black nomeDoArquivo
black nomeDaPasta

# Gerenciamento de dependências
poetry add nomeDaDependencia
poetry install
poetry new <nome_do_projeto>

# Execução de testes
python -m pytest tests/
```

-> Organização de tarefas : 

*Emilly* -> 1. _Como Estudante, quero informar meus interesses (ex.: artes, ciências, tecnologia) para que o sistema considere minhas afinidades._

*Matheus* -> 2. _Como Estudante, quero informar minhas habilidades (ex.: programação, redação, resolução de problemas) para receber recomendações alinhadas às minhas competências._

*Matheus* -> 3. _Como Estudante, quero informar meu desempenho em disciplinas escolares para que o sistema ajuste suas sugestões._

*Eric* -> 4. _Como Estudante, quero obter uma lista de carreiras recomendadas com justificativas baseadas em regras lógicas._

*Doug* -> 5. _Como Gestor Acadêmico, quero acrescentar novas regras referentes a carreiras emergentes sem alterar o código-fonte principal._

*Doug* -> 6. _Como Gestor Acadêmico, quero personalizar o peso das regras de acordo com a relevância de cada critério (ex.: interesses, habilidades)._ 

*Eric* -> 7. _Como Gestor Acadêmico, quero gerar relatórios agregados em formato CSV sobre tendências de carreira escolhidas pelos estudantes._

*Emilly* -> 8. _Como Gestor Acadêmico, quero visualizar gráficos de desempenho por disciplina e por estudante sobre as recomendações_
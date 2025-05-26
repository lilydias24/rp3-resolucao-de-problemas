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

-> Estrutura sugerida do sistema : 

`/sistema_carreiras/`  
`├── main.py`                     # Menu principal e execução 
`├── utils/`  
`├── data/`  
`│   └── logica.py`             # Definição das regras lógicas do sistema  
`│   └── conexao.py`              # Criação e acesso ao banco  
`├── models/`  
`│   ├── estudante.py`            # Classe Estudante  
`│   └── carreira.py`             # Classe Carreira  
`├── logic/`  
`│   ├── __init__.py
`│   ├── motor.py`                # Motor de inferência  
`│   ├── regra.py`                # Representação de regra lógica
`│   └── logica.py`                # Implementação das regras lógicas  
`├── reports/`  
`│   ├── exportador_csv.py`       # Gera CSVs  
`│   └── graficos.py`             # Gera gráficos  
`└── tests/`  
`    └── test_exemplo.py`           # Exemplo de uso do sistema  


-> Uteis para o grupo : 

black -> formata e identa o codigo com base em boas praticas em python
poetry -> gestão de dependencias
pip install black -> instala o formatador
black nomeDoArquivo -> formata o código do arquivo
black nomeDaPasta -> formata os códigos da pasta
pip install poetry -> instala o poetry
poetry add nomeDaDependencia -> adiciona a dependencia 
poetry install -> instala as dependencias
poetry new <nome_do_projeto> -> cria uma nova estrutura de projeto com o poetry.

-> Organização de tarefas : 

*Emilly* -> 1. _Como Estudante, quero informar meus interesses (ex.: artes, ciências, tecnologia) para que o sistema considere minhas afinidades._

*Matheus* -> 2. _Como Estudante, quero informar minhas habilidades (ex.: programação, redação, resolução de problemas) para receber recomendações alinhadas às minhas competências._

*Matheus* -> 3. _Como Estudante, quero informar meu desempenho em disciplinas escolares para que o sistema ajuste suas sugestões._

*Eric* -> 4. _Como Estudante, quero obter uma lista de carreiras recomendadas com justificativas baseadas em regras lógicas._

*Doug* -> 5. _Como Gestor Acadêmico, quero acrescentar novas regras referentes a carreiras emergentes sem alterar o código-fonte principal._

*Doug* -> 6. _Como Gestor Acadêmico, quero personalizar o peso das regras de acordo com a relevância de cada critério (ex.: interesses, habilidades)._ 

*Eric* -> 7. _Como Gestor Acadêmico, quero gerar relatórios agregados em formato CSV sobre tendências de carreira escolhidas pelos estudantes._

*Emilly* -> 8. _Como Gestor Acadêmico, quero visualizar gráficos de desempenho por disciplina e por estudante sobre as recomendações_
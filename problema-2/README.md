# Sistema de Dados Médicos - Problema II (2025/1)

Este projeto implementa um sistema voltado para a prática de **resolução de problemas utilizando programação funcional** em Python.  
O sistema permite o gerenciamento de contas de usuários e a análise de dados médicos de forma simples e intuitiva.

Desenvolvido como parte da disciplina **Resolução de Problemas III** - **Grupo 05**.

## Funcionalidades Principais

- **Cadastro de Usuários**: Criação de novas contas de usuários.
- **Login de Usuários**: Acesso ao sistema com diferenciação entre paciente e profissional de saúde.
- **Análise de Dados Médicos**:
  - Carregamento de arquivos CSV com registros de saúde.
  - Cálculo de métricas estatísticas: média, mediana, moda, desvio padrão e variância.
- **Painel Administrativo**:
  - Criar contas manualmente.
  - Editar dados de usuários.
  - Excluir contas.
  - Buscar contas por ID.


## Estrutura do Projeto

Ao longo do desenvolvimento do trabalho, pretende-se adotar a seguinte organização:

problema-2/
│
├── README.md                     # Este arquivo
├── main.py                       # Arquivo principal (menu e controle do sistema)
├── contas.csv                    # Arquivo de armazenamento das contas de usuários
│
├── autenticacao/                 # Módulo de autenticação de usuários
│   ├── __init__.py
│   ├── autenticacao.py
│   ├── validacoes.py
│   ├── utilitarios.py
│
├── administracao/                # Módulo de administração de contas
│   ├── __init__.py
│   ├── gerenciarConta.py
│
├── analise/                      # Módulo de análise de dados de saúde
│   ├── __init__.py
│   ├── analisar_metricas.py
│   ├── carregar_dados_saude_lazy.py
│
├── dados/                        # Pasta para arquivos CSV de saúde (entrada de dados)
│   └── exemplo_batimentos.csv     # Exemplo opcional para testes


## Como Executar o Projeto

1. Instale o **Python 3.10** ou superior.
2. Clone ou baixe este repositório no seu computador.
3. Certifique-se de que todos os arquivos estão organizados conforme a estrutura acima.
4. No terminal, navegue até a pasta `problema-2/`:
    ```bash
    cd problema-2
    ```
5. Execute o sistema com:
    ```bash
    python main.py
    ```


## Tecnologias e Conceitos Aplicados

- **Python 3.10**
- **Programação funcional**:
  - Uso de funções puras.
  - Uso de `lambda`, `map`, `reduce` e iteradores (`Iterator`).
- **Modularização**:
  - Separação de responsabilidade por pastas e arquivos.
- **Tipagem** com o módulo `typing`.
- **Leitura e escrita de arquivos CSV**.
- **Tratamento de erros** e **validação de dados**.
- **Estilização do terminal** para melhor experiência de usuário.

##  Área do Paciente

O sistema permite que pacientes criem suas contas de forma independente, utilizando qualquer endereço de e-mail válido.  
Após realizar login, o paciente é direcionado à "Área do Paciente", onde atualmente é exibida uma mensagem de boas-vindas.

O sistema é arquitetado para permitir funcionalidades como:
- Gerenciamento de sua conta
- Consulta e inserção de seus próprios registros médicos.
- Acompanhamento de métricas de saúde.
- Visualização de relatórios personalizados de evolução.


## Exemplos de Funcionalidades

- Login com email de médico (`@medico.com`) leva ao **menu profissional**.
- Médicos podem carregar um arquivo `.csv` de registros de saúde e ver:
  - Média dos valores.
  - Mediana dos valores.
  - Moda dos valores.
  - Desvio padrão.
  - Variância.


## Observações

- **Cadastro de pacientes e médicos** é diferenciado apenas pelo domínio do email (ex.: `joao@medico.com`).
- As senhas são **armazenadas de forma segura** utilizando hashing SHA-256.
- O arquivo `contas.csv` é atualizado automaticamente com cada ação de criação, edição ou exclusão de conta.


## Equipe

- Projeto desenvolvido por: **Grupo 05 - RP III - UNIPAMPA (2025/1)**
- @author Emilly Dias

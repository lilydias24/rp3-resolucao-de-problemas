# Sistema de Gestão de Estoque

Sistema  de gestão de estoque desenvolvido durante a disciplina de RPIII - Problema I - em Python. 

## Funcionalidades

OBS : Armazenamento de dados em `.json`

1. Gerenciar produtos : 
- cadastrar produtos -> nome, descrição, valor, quant_estoque, nivel_min, entradas[ quantidade, data ], saidas[ quantidade, data ] 
- editar produtos
- deletar produtos
- listar produtos
2. Gerenciar pessoas : 
- cadastrar pessoa -> cliente = 1 ou fornecedor = 2 | tipo_pessoa, status (ativo ou inativo), cep, contato + nome e cpf para clientes ou razao_social e cnpj para fornecedores
- editar pessoa
- deletar pessoa
- listar pessoas
3. Gerenciar movimentações : 
- visualizar níveis de estoque -> verificar nível mínimo de produtos cadastrados
- cadastrar movimentação -> id_movimento, id_produto, id_pessoa, tipo_pessoa(cliente ou fornecedor), tipo_movimento (entrada ou saida ), quantidade, data 
- deletar movimentações
- listar movimentações 
- buscar registros de movimentações
4. Exibir o estoque atual com suas principais informações
5. Gerar relatório de movimentações em `.csv`

## Estrutura do Projeto

```
problema-1/
├── data/                  # Arquivos de dados (JSON e CSV)
├── src/                   # Códigos-fonte do sistema
├── main.py                # Início do sistema
├── estilo.py              # Estilização do sistema
└── README.md              # Este arquivo
```

## Como Executar

1. Navegue até a pasta do projeto:
```bash
cd problema-1/
```
2. Execute o sistema principal:
```bash
python main.py
```

## Dados

Os dados são armazenados localmente nos arquivos:

- `estoque.json`: Produtos cadastrados e suas quantidades
- `movimentacoes.json`: Histórico de movimentações
- `pessoas.json`: Responsáveis pelas movimentações

## Desenvolvedores

Feito por Emilly -> 2410100671
Feito por Douglas -> 2410102161
Feito por Eric -> 2410100672
Feito por Matheus -> 1901560224

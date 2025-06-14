"""
Interface para o Gestor Acadêmico gerenciar as regras de carreiras.
"""
import json
import os
from typing import Dict, Any, List
from .gestor import GestorRegras
from data.conexao import conectar, desconectar
from data.transacao import ConexaoErro
from reports.gerar_relatorios import gerar_relatorios

from data.estudante_db import (
    listar_estudantes,
    obter_disciplinas,
    buscar_estudante
)
from reports.graficos import GeradorGraficos
from data.relatorio_db import RelatorioDB
from utils.cores import (
    titulo, sucesso, erro, aviso, destaque, cabecalho,
    menu_item, info, score, negrito, sublinhado
)


DISCIPLINAS = [
    "Matemática",
    "Física",
    "Química",
    "Biologia",
    "Português",
    "História",
    "Geografia",
    "Artes",
    "Inglês",
    "Literatura",
    "Sociologia",
    "Filosofia"
]

INTERESSES = [
    "Tecnologia",
    "Ciências",
    "Saúde",
    "Humanas",
    "Arte",
    "Comunicação",
    "Negócios",
    "Construção",
    "Comportamento humano",
    "Justiça",
    "Gestão",
    "Comunicação visual",
    "Ajuda ao próximo"
]

HABILIDADES = [
    "Programação",
    "Lógica",
    "Redação",
    "Comunicação",
    "Atenção aos detalhes",
    "Empatia",
    "Argumentação",
    "Leitura",
    "Raciocínio lógico",
    "Desenho técnico",
    "Criatividade",
    "Edição de imagens",
    "Liderança",
    "Organização",
    "Escuta ativa"
]

CARREIRAS = [
    "Engenharia de Software",
    "Ciência da Computação",
    "Engenharia Civil",
    "Medicina",
    "Direito",
    "Psicologia",
    "Administração",
    "Design Gráfico",
    "Jornalismo",
    "Arquitetura",
    "Ciência de Dados",
    "Engenharia Elétrica",
    "Engenharia Mecânica",
    "Fisioterapia",
    "Nutrição"
]

def exibir_menu_gestor() -> str:
    """
    Exibe o menu do gestor acadêmico.
    
    Returns:
        Opção selecionada pelo usuário
    """
    print(cabecalho("Menu do Gestor Acadêmico"))
    print(menu_item("1", "Adicionar regra de carreira"))
    print(menu_item("2", "Editar regra de carreira"))
    print(menu_item("3", "Remover regra de carreira"))
    print(menu_item("4", "Listar regras de carreira"))
    print(menu_item("5", "Gerar relatórios"))
    print(menu_item("6", "Voltar ao menu principal"))
    return input("\n" + destaque("Escolha uma opção: ")).strip()

def selecionar_opcoes(titulo_texto, opcoes):
    """
    Permite que o usuário selecione múltiplas opções de uma lista.
    
    Args:
        titulo_texto: Título da seleção
        opcoes: Lista de opções disponíveis
        
    Returns:
        Lista com as opções selecionadas
    """
    print(cabecalho(titulo_texto))
    
    for i, opcao in enumerate(opcoes, 1):
        print(menu_item(str(i), opcao))
    
    while True:
        escolha = input("\n" + destaque("Digite os números das opções desejadas (separados por vírgula)\nExemplo: 1,3,5\n\nSua escolha: ")).strip()
        
        try:
            indices = [int(x.strip()) for x in escolha.split(',')]
            if all(1 <= i <= len(opcoes) for i in indices):
                return [opcoes[i-1] for i in indices]
            else:
                print(erro("\nNúmeros inválidos! Use apenas números entre 1 e", len(opcoes)))
        except ValueError:
            print(erro("\nFormato inválido! Use números separados por vírgula."))

def carregar_regras(caminho_arquivo: str) -> Dict[str, Any]:
    """
    Carrega as regras de carreira do arquivo JSON.
    
    Args:
        caminho_arquivo: Caminho do arquivo de regras
        
    Returns:
        Dicionário com as regras de carreira
        
    Raises:
        FileNotFoundError: Se o arquivo não existir
        json.JSONDecodeError: Se o arquivo não for um JSON válido
    """
    try:
        with open(caminho_arquivo, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(aviso(f"\nArquivo de regras não encontrado: {caminho_arquivo}"))
        return {"carreiras": []}
    except json.JSONDecodeError as e:
        print(f"\nErro ao carregar regras: {str(e)}")
        return {"carreiras": []}

def salvar_regras(caminho_arquivo: str, regras: Dict[str, Any]) -> None:
    """
    Salva as regras de carreira no arquivo JSON.
    
    Args:
        caminho_arquivo: Caminho do arquivo de regras
        regras: Dicionário com as regras de carreira
        
    Raises:
        IOError: Se houver erro ao salvar o arquivo
    """
    try:
        with open(caminho_arquivo, 'w', encoding='utf-8') as f:
            json.dump(regras, f, indent=2, ensure_ascii=False)
        print(sucesso("\nRegras salvas com sucesso!"))
    except IOError as e:
        print(f"\nErro ao salvar regras: {str(e)}")

def coletar_dados_regra() -> Dict[str, Any]:
    """
    Coleta os dados para uma nova regra de carreira.
    
    Returns:
        Dicionário com os dados da regra
    """
    print(cabecalho("Nova Regra de Carreira"))
    
    nome = input("\n" + destaque("Nome da carreira: ")).strip()
    if not nome:
        print(erro("\nNome da carreira não pode estar vazio!"))
        return None
    
    descricao = input("\n" + destaque("Descrição da carreira: ")).strip()
    if not descricao:
        print(erro("\nDescrição da carreira não pode estar vazia!"))
        return None
    
    print("\n" + destaque("Selecione os interesses necessários:"))
    interesses = selecionar_opcoes("Interesses", INTERESSES)
    
    print("\n" + destaque("Selecione as habilidades necessárias:"))
    habilidades = selecionar_opcoes("Habilidades", HABILIDADES)
    
    print("\n" + destaque("Defina as notas mínimas para cada disciplina:"))
    desempenho = {}
    for disciplina in DISCIPLINAS:
        while True:
            try:
                nota = float(input(f"\n{destaque(f'Nota mínima em {disciplina} (0-10): ')}").strip())
                if 0 <= nota <= 10:
                    desempenho[disciplina] = nota
                    break
                else:
                    print(erro("\nA nota deve estar entre 0 e 10!"))
            except ValueError:
                print(erro("\nPor favor, digite um número válido!"))
    
    justificativa = input("\n" + destaque("Justificativa para a carreira: ")).strip()
    if not justificativa:
        print(erro("\nJustificativa não pode estar vazia!"))
        return None
    
    return {
        "nome": nome,
        "descricao": descricao,
        "condicoes": {
            "interesses": interesses,
            "habilidades": habilidades,
            "desempenho": desempenho
        },
        "justificativa": justificativa
    }

def exibir_regra(regra: Dict[str, Any]) -> None:
    """
    Exibe os detalhes de uma regra.
    
    Args:
        regra: Regra a ser exibida
    """
    print(f"\n=== Regra: {regra['nome']} ===")
    print(f"\nDescrição: {regra['descricao']}")
    
    print("\nCondições:")
    condicoes = regra['condicoes']
    
    if condicoes.get('interesses'):
        print("\nInteresses necessários:")
        for interesse in condicoes['interesses']:
            print(f"- {interesse}")
    
    if condicoes.get('habilidades'):
        print("\nHabilidades necessárias:")
        for habilidade in condicoes['habilidades']:
            print(f"- {habilidade}")
    
    if condicoes.get('desempenho'):
        print("\nNotas mínimas necessárias:")
        for disciplina, nota in condicoes['desempenho'].items():
            print(f"- {disciplina}: {nota}")

def executar_menu_gestor(caminho_regras: str) -> None:
    """
    Executa o menu do gestor acadêmico.
    
    Args:
        caminho_regras: Caminho do arquivo de regras
    """
    while True:
        opcao = exibir_menu_gestor()
        
        if opcao == "1":  # Adicionar regra
            regras = carregar_regras(caminho_regras)
            nova_regra = coletar_dados_regra()
            
            if nova_regra:
                regras["carreiras"].append(nova_regra)
                salvar_regras(caminho_regras, regras)
        
        elif opcao == "2":  # Editar regra
            regras = carregar_regras(caminho_regras)
            if not regras["carreiras"]:
                print(aviso("\nNão há regras para editar!"))
                continue
                
            print(cabecalho("Editar Regra de Carreira"))
            for i, regra in enumerate(regras["carreiras"], 1):
                print(menu_item(str(i), regra['nome']))
            
            try:
                indice = int(input("\n" + destaque("Digite o número da regra a editar: ")).strip()) - 1
                if 0 <= indice < len(regras["carreiras"]):
                    regras["carreiras"][indice] = coletar_dados_regra()
                    salvar_regras(caminho_regras, regras)
                else:
                    print(erro("\nNúmero de regra inválido!"))
            except ValueError:
                print(erro("\nPor favor, digite um número válido!"))
            
        elif opcao == "3":  # Remover regra
            regras = carregar_regras(caminho_regras)
            if not regras["carreiras"]:
                print(aviso("\nNão há regras para remover!"))
                continue
                
            print(cabecalho("Remover Regra de Carreira"))
            for i, regra in enumerate(regras["carreiras"], 1):
                print(menu_item(str(i), regra['nome']))
            
            try:
                indice = int(input("\n" + destaque("Digite o número da regra a remover: ")).strip()) - 1
                if 0 <= indice < len(regras["carreiras"]):
                    regra_removida = regras["carreiras"].pop(indice)
                    salvar_regras(caminho_regras, regras)
                    print(f"\nRegra '{regra_removida['nome']}' removida com sucesso!")
                else:
                    print(erro("\nNúmero de regra inválido!"))
            except ValueError:
                print(erro("\nPor favor, digite um número válido!"))
            
        elif opcao == "4":  # Listar regras
            regras = carregar_regras(caminho_regras)
            if not regras["carreiras"]:
                print(aviso("\nNão há regras cadastradas!"))
                continue
                
            print(cabecalho("Regras de Carreira"))
            for regra in regras["carreiras"]:
                print(f"\n{destaque('Carreira:')} {negrito(regra['nome'])}")
                print(f"{destaque('Descrição:')} {regra['descricao']}")
                print(f"\n{destaque('Interesses:')}")
                for interesse in regra['condicoes']['interesses']:
                    print(f"  • {info(interesse)}")
                print(f"\n{destaque('Habilidades:')}")
                for habilidade in regra['condicoes']['habilidades']:
                    print(f"  • {info(habilidade)}")
                print(f"\n{destaque('Desempenho:')}")
                for disciplina, nota in regra['condicoes']['desempenho'].items():
                    print(f"  • {disciplina}: {nota}")
                print(f"\n{destaque('Justificativa:')} {regra['justificativa']}")
                print(separador('-'))
            
        elif opcao == "5":  # Gerar relatórios
            try:
                gerar_relatorios()
            except Exception as e:
                print(f"\nErro ao gerar relatório: {str(e)}")
            
        elif opcao == "6":  # Voltar
            break
            
        else:
            print(erro("\nOpção inválida! Por favor, escolha uma opção válida."))
        
        input("\n" + destaque("Pressione Enter para continuar..."))
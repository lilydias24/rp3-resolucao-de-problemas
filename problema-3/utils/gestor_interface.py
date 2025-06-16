"""
Módulo de interface do gestor acadêmico.

Contém funções para interação com o gestor acadêmico via terminal.
"""
import json
import sys
import os
from typing import Dict, List, Tuple, Any
from utils.cores import (
    titulo, sucesso, erro, aviso, destaque, 
    cabecalho, menu_item, info, score, 
    negrito, sublinhado, separador
)
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Constantes para validação
INTERESSES = [
    "Matemática", "Física", "Química", "Biologia", "Computação",
    "Engenharia", "Medicina", "Direito", "Administração", "Artes",
    "Música", "Literatura", "História", "Geografia", "Filosofia",
    "Psicologia", "Sociologia", "Economia", "Contabilidade", "Marketing"
]

HABILIDADES = [
    "Raciocínio Lógico", "Criatividade", "Comunicação", "Trabalho em Equipe",
    "Liderança", "Resolução de Problemas", "Análise de Dados", "Programação",
    "Gestão de Projetos", "Pensamento Crítico", "Adaptabilidade", "Inovação",
    "Negociação", "Planejamento", "Organização", "Pesquisa", "Escrita",
    "Apresentação", "Gestão de Tempo", "Tomada de Decisão"
]

DISCIPLINAS = [
    "Matemática", "Física", "Química", "Biologia", "Português",
    "Literatura", "História", "Geografia", "Filosofia", "Sociologia",
    "Inglês", "Artes", "Educação Física", "Redação"
]

class GestorInterface:
    """
    Classe que gerencia a interface do gestor acadêmico.
    """
    
    @staticmethod
    def coletar_dados_regra() -> Dict[str, Any]:
        """
        Coleta os dados para uma nova regra de carreira.
        
        Returns:
            Dict com os dados da regra
        """
        print(cabecalho("Cadastro de Nova Regra de Carreira"))
        print(separador())
        
        # Nome da carreira
        carreira = input(destaque("Nome da carreira: ")).strip()
        while not carreira:
            print(erro("Nome da carreira não pode estar vazio!"))
            carreira = input(destaque("Nome da carreira: ")).strip()
        
        # Justificativa
        justificativa = input(destaque("Justificativa para a carreira: ")).strip()
        while not justificativa:
            print(erro("Justificativa não pode estar vazia!"))
            justificativa = input(destaque("Justificativa para a carreira: ")).strip()
        
        # Interesses necessários
        print("\n" + destaque("Selecione os interesses necessários:"))
        print(separador())
        for i, interesse in enumerate(INTERESSES, 1):
            print(f"{i}. {interesse}")
        print(separador())
        
        interesses = []
        while True:
            try:
                opcao = input(destaque("Digite o número do interesse (ou 0 para terminar): ")).strip()
                if opcao == "0":
                    break
                idx = int(opcao) - 1
                if 0 <= idx < len(INTERESSES):
                    interesse = INTERESSES[idx]
                    if interesse not in interesses:
                        interesses.append(interesse)
                        print(sucesso(f"Interesse '{interesse}' adicionado!"))
                    else:
                        print(aviso(f"Interesse '{interesse}' já foi adicionado!"))
                else:
                    print(erro("Opção inválida!"))
            except ValueError:
                print(erro("Digite um número válido!"))
        
        # Habilidades necessárias
        print("\n" + destaque("Selecione as habilidades necessárias:"))
        print(separador())
        for i, habilidade in enumerate(HABILIDADES, 1):
            print(f"{i}. {habilidade}")
        print(separador())
        
        habilidades = []
        while True:
            try:
                opcao = input(destaque("Digite o número da habilidade (ou 0 para terminar): ")).strip()
                if opcao == "0":
                    break
                idx = int(opcao) - 1
                if 0 <= idx < len(HABILIDADES):
                    habilidade = HABILIDADES[idx]
                    if habilidade not in habilidades:
                        habilidades.append(habilidade)
                        print(sucesso(f"Habilidade '{habilidade}' adicionada!"))
                    else:
                        print(aviso(f"Habilidade '{habilidade}' já foi adicionada!"))
                else:
                    print(erro("Opção inválida!"))
            except ValueError:
                print(erro("Digite um número válido!"))
        
        # Desempenho necessário
        print("\n" + destaque("Digite o desempenho necessário para cada disciplina:"))
        print(separador())
        print("Digite as notas mínimas para cada disciplina (0-10)")
        print("Deixe em branco para pular uma disciplina")
        print(separador())
        
        desempenho = {}
        pesos = {}
        for disciplina in DISCIPLINAS:
            while True:
                nota = input(destaque(f"{disciplina}: ")).strip()
                if not nota:
                    break
                try:
                    nota = float(nota)
                    if 0 <= nota <= 10:
                        desempenho[disciplina] = nota
                        peso = input(destaque(f"Peso para {disciplina} (1-5, padrão=1): ")).strip()
                        if peso:
                            try:
                                peso = float(peso)
                                if 1 <= peso <= 5:
                                    pesos[disciplina] = peso
                                else:
                                    print(aviso("Peso deve estar entre 1 e 5. Usando peso padrão."))
                            except ValueError:
                                print(aviso("Peso inválido. Usando peso padrão."))
                        break
                    else:
                        print(erro("A nota deve estar entre 0 e 10!"))
                except ValueError:
                    print(erro("Digite um número válido!"))
        
        return {
            'carreira': carreira,
            'justificativa': justificativa,
            'condicoes': {
                'interesses': interesses,
                'habilidades': habilidades,
                'desempenho': desempenho,
                'pesos': pesos
            }
        }

    @staticmethod
    def exibir_regra(regra: Dict) -> None:
        """
        Exibe os dados de uma regra de carreira de forma organizada.
        
        Args:
            regra: Dicionário com os dados da regra
        """
        print(separador())
        print(f"\n{destaque('Carreira:')} {negrito(regra['carreira'])}")
        print(f"{destaque('Justificativa:')} {regra['justificativa']}")
        
        print(f"\n{destaque('Interesses necessários:')}")
        if regra['condicoes']['interesses']:
            for interesse in regra['condicoes']['interesses']:
                print(f"  • {info(interesse)}")
        else:
            print(aviso("  Nenhum interesse necessário"))
        
        print(f"\n{destaque('Habilidades necessárias:')}")
        if regra['condicoes']['habilidades']:
            for habilidade in regra['condicoes']['habilidades']:
                print(f"  • {info(habilidade)}")
        else:
            print(aviso("  Nenhuma habilidade necessária"))
        
        print(f"\n{destaque('Desempenho necessário:')}")
        if regra['condicoes']['desempenho']:
            for disciplina, nota in regra['condicoes']['desempenho'].items():
                peso = regra['condicoes']['pesos'].get(disciplina, 1.0)
                print(f"  • {disciplina}: {score(nota)} (peso: {peso})")
        else:
            print(aviso("  Nenhum desempenho necessário"))
        
        print(separador())
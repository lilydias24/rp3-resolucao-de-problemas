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
    def coletar_dados_regra(regra_atual: Dict = None) -> Dict[str, Any]:
        """
        Coleta os dados para uma regra de carreira.
        
        Args:
            regra_atual: Dicionário com os dados atuais da regra (opcional)
            
        Returns:
            Dicionário com os dados da regra
        """
        print("\n" + destaque("Cadastro de Regra de Carreira"))
        print(separador())
        
        # Nome da carreira
        nome_atual = regra_atual.get('carreira', '') if regra_atual else ''
        carreira = input(destaque(f"Nome da carreira ({nome_atual}): ")).strip()
        if not carreira and regra_atual:
            carreira = nome_atual
        
        # Justificativa
        justificativa_atual = regra_atual.get('justificativa', '') if regra_atual else ''
        justificativa = input(destaque(f"Justificativa ({justificativa_atual}): ")).strip()
        if not justificativa and regra_atual:
            justificativa = justificativa_atual
        
        # Interesses
        print("\n" + destaque("Digite os interesses necessários:"))
        print(separador())
        print("Digite um interesse por linha")
        print("Pressione Enter duas vezes para manter os interesses atuais")
        
        interesses = []
        if regra_atual:
            print("\nInteresses atuais:")
            for interesse in regra_atual.get('condicoes', {}).get('interesses', []):
                print(f"  • {interesse}")
        
        while True:
            interesse = input(destaque("> ")).strip()
            if not interesse:
                if not interesses and regra_atual:  # Se não digitou nenhum interesse novo
                    interesses = regra_atual.get('condicoes', {}).get('interesses', [])  # Mantém os atuais
                break
            interesses.append(interesse)
        
        # Habilidades
        print("\n" + destaque("Digite as habilidades necessárias:"))
        print(separador())
        print("Digite uma habilidade por linha")
        print("Pressione Enter duas vezes para manter as habilidades atuais")
        
        habilidades = []
        if regra_atual:
            print("\nHabilidades atuais:")
            for habilidade in regra_atual.get('condicoes', {}).get('habilidades', []):
                print(f"  • {habilidade}")
        
        while True:
            habilidade = input(destaque("> ")).strip()
            if not habilidade:
                if not habilidades and regra_atual:  # Se não digitou nenhuma habilidade nova
                    habilidades = regra_atual.get('condicoes', {}).get('habilidades', [])  # Mantém as atuais
                break
            habilidades.append(habilidade)
        
        # Desempenho necessário
        print("\n" + destaque("Digite o desempenho necessário para cada disciplina:"))
        print(separador())
        print("Digite as notas mínimas para cada disciplina (0-10)")
        print("Deixe em branco para manter a nota atual")
        print(separador())
        
        desempenho = {}
        pesos = {}
        if regra_atual:
            print("\nDesempenho atual:")
            for disciplina, nota in regra_atual.get('condicoes', {}).get('desempenho', {}).items():
                peso = regra_atual.get('condicoes', {}).get('pesos', {}).get(disciplina, 1.0)
                print(f"  • {disciplina}: {nota} (peso: {peso})")
        
        for disciplina in DISCIPLINAS:
            nota_atual = regra_atual.get('condicoes', {}).get('desempenho', {}).get(disciplina) if regra_atual else None
            peso_atual = regra_atual.get('condicoes', {}).get('pesos', {}).get(disciplina, 1.0) if regra_atual else 1.0
            
            while True:
                nota = input(destaque(f"{disciplina} ({nota_atual if nota_atual is not None else 'não definida'}): ")).strip()
                if not nota:
                    if nota_atual is not None:  # Se tinha nota definida
                        desempenho[disciplina] = nota_atual
                        pesos[disciplina] = peso_atual
                    break
                try:
                    nota = float(nota)
                    if 0 <= nota <= 10:
                        desempenho[disciplina] = nota
                        peso = input(destaque(f"Peso para {disciplina} (1-5, atual={peso_atual}): ")).strip()
                        if peso:
                            try:
                                peso = float(peso)
                                if 1 <= peso <= 5:
                                    pesos[disciplina] = peso
                                else:
                                    print(aviso("Peso deve estar entre 1 e 5. Mantendo peso atual."))
                                    pesos[disciplina] = peso_atual
                            except ValueError:
                                print(aviso("Peso inválido. Mantendo peso atual."))
                                pesos[disciplina] = peso_atual
                        else:
                            pesos[disciplina] = peso_atual
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
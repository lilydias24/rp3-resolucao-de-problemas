"""
Módulo de gerenciamento de interface.

Contém funções para gerenciar a interface do sistema.
"""
import json
import sys
import os
from typing import Dict, List, Tuple, Any
import unicodedata

from utils.cores import (
    titulo, sucesso, erro, aviso, destaque, 
    menu_item, info, score, negrito, sublinhado,
    cabecalho, separador
)

# Lista de disciplinas disponíveis
DISCIPLINAS: List[str] = [
    "Matemática",
    "Português",
    "História",
    "Geografia",
    "Física",
    "Química",
    "Biologia",
    "Inglês",
    "Literatura",
    "Artes",
    "Educação Física",
    "Filosofia",
    "Sociologia"
]

# Lista de interesses disponíveis
INTERESSES: List[str] = [
    "Tecnologia",
    "Ciências",
    "Artes",
    "Esportes",
    "Literatura",
    "Música",
    "Matemática",
    "História",
    "Geografia",
    "Línguas",
    "Filosofia",
    "Psicologia",
    "Medicina",
    "Direito",
    "Engenharia",
    "Administração",
    "Marketing",
    "Design",
    "Comunicação",
    "Educação"
]

# Lista de habilidades disponíveis
HABILIDADES: List[str] = [
    "Liderança",
    "Trabalho em equipe",
    "Comunicação",
    "Criatividade",
    "Resolução de problemas",
    "Pensamento crítico",
    "Organização",
    "Adaptabilidade",
    "Proatividade",
    "Empatia",
    "Negociação",
    "Gestão de tempo",
    "Análise de dados",
    "Programação",
    "Design",
    "Escrita",
    "Oratória",
    "Pesquisa",
    "Planejamento",
    "Raciocínio Lógico",
    "Inovação"
]

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from .gestor import GestorRegras
from data.conexao import conectar
from data.transacao import ConexaoErro
from reports.gerar_relatorios import gerar_relatorios
from data.relatorio_db import listar_estudantes
from logic.estudante import buscar_estudante
from reports.graficos import GeradorGraficos
from data.relatorio_db import RelatorioDB

class GestorInterface:
    """
    Classe que gerencia a interface do gestor acadêmico.
    """
    
    @staticmethod
    def exibir_menu_gestor() -> str:
        """
        Exibe o menu do gestor acadêmico.
        
        Returns:
            str: Opção escolhida pelo usuário
        """
        print(cabecalho("Menu do Gestor Acadêmico"))
        print(menu_item("\t 1", "Adicionar regra de carreira"))
        print(menu_item("\t 2", "Editar regra de carreira"))
        print(menu_item("\t 3", "Remover regra de carreira"))
        print(menu_item("\t 4", "Listar regras de carreira"))
        print(menu_item("\t 5", "Gerar relatórios"))
        print(menu_item("\t 6", "Gerar gráficos"))
        print(menu_item("\t 7", "Voltar ao menu principal"))
        return input("\n" + destaque(">>> Escolha uma opção: ")).strip()

    @staticmethod
    def exibir_menu_relatorios() -> str:
        """
        Exibe o menu de relatórios.
        
        Returns:
            str: Opção escolhida pelo usuário
        """
        print(cabecalho("Menu de Relatórios"))
        print(menu_item("\t 1", "Gerar relatório de estudantes"))
        print(menu_item("\t 2", "Gerar relatório de regras"))
        print(menu_item("\t 3", "Gerar relatório de estatísticas"))
        print(menu_item("\t 4", "Gerar relatório de tendências"))
        print(menu_item("\t 5", "Gerar todos os relatórios"))
        print(menu_item("\t 6", "Voltar ao menu do gestor"))
        return input("\n" + destaque(">>> Escolha uma opção: ")).strip()

    @staticmethod
    def exibir_menu_formato_relatorio() -> str:
        """
        Exibe o menu de seleção de formato do relatório.
        
        Returns:
            str: Opção escolhida pelo usuário
        """
        print(cabecalho("Formato do Relatório"))
        print(menu_item("\t 1", "JSON"))
        print(menu_item("\t 2", "CSV"))
        return input("\n" + destaque(">>> Escolha o formato: ")).strip()

    @staticmethod
    def exibir_menu_graficos() -> str:
        """
        Exibe o menu de gráficos.
        
        Returns:
            str: Opção escolhida pelo usuário
        """
        print(cabecalho("Menu de Gráficos"))
        print(menu_item("\t 1", "Gerar gráficos de desempenho por estudante"))
        print(menu_item("\t 2", "Gerar gráficos de desempenho por disciplina"))
        print(menu_item("\t 3", "Gerar gráfico de distribuição de recomendações"))
        print(menu_item("\t 4", "Gerar todos os gráficos"))
        print(menu_item("\t 5", "Voltar ao menu do gestor"))
        return input("\n" + destaque(">>> Escolha uma opção: ")).strip()

def normalizar(texto):
    return unicodedata.normalize('NFKD', texto.strip().lower()).encode('ASCII', 'ignore').decode('ASCII')

def coletar_dados_regra() -> Dict[str, Any]:
    """
    Coleta os dados para uma nova regra.
    
    Returns:
        Dict[str, Any]: Dicionário com os dados da regra
    """
    print(cabecalho("Dados da Regra"))
    
    carreira = input(destaque("Nome da carreira: ")).strip()
    if not carreira:
        print(erro("Nome da carreira é obrigatório!"))
        return None
        
    print("\n" + destaque("Interesses disponíveis:"))
    for interesse in INTERESSES:
        print(f"- {interesse}")
    print("\n" + destaque("Digite os interesses (um por linha, deixe em branco para terminar):"))
    interesses = []
    interesses_norm = {normalizar(i): i for i in INTERESSES}
    while True:
        interesse = input().strip()
        if not interesse:
            break
        chave = normalizar(interesse)
        if chave in interesses_norm:
            interesses.append(interesses_norm[chave])
        else:
            print(erro(f"Interesse '{interesse}' não é válido! Use um dos interesses listados acima."))
            
    print("\n" + destaque("Habilidades disponíveis:"))
    for habilidade in HABILIDADES:
        print(f"- {habilidade}")
    print("\n" + destaque("Digite as habilidades (um por linha, deixe em branco para terminar):"))
    habilidades = []
    habilidades_norm = {normalizar(h): h for h in HABILIDADES}
    while True:
        habilidade = input().strip()
        if not habilidade:
            break
        chave = normalizar(habilidade)
        if chave in habilidades_norm:
            habilidades.append(habilidades_norm[chave])
        else:
            print(erro(f"Habilidade '{habilidade}' não é válida! Use uma das habilidades listadas acima."))
            
    print("\n" + destaque("Desempenho acadêmico (nota de 0 a 10):"))
    desempenho = {}
    for disciplina in DISCIPLINAS:
        while True:
            try:
                nota = input(f"{disciplina}: ").strip()
                if not nota:
                    print(erro("Nota é obrigatória!"))
                    continue
                nota = float(nota)
                if 0 <= nota <= 10:
                    desempenho[disciplina] = nota
                    break
                else:
                    print(erro("Nota deve estar entre 0 e 10!"))
            except ValueError:
                print(erro("Digite um número válido!"))
                
    print("\n" + destaque("Pesos (0 a 1):"))
    print("Os pesos determinam a importância de cada critério na recomendação.")
    print("A soma dos pesos deve ser igual a 1.")
    pesos = {}
    while True:
        try:
            peso_interesses = input("Peso dos interesses (0 a 1): ").strip()
            if not peso_interesses:
                print(erro("Peso é obrigatório!"))
                continue
            peso_interesses = float(peso_interesses)
            
            peso_habilidades = input("Peso das habilidades (0 a 1): ").strip()
            if not peso_habilidades:
                print(erro("Peso é obrigatório!"))
                continue
            peso_habilidades = float(peso_habilidades)
            
            peso_desempenho = input("Peso do desempenho (0 a 1): ").strip()
            if not peso_desempenho:
                print(erro("Peso é obrigatório!"))
                continue
            peso_desempenho = float(peso_desempenho)
            
            if not all(0 <= p <= 1 for p in [peso_interesses, peso_habilidades, peso_desempenho]):
                print(erro("Todos os pesos devem estar entre 0 e 1!"))
                continue
                
            soma = peso_interesses + peso_habilidades + peso_desempenho
            if abs(soma - 1.0) > 0.001:  # Usando uma pequena margem de erro para comparação de float
                print(erro(f"A soma dos pesos deve ser igual a 1! (atual: {soma:.2f})"))
                continue
                
            pesos = {
                "interesses": peso_interesses,
                "habilidades": peso_habilidades,
                "desempenho": peso_desempenho
            }
            break
            
        except ValueError:
            print(erro("Digite um número válido!"))
    
    return {
        "carreira": carreira,
        "condicoes": {
            "interesses": interesses,
            "habilidades": habilidades,
            "desempenho": desempenho,
            "pesos": pesos
        }
    }

def exibir_regra(regra: Dict[str, Any]) -> None:
    """
    Exibe os dados de uma regra.
    
    Args:
        regra: Dicionário com os dados da regra
    """
    print(cabecalho(regra["carreira"]))
    
    if regra.get("justificativa"):
        print(destaque("\nJustificativa:"))
        print(regra["justificativa"])
    
    print(destaque("\nInteresses:"))
    for interesse in sorted(regra["condicoes"]["interesses"]):
        print(f"- {interesse}")
        
    print(destaque("\nHabilidades:"))
    for habilidade in sorted(regra["condicoes"]["habilidades"]):
        print(f"- {habilidade}")
        
    print(destaque("\nDesempenho:"))
    for disciplina, nota in sorted(regra["condicoes"]["desempenho"].items()):
        print(f"- {disciplina}: {nota}")
        
    print(destaque("\nPesos:"))
    for tipo, peso in sorted(regra["condicoes"]["pesos"].items()):
        print(f"- {tipo}: {peso}")

def executar_menu_gestor(motor) -> None:
    """
    Executa o menu do gestor acadêmico.
    
    Args:
        motor: Instância do motor de inferência
    """
    from logic.motor import MotorDeInferencia
    if not isinstance(motor, MotorDeInferencia):
        raise TypeError("motor deve ser uma instância de MotorDeInferencia")
        
    while True:
        opcao = GestorInterface.exibir_menu_gestor()
        
        if opcao == "1":
            regra = coletar_dados_regra()
            if regra:
                try:
                    motor.adicionar_regra(regra)
                    print(sucesso("\nRegra adicionada com sucesso!"))
                except Exception as e:
                    print(erro(f"\nErro ao adicionar regra: {str(e)}"))
                    
        elif opcao == "2":
            regras = motor.listar_regras()
            if not regras:
                print(aviso("\nNenhuma regra cadastrada!"))
                continue
                
            print(cabecalho("Regras Cadastradas"))
            for i, regra in enumerate(regras, 1):
                print(f"\n{i}. {regra['carreira']} [ID: {regra['id']}]")
                
            try:
                idx = int(input("\n" + destaque("Digite o número da regra a editar: ")).strip())
                if 1 <= idx <= len(regras):
                    regra = coletar_dados_regra()
                    if regra:
                        motor.atualizar_regra(regras[idx-1]['id'], regra)
                        print(sucesso("\nRegra atualizada com sucesso!"))
                else:
                    print(erro("\nNúmero de regra inválido!"))
            except ValueError:
                print(erro("\nEntrada inválida! Digite apenas números."))
                
        elif opcao == "3":
            regras = motor.listar_regras()
            if not regras:
                print(aviso("\nNenhuma regra cadastrada!"))
                continue
                
            print(cabecalho("Regras Cadastradas"))
            for i, regra in enumerate(regras, 1):
                print(f"\n{i}. {regra['carreira']} [ID: {regra['id']}]")
                
            try:
                idx = int(input("\n" + destaque("Digite o número da regra a remover: ")).strip())
                if 1 <= idx <= len(regras):
                    motor.remover_regra(regras[idx-1]['id'])
                    print(sucesso("\nRegra removida com sucesso!"))
                else:
                    print(erro("\nNúmero de regra inválido!"))
            except ValueError:
                print(erro("\nEntrada inválida! Digite apenas números."))
                
        elif opcao == "4":
            regras = motor.listar_regras()
            if not regras:
                print(aviso("\nNenhuma regra cadastrada!"))
                continue
                
            print(cabecalho("Regras de Carreira"))
            for regra in sorted(regras, key=lambda x: x['carreira']):
                print(f"\n[ID: {regra['id']}]")
                exibir_regra(regra)
                print("\n" + "="*50 + "\n")
                
        elif opcao == "5":
            try:
                gerar_relatorios()
                print(sucesso("\nRelatórios gerados com sucesso!"))
            except Exception as e:
                print(erro(f"\nErro ao gerar relatórios: {str(e)}"))
                
        elif opcao == "6":
            try:
                GeradorGraficos.gerar_graficos()
                print(sucesso("\nGráficos gerados com sucesso!"))
            except Exception as e:
                print(erro(f"\nErro ao gerar gráficos: {str(e)}"))
                
        elif opcao == "7":
            break
            
        else:
            print(erro("\nOpção inválida!"))
            
        input("\nPressione Enter para continuar...")

def validar_interesses(interesses: List[str]) -> bool:
    """
    Valida se os interesses informados são válidos.
    
    Args:
        interesses: Lista de interesses a serem validados
        
    Returns:
        bool: True se todos os interesses são válidos, False caso contrário
    """
    return all(interesse in INTERESSES for interesse in interesses)

def validar_habilidades(habilidades: List[str]) -> bool:
    """
    Valida se as habilidades informadas são válidas.
    
    Args:
        habilidades: Lista de habilidades a serem validadas
        
    Returns:
        bool: True se todas as habilidades são válidas, False caso contrário
    """
    return all(habilidade in HABILIDADES for habilidade in habilidades)

def validar_disciplinas(disciplinas: Dict[str, float]) -> bool:
    """
    Valida se as disciplinas e notas informadas são válidas.
    
    Args:
        disciplinas: Dicionário com disciplinas e notas
        
    Returns:
        bool: True se todas as disciplinas e notas são válidas, False caso contrário
    """
    return all(
        disciplina in DISCIPLINAS and 
        0 <= nota <= 10 
        for disciplina, nota in disciplinas.items()
    )
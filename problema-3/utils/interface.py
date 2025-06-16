"""
Módulo de interface com o usuário.

Contém funções para interação com o usuário via terminal.
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
from utils.gestor_interface import INTERESSES, HABILIDADES, DISCIPLINAS
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class Interface:
    """
    Classe que gerencia a interface do usuário do sistema.
    """
    
    @staticmethod
    def exibir_menu_principal() -> str:
        """
        Exibe o menu principal do sistema.
        
        Returns:
            str: Opção escolhida pelo usuário
        """
        print(cabecalho("Sistema de Recomendação de Carreiras"))
        print(menu_item("\t 1", "Cadastrar novo estudante"))
        print(menu_item("\t 2", "Listar estudantes cadastrados"))
        print(menu_item("\t 3", "Buscar estudante por nome"))
        print(menu_item("\t 4", "Ver recomendações de carreira"))
        print(menu_item("\t 5", "Menu do Gestor Acadêmico"))
        print(menu_item("\t 6", "Sair do sistema"))
        return input("\n" + destaque(">>> Escolha uma opção: ")).strip()

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
        print(menu_item("\t 2", "Gerar relatório de carreiras"))
        print(menu_item("\t 3", "Voltar ao menu do gestor"))
        return input("\n" + destaque(">>> Escolha uma opção: ")).strip()

    @staticmethod
    def exibir_menu_graficos() -> str:
        """
        Exibe o menu de gráficos.
        
        Returns:
            str: Opção escolhida pelo usuário
        """
        print(cabecalho("Menu de Gráficos"))
        print(menu_item("\t 1", "Gerar gráfico de estudantes"))
        print(menu_item("\t 2", "Gerar gráfico de carreiras"))
        print(menu_item("\t 3", "Voltar ao menu do gestor"))
        return input("\n" + destaque(">>> Escolha uma opção: ")).strip()

    @staticmethod
    def exibir_dados_estudante(estudante: Tuple) -> None:
        """
        Exibe os dados de um estudante de forma organizada.
        
        Args:
            estudante: Tupla com os dados do estudante (id, nome, interesses, habilidades, desempenho)
        """
        id_, nome, interesses, habilidades, desempenho = estudante
        
        print(separador())
        print(destaque("ID:") + f" {id_}")
        print(destaque("Nome:") + f" {nome}")
        
        print("\n" + destaque("Interesses:"))
        if interesses:
            for interesse in interesses:
                print(f"  • {info(interesse)}")
        else:
            print(aviso("  Nenhum interesse registrado"))
        
        print("\n" + destaque("Habilidades:"))
        if habilidades:
            for habilidade in habilidades:
                print(f"  • {info(habilidade)}")
        else:
            print(aviso("  Nenhuma habilidade registrada"))
        
        print("\n" + destaque("Desempenho Acadêmico:"))
        if desempenho:
            for disciplina, nota in desempenho.items():
                print(f"  • {disciplina}: {score(nota)}")
        else:
            print(aviso("  Nenhum desempenho registrado"))
        print(separador())

    @staticmethod
    def exibir_recomendacoes(recomendacoes: Dict[str, List], nome: str = None) -> None:
        """
        Exibe as recomendações de carreira de forma organizada.
        
        Args:
            recomendacoes: Dicionário com carreiras recomendadas e próximas
            nome: Nome do estudante (opcional)
        """
        recomendadas = recomendacoes['recomendadas']
        proximas = recomendacoes['proximas']
        
        titulo_recomendacoes = "Recomendações de Carreira"
        if nome:
            titulo_recomendacoes += f" para {nome}"
        
        print(cabecalho(titulo_recomendacoes))
        print(separador())
        
        print(destaque("Carreiras Recomendadas:"))
        if recomendadas:
            for c in recomendadas:
                print(f"\n  {destaque('•')} {negrito(c['carreira'])} {score(c['score'])}")
                print(f"    {sublinhado('Justificativa:')} {c['justificativa']}")
                print(f"\n    {sublinhado('Explicação:')}")
                for tipo, explicacao in c['explicacao'].items():
                    print(f"    {destaque('•')} {explicacao}")
        else:
            print("\n" + aviso("  Nenhuma carreira recomendada no momento."))
            print(aviso("  Para ter uma carreira recomendada, você precisa atender TODOS os critérios"))
            print(aviso("  (interesses, habilidades e desempenho) para pelo menos uma carreira."))
        
        print("\n" + destaque("Carreiras Próximas:"))
        if proximas:
            for c in proximas:
                print(f"\n  {destaque('•')} {negrito(c['carreira'])} {score(c['score'])}")
                print(f"    {sublinhado('Justificativa:')} {c['justificativa']}")
                print(f"\n    {sublinhado('Explicação:')}")
                for tipo, explicacao in c['explicacao'].items():
                    print(f"    {destaque('•')} {explicacao}")
                
                print(f"\n    {sublinhado('Sugestões para transformar em carreira recomendada:')}")
                for tipo, explicacao in c['explicacao'].items():
                    if "Faltam" in explicacao:
                        print(f"    {destaque('•')} {explicacao.replace('Faltam', 'Adquira')}")
        else:
            print(aviso("  Nenhuma carreira próxima no momento."))
        print(separador())

    @staticmethod
    def exibir_lista_estudantes(estudantes: List[Tuple]) -> None:
        """
        Exibe a lista de estudantes de forma organizada.
        
        Args:
            estudantes: Lista de tuplas com dados dos estudantes
        """
        if not estudantes:
            print(aviso("\nNenhum estudante cadastrado."))
            return
        
        print(cabecalho("Lista de Estudantes"))
        print(separador())
        
        for estudante in estudantes:
            Interface.exibir_dados_estudante(estudante)
            print("\n")

    @staticmethod
    def exibir_lista_regras(regras: List[Dict]) -> None:
        """
        Exibe a lista de regras de carreira de forma organizada.
        
        Args:
            regras: Lista de dicionários com dados das regras
        """
        if not regras:
            print(aviso("\nNenhuma regra de carreira cadastrada."))
            return
        
        print(cabecalho("Lista de Regras de Carreira"))
        print(separador())
        
        for regra in regras:
            print(f"\n{destaque('ID:')} {regra['id']}")
            print(f"{destaque('Carreira:')} {negrito(regra['carreira'])}")
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

    @staticmethod
    def solicitar_nome_estudante() -> str:
        """
        Solicita o nome do estudante ao usuário.
        
        Returns:
            str: Nome do estudante
        """
        return input("\n" + destaque("Digite o nome do estudante: ")).strip()

    @staticmethod
    def exibir_erro(mensagem: str) -> None:
        """
        Exibe uma mensagem de erro.
        
        Args:
            mensagem: Mensagem de erro a ser exibida
        """
        print(erro(f"\n{mensagem}"))

    @staticmethod
    def exibir_sucesso(mensagem: str) -> None:
        """
        Exibe uma mensagem de sucesso.
        
        Args:
            mensagem: Mensagem de sucesso a ser exibida
        """
        print(sucesso(f"\n{mensagem}"))

    @staticmethod
    def exibir_aviso(mensagem: str) -> None:
        """
        Exibe uma mensagem de aviso.
        
        Args:
            mensagem: Mensagem de aviso a ser exibida
        """
        print(aviso(f"\n{mensagem}"))

    @staticmethod
    def confirmar_saida() -> bool:
        """
        Solicita confirmação para sair do sistema.
        
        Returns:
            bool: True se o usuário confirmou a saída, False caso contrário
        """
        return input("\n" + destaque("Tem certeza que deseja sair? (s/n): ")).lower() == 's'

    @staticmethod
    def aguardar_continuar() -> None:
        """
        Aguarda o usuário pressionar Enter para continuar.
        """
        input("\n" + destaque("Pressione Enter para continuar..."))

    @staticmethod
    def cadastrar_estudante() -> Dict[str, Any]:
        """
        Gerencia o processo de cadastro de um novo estudante.
        
        Returns:
            Dict com os dados do estudante
        """
        print(cabecalho("Cadastro de Novo Estudante"))
        print(separador())
        
        # Nome do estudante
        nome = input(destaque("Nome do estudante: ")).strip()
        while not nome:
            Interface.exibir_erro("Nome não pode estar vazio!")
            nome = input(destaque("Nome do estudante: ")).strip()
        
        # Interesses
        print("\n" + destaque("Selecione os interesses do estudante:"))
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
        
        # Habilidades
        print("\n" + destaque("Selecione as habilidades do estudante:"))
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
        
        # Desempenho acadêmico
        print("\n" + destaque("Digite o desempenho acadêmico do estudante:"))
        print(separador())
        print("Digite as notas para cada disciplina (0-10)")
        print("Deixe em branco para pular uma disciplina")
        print(separador())
        
        desempenho = {}
        for disciplina in DISCIPLINAS:
            while True:
                nota = input(destaque(f"{disciplina}: ")).strip()
                if not nota:
                    break
                try:
                    nota = float(nota)
                    if 0 <= nota <= 10:
                        desempenho[disciplina] = nota
                        break
                    else:
                        print(erro("A nota deve estar entre 0 e 10!"))
                except ValueError:
                    print(erro("Digite um número válido!"))
        
        return {
            'nome': nome,
            'interesses': interesses,
            'habilidades': habilidades,
            'desempenho': desempenho
        }

    @staticmethod
    def solicitar_id_regra() -> int:
        """
        Solicita o ID da regra ao usuário.
        
        Returns:
            int: ID da regra selecionada
        """
        while True:
            try:
                regra_id = int(input("\n" + destaque("Digite o ID da regra: ")).strip())
                if regra_id > 0:
                    return regra_id
                else:
                    print(erro("ID deve ser um número positivo!"))
            except ValueError:
                print(erro("Digite um número válido!"))

    @staticmethod
    def confirmar_remocao() -> bool:
        """
        Solicita confirmação para remover um item.
        
        Returns:
            bool: True se o usuário confirmou a remoção, False caso contrário
        """
        return input("\n" + destaque("Tem certeza que deseja remover? (s/n): ")).lower() == 's'

    @staticmethod
    def editar_regra(regra: Dict) -> Dict:
        """
        Solicita dados para edição de uma regra de carreira.
        
        Args:
            regra: Dicionário com os dados atuais da regra
            
        Returns:
            Dicionário com os novos dados da regra
        """
        print(f"\n{destaque('Editar Regra de Carreira')}")
        print(f"Pressione Enter para manter o valor atual entre parênteses")
        
        # Nome da carreira
        nome_atual = regra.get('carreira', '')
        nome = input(f"\nNome da carreira ({nome_atual}): ").strip()
        if not nome:
            nome = nome_atual
        
        # Justificativa
        justificativa_atual = regra.get('justificativa', '')
        justificativa = input(f"\nJustificativa ({justificativa_atual}): ").strip()
        if not justificativa:
            justificativa = justificativa_atual
        
        # Interesses
        print("\nInteresses atuais:")
        for interesse in regra.get('interesses', []):
            print(f"- {interesse}")
        
        print("\nDigite os novos interesses (um por linha)")
        print("Pressione Enter duas vezes para manter os interesses atuais")
        interesses = []
        while True:
            interesse = input("> ").strip()
            if not interesse:
                if not interesses:  # Se não digitou nenhum interesse novo
                    interesses = regra.get('interesses', [])  # Mantém os atuais
                break
            interesses.append(interesse)
        
        # Habilidades
        print("\nHabilidades atuais:")
        for habilidade in regra.get('habilidades', []):
            print(f"- {habilidade}")
        
        print("\nDigite as novas habilidades (uma por linha)")
        print("Pressione Enter duas vezes para manter as habilidades atuais")
        habilidades = []
        while True:
            habilidade = input("> ").strip()
            if not habilidade:
                if not habilidades:  # Se não digitou nenhuma habilidade nova
                    habilidades = regra.get('habilidades', [])  # Mantém as atuais
                break
            habilidades.append(habilidade)
        
        # Desempenho
        print("\nDesempenho atual:")
        for disciplina, nota in regra.get('desempenho', {}).items():
            print(f"- {disciplina}: {nota}")
        
        print("\nDigite o novo desempenho (disciplina=nota)")
        print("Pressione Enter duas vezes para manter o desempenho atual")
        desempenho = {}
        while True:
            entrada = input("> ").strip()
            if not entrada:
                if not desempenho:  # Se não digitou nenhum desempenho novo
                    desempenho = regra.get('desempenho', {})  # Mantém o atual
                break
            
            try:
                disciplina, nota = entrada.split('=')
                disciplina = disciplina.strip()
                nota = float(nota.strip())
                if 0 <= nota <= 10:
                    desempenho[disciplina] = nota
                else:
                    print("Nota deve estar entre 0 e 10")
            except ValueError:
                print("Formato inválido. Use: disciplina=nota")
        
        return {
            'carreira': nome,
            'justificativa': justificativa,
            'interesses': interesses,
            'habilidades': habilidades,
            'desempenho': desempenho
        } 
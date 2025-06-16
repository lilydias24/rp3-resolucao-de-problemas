"""
Módulo de controle do sistema.

Contém a classe Controlador que gerencia o fluxo do sistema.
"""
import sys
import os
from typing import Dict, List, Tuple, Any
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.interface import Interface
from utils.gestor_interface import GestorInterface
from logic.motor import MotorDeInferencia
from logic.estudante import Estudante
from logic.recomendacao import cadastrar_regra, listar_regras, atualizar_regra, remover_regra
from reports.gerar_relatorios import gerar_relatorios
from reports.graficos import GeradorGraficos

class Controlador:
    """
    Classe que gerencia o fluxo do sistema.
    """
    
    def __init__(self):
        """
        Inicializa o controlador.
        """
        self.motor = MotorDeInferencia()
        
    def executar_menu_principal(self) -> None:
        """
        Executa o menu principal do sistema.
        """
        while True:
            opcao = Interface.exibir_menu_principal()
            
            if opcao == "1":
                self.cadastrar_estudante()
            elif opcao == "2":
                self.listar_estudantes()
            elif opcao == "3":
                self.buscar_estudante()
            elif opcao == "4":
                self.ver_recomendacoes()
            elif opcao == "5":
                self.executar_menu_gestor()
            elif opcao == "6":
                if Interface.confirmar_saida():
                    break
            else:
                Interface.exibir_erro("Opção inválida!")
            
            Interface.aguardar_continuar()
    
    def executar_menu_gestor(self) -> None:
        """
        Executa o menu do gestor acadêmico.
        """
        while True:
            opcao = Interface.exibir_menu_gestor()
            
            if opcao == "1":
                self.adicionar_regra()
            elif opcao == "2":
                self.editar_regra()
            elif opcao == "3":
                self.remover_regra()
            elif opcao == "4":
                self.listar_regras()
            elif opcao == "5":
                self.executar_menu_relatorios()
            elif opcao == "6":
                self.executar_menu_graficos()
            elif opcao == "7":
                break
            else:
                Interface.exibir_erro("Opção inválida!")
            
            Interface.aguardar_continuar()
    
    def executar_menu_relatorios(self) -> None:
        """
        Executa o menu de relatórios.
        """
        while True:
            opcao = Interface.exibir_menu_relatorios()
            
            if opcao == "1":
                self.gerar_relatorio_estudantes()
            elif opcao == "2":
                self.gerar_relatorio_carreiras()
            elif opcao == "3":
                break
            else:
                Interface.exibir_erro("Opção inválida!")
            
            Interface.aguardar_continuar()
    
    def executar_menu_graficos(self) -> None:
        """
        Executa o menu de gráficos.
        """
        while True:
            opcao = Interface.exibir_menu_graficos()
            
            if opcao == "1":
                self.gerar_grafico_estudantes()
            elif opcao == "2":
                self.gerar_grafico_carreiras()
            elif opcao == "3":
                break
            else:
                Interface.exibir_erro("Opção inválida!")
            
            Interface.aguardar_continuar()
    
    def cadastrar_estudante(self) -> None:
        """
        Cadastra um novo estudante.
        """
        try:
            dados = Interface.cadastrar_estudante()
            estudante = Estudante(**dados)
            self.motor.adicionar_estudante(estudante)
            Interface.exibir_sucesso("Estudante cadastrado com sucesso!")
        except Exception as e:
            Interface.exibir_erro(f"Erro ao cadastrar estudante: {str(e)}")
    
    def listar_estudantes(self) -> None:
        """
        Lista todos os estudantes cadastrados.
        """
        try:
            estudantes = self.motor.listar_estudantes()
            Interface.exibir_lista_estudantes(estudantes)
        except Exception as e:
            Interface.exibir_erro(f"Erro ao listar estudantes: {str(e)}")
    
    def buscar_estudante(self) -> None:
        """
        Busca um estudante pelo nome.
        """
        try:
            nome = Interface.solicitar_nome_estudante()
            estudante = self.motor.buscar_estudante(nome)
            if estudante:
                Interface.exibir_dados_estudante(estudante)
            else:
                Interface.exibir_aviso("Estudante não encontrado!")
        except Exception as e:
            Interface.exibir_erro(f"Erro ao buscar estudante: {str(e)}")
    
    def ver_recomendacoes(self) -> None:
        """
        Exibe as recomendações de carreira para um estudante.
        """
        try:
            nome = Interface.solicitar_nome_estudante()
            estudante = self.motor.buscar_estudante(nome)
            if estudante:
                recomendacoes = self.motor.recomendar_carreiras(estudante)
                Interface.exibir_recomendacoes(recomendacoes, nome)
            else:
                Interface.exibir_aviso("Estudante não encontrado!")
        except Exception as e:
            Interface.exibir_erro(f"Erro ao gerar recomendações: {str(e)}")
    
    def adicionar_regra(self) -> None:
        """
        Adiciona uma nova regra de carreira.
        """
        try:
            dados = GestorInterface.coletar_dados_regra()
            cadastrar_regra(dados)
            Interface.exibir_sucesso("Regra adicionada com sucesso!")
        except Exception as e:
            Interface.exibir_erro(f"Erro ao adicionar regra: {str(e)}")
    
    def editar_regra(self) -> None:
        """
        Edita uma regra de carreira existente.
        """
        try:
            regras = listar_regras()
            if not regras:
                Interface.exibir_aviso("Nenhuma regra cadastrada!")
                return
            
            print(cabecalho("Regras Cadastradas"))
            for i, regra in enumerate(regras, 1):
                print(f"\n{i}. {regra['carreira']} [ID: {regra['id']}]")
            
            try:
                idx = int(input("\n" + destaque("Digite o número da regra a editar: ")).strip())
                if 1 <= idx <= len(regras):
                    dados = GestorInterface.coletar_dados_regra()
                    atualizar_regra(regras[idx-1]['id'], dados)
                    Interface.exibir_sucesso("Regra atualizada com sucesso!")
                else:
                    Interface.exibir_erro("Número de regra inválido!")
            except ValueError:
                Interface.exibir_erro("Entrada inválida! Digite apenas números.")
        except Exception as e:
            Interface.exibir_erro(f"Erro ao editar regra: {str(e)}")
    
    def remover_regra(self) -> None:
        """
        Remove uma regra de carreira.
        """
        try:
            regras = listar_regras()
            if not regras:
                Interface.exibir_aviso("Nenhuma regra cadastrada!")
                return
            
            print(cabecalho("Regras Cadastradas"))
            for i, regra in enumerate(regras, 1):
                print(f"\n{i}. {regra['carreira']} [ID: {regra['id']}]")
            
            try:
                idx = int(input("\n" + destaque("Digite o número da regra a remover: ")).strip())
                if 1 <= idx <= len(regras):
                    remover_regra(regras[idx-1]['id'])
                    Interface.exibir_sucesso("Regra removida com sucesso!")
                else:
                    Interface.exibir_erro("Número de regra inválido!")
            except ValueError:
                Interface.exibir_erro("Entrada inválida! Digite apenas números.")
        except Exception as e:
            Interface.exibir_erro(f"Erro ao remover regra: {str(e)}")
    
    def listar_regras(self) -> None:
        """
        Lista todas as regras de carreira.
        """
        try:
            regras = listar_regras()
            Interface.exibir_lista_regras(regras)
        except Exception as e:
            Interface.exibir_erro(f"Erro ao listar regras: {str(e)}")
    
    def gerar_relatorio_estudantes(self) -> None:
        """
        Gera relatório de estudantes.
        """
        try:
            gerar_relatorios("estudantes")
            Interface.exibir_sucesso("Relatório de estudantes gerado com sucesso!")
        except Exception as e:
            Interface.exibir_erro(f"Erro ao gerar relatório: {str(e)}")
    
    def gerar_relatorio_carreiras(self) -> None:
        """
        Gera relatório de carreiras.
        """
        try:
            gerar_relatorios("carreiras")
            Interface.exibir_sucesso("Relatório de carreiras gerado com sucesso!")
        except Exception as e:
            Interface.exibir_erro(f"Erro ao gerar relatório: {str(e)}")
    
    def gerar_grafico_estudantes(self) -> None:
        """
        Gera gráfico de estudantes.
        """
        try:
            GeradorGraficos.gerar_grafico_estudantes()
            Interface.exibir_sucesso("Gráfico de estudantes gerado com sucesso!")
        except Exception as e:
            Interface.exibir_erro(f"Erro ao gerar gráfico: {str(e)}")
    
    def gerar_grafico_carreiras(self) -> None:
        """
        Gera gráfico de carreiras.
        """
        try:
            GeradorGraficos.gerar_grafico_carreiras()
            Interface.exibir_sucesso("Gráfico de carreiras gerado com sucesso!")
        except Exception as e:
            Interface.exibir_erro(f"Erro ao gerar gráfico: {str(e)}") 
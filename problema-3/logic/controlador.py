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
from data.conexao import conectar, ConexaoErro
from data.transacao import executar_consulta, executar_comando, transacao
from data.validacao import validar_estudante, validar_regra, ValidacaoErro
from models.estudante import Estudante
from logic.recomendacao import cadastrar_regra, listar_regras, editar_regra, remover_regra
from logic.recomendacao import listar_recomendacoes, gerar_recomendacoes
from reports.gerar_relatorios import gerar_relatorios
from reports.graficos import GeradorGraficos
from utils.exportador_csv import exportar_estudantes_para_csv
from utils.exportador_json import exportar_estudantes_para_json
from logic.estudante import salvar_estudante, listar_estudantes, buscar_estudante_completo_por_nome

class Controlador:
    """
    Classe que gerencia o fluxo do sistema.
    """
    
    def __init__(self):
        """
        Inicializa o controlador.
        """
        self.motor = MotorDeInferencia()
        self.gerador_graficos = GeradorGraficos()
        
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
                self.executar_menu_relatorios()
            elif opcao == "7":
                if Interface.confirmar_saida():
                    Interface.exibir_sucesso("Encerrando o sistema...")
                    break
            else:
                Interface.exibir_erro("Opção inválida! Por favor, escolha uma opção válida.")
            
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
                self.gerar_relatorios()
            elif opcao == "6":
                self.gerar_graficos()
            elif opcao == "7":
                break
            else:
                Interface.exibir_erro("Opção inválida! Por favor, escolha uma opção válida.")
            
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
                self.gerar_relatorio_estatisticas()
            elif opcao == "4":
                self.gerar_graficos()
            elif opcao == "5":
                break
            else:
                Interface.exibir_erro("Opção inválida! Por favor, escolha uma opção válida.")
            
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
            estudante_id = salvar_estudante(dados)
            Interface.exibir_sucesso(f"Estudante cadastrado com sucesso! (ID: {estudante_id})")
        except Exception as e:
            Interface.exibir_erro(f"Erro ao cadastrar estudante: {str(e)}")
    
    def listar_estudantes(self) -> None:
        """
        Lista todos os estudantes cadastrados.
        """
        try:
            estudantes = listar_estudantes()
            Interface.exibir_lista_estudantes(estudantes)
        except Exception as e:
            Interface.exibir_erro(f"Erro ao listar estudantes: {str(e)}")
    
    def buscar_estudante(self) -> None:
        """
        Busca um estudante pelo nome.
        """
        try:
            nome = Interface.solicitar_nome_estudante()
            estudante = buscar_estudante_completo_por_nome(nome)
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
            from logic.estudante import buscar_estudante_completo_por_nome
            from logic.recomendacao import gerar_recomendacoes
            nome = Interface.solicitar_nome_estudante()
            estudante = buscar_estudante_completo_por_nome(nome)
            if estudante:
                estudante_id = estudante[0]  # O ID é o primeiro elemento da tupla
                recomendacoes = gerar_recomendacoes(estudante_id)
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
            regra_id = cadastrar_regra(dados)
            Interface.exibir_sucesso(f"Regra cadastrada com sucesso! (ID: {regra_id})")
        except Exception as e:
            Interface.exibir_erro(f"Erro ao cadastrar regra: {str(e)}")
    
    def editar_regra(self) -> None:
        """
        Edita uma regra de carreira existente.
        """
        try:
            regras = listar_regras()
            if not regras:
                Interface.exibir_aviso("Nenhuma regra cadastrada!")
                return
            
            Interface.exibir_lista_regras(regras)
            regra_id = Interface.solicitar_id_regra()
            
            # Busca a regra atual
            regra_atual = None
            for regra in regras:
                if regra['id'] == regra_id:
                    regra_atual = regra
                    break
            
            if not regra_atual:
                Interface.exibir_erro(f"Regra com ID {regra_id} não encontrada!")
                return
            
            dados = GestorInterface.coletar_dados_regra(regra_atual)
            # Achatar o dicionário para o formato esperado pela função editar_regra
            if 'condicoes' in dados:
                dados_flat = {
                    'carreira': dados.get('carreira'),
                    'justificativa': dados.get('justificativa'),
                    'interesses': dados['condicoes'].get('interesses', []),
                    'habilidades': dados['condicoes'].get('habilidades', []),
                    'desempenho': dados['condicoes'].get('desempenho', {}),
                    'pesos': dados['condicoes'].get('pesos', {})
                }
            else:
                dados_flat = dados
            editar_regra(regra_id, dados_flat)
            Interface.exibir_sucesso("Regra atualizada com sucesso!")
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
            
            Interface.exibir_lista_regras(regras)
            regra_id = Interface.solicitar_id_regra()
            
            if Interface.confirmar_remocao():
                remover_regra(regra_id)
                Interface.exibir_sucesso("Regra removida com sucesso!")
        except Exception as e:
            Interface.exibir_erro(f"Erro ao remover regra: {str(e)}")
    
    def listar_regras(self) -> None:
        """
        Lista todas as regras de carreira cadastradas.
        """
        try:
            regras = listar_regras()
            Interface.exibir_lista_regras(regras)
        except Exception as e:
            Interface.exibir_erro(f"Erro ao listar regras: {str(e)}")
    
    def gerar_relatorio_estudantes(self) -> None:
        """
        Gera um relatório com todos os estudantes cadastrados.
        """
        try:
            gerar_relatorios()
            Interface.exibir_sucesso("Relatório de estudantes gerado com sucesso!")
        except Exception as e:
            Interface.exibir_erro(f"Erro ao gerar relatório: {str(e)}")
    
    def gerar_relatorio_carreiras(self) -> None:
        """
        Gera um relatório com todas as regras de carreira cadastradas.
        """
        try:
            gerar_relatorios()
            Interface.exibir_sucesso("Relatório de carreiras gerado com sucesso!")
        except Exception as e:
            Interface.exibir_erro(f"Erro ao gerar relatório: {str(e)}")
    
    def gerar_relatorio_estatisticas(self) -> None:
        """
        Gera um relatório com estatísticas do sistema.
        """
        try:
            gerar_relatorios()
            Interface.exibir_sucesso("Relatório de estatísticas gerado com sucesso!")
        except Exception as e:
            Interface.exibir_erro(f"Erro ao gerar relatório: {str(e)}")
    
    def gerar_relatorios(self) -> None:
        """Gera relatórios do sistema."""
        try:
            gerar_relatorios()
            Interface.exibir_sucesso("Relatórios gerados com sucesso!")
        except Exception as e:
            Interface.exibir_erro(f"Erro ao gerar relatórios: {str(e)}")
    
    def gerar_graficos(self) -> None:
        """Gera gráficos do sistema."""
        try:
            self.gerador_graficos.gerar_todos_graficos()
            Interface.exibir_sucesso("Gráficos gerados com sucesso!")
        except Exception as e:
            Interface.exibir_erro(f"Erro ao gerar gráficos: {str(e)}")
    
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
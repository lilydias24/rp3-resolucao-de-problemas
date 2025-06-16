"""
Sistema de recomendação de carreiras usando paradigma lógico.

Este módulo executa o fluxo principal do sistema:
- Coleta os interesses de um estudante via terminal
- Coleta o desempenho acadêmico do estudante
- Constrói os fatos lógicos a partir dos interesses e desempenho
- Salva os dados no banco SQLite
- Lista os estudantes registrados
"""
import os
from logic.controlador import Controlador
from utils.interface import Interface
from data.transacao import ConexaoErro
from utils.popular_banco import popular_banco
from utils.importar_regras import importar_regras_json_para_banco

def main():
    """
    Função principal que inicia o sistema.
    """
    try:
        # Inicializa o banco de dados
        caminho_json = os.path.join(os.path.dirname(__file__), 'utils', 'regras.json')
        try:
            importar_regras_json_para_banco(caminho_json)
        except Exception:
            pass
        try:
            popular_banco()
        except Exception:
            pass

        # Inicializa o controlador
        controlador = Controlador()
        
        while True:
            opcao = Interface.exibir_menu_principal()
            
            if opcao == "1":
                try:
                    resultado = controlador.cadastrar_novo_estudante()
                    Interface.exibir_recomendacoes(resultado)
                except ConexaoErro as e:
                    Interface.exibir_erro(f"Erro ao cadastrar estudante: {str(e)}")
            
            elif opcao == "2":
                try:
                    estudantes = controlador.listar_todos_estudantes()
                    Interface.exibir_lista_estudantes(estudantes)
                except ConexaoErro as e:
                    Interface.exibir_erro(f"Erro ao listar estudantes: {str(e)}")
            
            elif opcao == "3":
                nome = Interface.solicitar_nome_estudante()
                if not nome:
                    Interface.exibir_erro("Nome não pode estar vazio!")
                    continue
                
                try:
                    estudante = controlador.buscar_estudante(nome)
                    if estudante:
                        Interface.exibir_dados_estudante(estudante)
                    else:
                        Interface.exibir_aviso(f"Nenhum estudante encontrado com o nome '{nome}'")
                except ConexaoErro as e:
                    Interface.exibir_erro(f"Erro ao buscar estudante: {str(e)}")
            
            elif opcao == "4":
                nome = Interface.solicitar_nome_estudante()
                if not nome:
                    Interface.exibir_erro("Nome não pode estar vazio!")
                    continue
                try:
                    recomendacoes = controlador.obter_recomendacoes(nome)
                    Interface.exibir_recomendacoes(recomendacoes, nome)
                except ConexaoErro as e:
                    Interface.exibir_erro(f"Erro ao obter recomendações: {str(e)}")
            
            elif opcao == "5":
                try:
                    controlador.executar_menu_gestor()
                except Exception as e:
                    Interface.exibir_erro(f"Erro ao executar menu do gestor: {str(e)}")
            
            elif opcao == "6":
                if Interface.confirmar_saida():
                    Interface.exibir_sucesso("Encerrando o sistema...")
                    break
            
            else:
                Interface.exibir_erro("Opção inválida! Por favor, escolha uma opção válida.")
            
            Interface.aguardar_continuar()
            
    except Exception as e:
        Interface.exibir_erro(f"Erro fatal no sistema: {str(e)}")

if __name__ == "__main__":
    main()

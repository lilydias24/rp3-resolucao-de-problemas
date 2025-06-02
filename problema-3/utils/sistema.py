"""
Módulo principal do sistema de recomendação de carreiras.

Contém a classe Sistema que gerencia todas as funcionalidades do sistema, incluindo:
- Menus e interfaces
- Gerenciamento de estudantes
- Geração de relatórios
- Recomendações de carreiras
"""
import os
import json
from logic.motor import MotorDeInferencia, criar_estudante
from data.estudante_db import (
    criar_tabela_estudantes,
    salvar_estudante,
    listar_estudantes,
    obter_disciplinas,
    obter_desempenho_disciplina,
    obter_desempenho_estudante,
    obter_recomendacoes,
    excluir_estudante
)
from models.estudante import Estudante

class Sistema:
    def __init__(self):
        """Inicializa o sistema."""
        criar_tabela_estudantes()
        self.CAMINHO_REGRAS = os.path.join(os.path.dirname(__file__), '..', 'data', 'regras.json')

    def exibir_menu_principal(self):
        """Exibe o menu principal do sistema."""
        print("\n=== Sistema de Recomendação de Carreiras ===")
        print("1. Cadastrar novo estudante")
        print("2. Listar estudantes")
        print("3. Excluir estudante")
        print("4. Gerar relatórios")
        print("0. Sair")
        print("==========================================")

    def exibir_recomendacoes(self, recomendadas, proximas):
        """Exibe as recomendações de carreira de forma mais detalhada e informativa."""
        print("\nCarreiras recomendadas:")
        if recomendadas:
            for c in recomendadas:
                print(f"\n- {c['carreira']} (score: {c['score']}%)")
                print(f"  Justificativa: {c['justificativa']}")
                print("\n  Explicação:")
                for tipo, explicacao in c['explicacao'].items():
                    print(f"  - {explicacao}")
        else:
            print("\nNenhuma carreira recomendada no momento.")
            print("Para ter uma carreira recomendada, você precisa atender TODOS os critérios")
            print("(interesses, habilidades e desempenho) para pelo menos uma carreira.")
        
        print("\nCarreiras próximas:")
        if proximas:
            proximas.sort(key=lambda x: x['score'], reverse=True)
            for c in proximas:
                print(f"\n- {c['carreira']} (score: {c['score']}%)")
                print(f"  Justificativa: {c['justificativa']}")
                print("\n  Explicação:")
                for tipo, explicacao in c['explicacao'].items():
                    print(f"  - {explicacao}")
                
                print("\n  Sugestões para transformar em carreira recomendada:")
                for tipo, explicacao in c['explicacao'].items():
                    if "Faltam" in explicacao:
                        print(f"  - {explicacao.replace('Faltam', 'Adquira')}")
        else:
            print("Nenhuma carreira próxima no momento.")

    def coletar_interesses(self):
        """Solicita ao usuário que informe seu nome e interesses."""
        print("\n\t Cadastro de Interesses do Aluno : \n")
        nome = input("> Digite seu nome: ").strip()
        entrada = input("> Digite seus interesses, separados por vírgula (ex: artes, ciência, tecnologia):\n>> ")
        interesses = [i.strip().lower() for i in entrada.split(",") if i.strip()]
        return Estudante(nome=nome, interesses=interesses)

    def coletar_habilidades(self, estudante):
        """Solicita ao usuário que informe suas habilidades."""
        print("\n\t Cadastro de Habilidades : \n")
        print("Digite suas habilidades, separadas por vírgula.")
        print("Exemplos: programação, resolução de problemas, trabalho em equipe, análise de dados")
        entrada = input(">> ").strip()
        
        habilidades = [h.strip().lower() for h in entrada.split(",") if h.strip()]
        for habilidade in habilidades:
            try:
                estudante.adicionar_habilidade(habilidade)
            except (TypeError, ValueError) as e:
                print(f"Erro ao adicionar habilidade '{habilidade}': {str(e)}")
        
        print("\n\t Habilidades registradas : \n")
        for habilidade in estudante.habilidades:
            print(f"-> {habilidade}")
        
        return estudante

    def coletar_desempenho_academico(self, estudante):
        """Solicita ao usuário que informe suas notas em diferentes disciplinas."""
        print("\n\t Cadastro de Desempenho Acadêmico : \n")
        print("Digite suas notas (0-10) para cada disciplina.")
        print("Digite 'fim' para sair ou deixar uma nota em branco.")
        
        disciplinas = [
            "matematica", "portugues", "fisica", "quimica", "biologia",
            "historia", "geografia", "ingles", "programacao", "artes"
        ]
        
        desempenho = {}
        
        for disciplina in disciplinas:
            while True:
                try:
                    nota = input(f"Nota em {disciplina} : ").strip().lower()
                    if nota == 'fim':
                        break
                    
                    nota = float(nota)
                    if 0 <= nota <= 10:
                        desempenho[disciplina] = nota
                        break
                    else:
                        print("Por favor, digite uma nota entre 0 e 10.")
                except ValueError:
                    print("Por favor, digite um número válido ou 'fim'.")
            
            if nota == 'fim':
                break
        
        estudante.desempenho_escolar = desempenho
        print("\n\t Notas: \n")
        for disciplina, nota in desempenho.items():
            print(f"-> {disciplina} : {nota}")
        
        return estudante

    def listar_todos_estudantes(self):
        """Lista todos os estudantes cadastrados no sistema."""
        print("\nEstudantes cadastrados:")
        print("----------------------")
        estudantes = listar_estudantes()
        if not estudantes:
            print("Nenhum estudante cadastrado.")
            return
        
        for id_, nome, interesses, habilidades, desempenho in estudantes:
            print(f"\nNome: {nome}")
            print(f"Interesses: {', '.join(interesses)}")
            if habilidades:
                print(f"Habilidades: {', '.join(habilidades)}")
            if desempenho:
                print("Desempenho:")
                for disciplina, nota in desempenho.items():
                    print(f"  - {disciplina}: {nota}")

    def excluir_estudante_sistema(self):
        """Interface para excluir um estudante do sistema."""
        print("\nExcluir estudante")
        print("----------------")
        nome = input("Digite o nome do estudante a ser excluído: ").strip()
        
        if not nome:
            print("Nome inválido!")
            return
        
        confirmacao = input(f"\nTem certeza que deseja excluir o estudante '{nome}'? (s/n): ").lower()
        if confirmacao != 's':
            print("Operação cancelada.")
            return
        
        if excluir_estudante(nome):
            print(f"Estudante '{nome}' foi excluído com sucesso!")
        else:
            print(f"Não foi possível excluir o estudante '{nome}'.")

    def cadastrar_estudante(self):
        """Gerencia o cadastro de um novo estudante."""
        try:
            estudante = self.coletar_interesses()
            estudante = self.coletar_habilidades(estudante)
            estudante = self.coletar_desempenho_academico(estudante)
            
            salvar_estudante(estudante)
            print("\nEstudante cadastrado com sucesso!")
            
            motor = MotorDeInferencia(self.CAMINHO_REGRAS)
            recomendadas, proximas = motor.processa_estudante(estudante)
            
            self.exibir_recomendacoes(recomendadas, proximas)
            
        except Exception as e:
            print(f"\nErro ao cadastrar estudante: {str(e)}")

    def gerar_relatorios(self):
        """Gera os relatórios do sistema."""
        try:
            from reports.gerar_relatorios import gerar_relatorios
            gerar_relatorios()
        except ImportError:
            print("\nErro: Módulo de relatórios não encontrado.")
            print("Certifique-se de que o módulo reports está instalado corretamente.")

    def executar(self):
        """Executa o sistema."""
        while True:
            self.exibir_menu_principal()
            opcao = input("\nEscolha uma opção: ").strip()
            
            if opcao == "1":
                self.cadastrar_estudante()
            elif opcao == "2":
                self.listar_todos_estudantes()
            elif opcao == "3":
                self.excluir_estudante_sistema()
            elif opcao == "4":
                self.gerar_relatorios()
            elif opcao == "0":
                print("\nSaindo do sistema...")
                break
            else:
                print("\nOpção inválida!")
            
            input("\nPressione Enter para continuar...")

if __name__ == "__main__":
    sistema = Sistema()
    sistema.executar()
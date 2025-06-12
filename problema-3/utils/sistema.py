"""
Módulo do fluxo principal do sistema.

Contém funções para gerenciar o fluxo de execução do sistema.
"""
from data.criar_banco import criar_tabelas
from logic.estudante import *
from logic.recomendacao import salvar_recomendacao
from logic.motor import MotorDeInferencia
from utils.exportador_csv import exportar_tendencias_para_csv

def exibir_menu():
    """
    Exibe o menu principal do sistema.
    """
    print("\n=== Sistema de Recomendação de Carreiras ===")
    print("1. Cadastrar novo estudante")
    print("2. Listar estudantes cadastrados")
    print("3. Buscar estudante por nome")
    print("4. Ver recomendações de carreira")
    print("5. Exportar tendências de carreira para CSV")
    print("6. Sair")
    return input("\nEscolha uma opção: ").strip()

def ver_recomendacoes():
    """
    Exibe recomendações de carreira para um estudante, buscando pelo ID.
    """
    try:
        estudantes = listar_estudantes()
        exibir_estudantes(estudantes)
        estudante_id = int(input("\nDigite o ID do estudante: ").strip())
    except ValueError:
        print("ID inválido.")
        return

    # Buscar dados completos do estudante pelo ID
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT nome FROM estudantes WHERE id = ?", (estudante_id,))
    row = cursor.fetchone()
    if not row:
        print(f"\nEstudante com ID {estudante_id} não encontrado no banco.")
        conn.close()
        return
    nome = row[0]
    conn.close()

    dados_estudante = buscar_estudante_completo_por_nome(nome)
    if not dados_estudante:
        print(f"\nEstudante '{nome}' não encontrado.")
        return

    motor = MotorDeInferencia()
    recomendadas, proximas = motor.processa_estudante(dados_estudante)

    # Salve as recomendações recomendadas
    for rec in recomendadas:
        salvar_recomendacao(estudante_id, rec['carreira'], rec['score'])

    print("\n=== Recomendações de Carreira ===")
    if recomendadas:
        print("\nCarreiras recomendadas:")
        for c in recomendadas:
            print(f"- {c['carreira']} (score: {c['score']}): {c['justificativa']}")
            for k, v in c['explicacao'].items():
                print(f"  {k}: {v}")
    else:
        print("\nNenhuma carreira específica recomendada.")

    if proximas:
        print("\nCarreiras próximas (requerem desenvolvimento adicional):")
        for c in proximas:
            print(f"- {c['carreira']} (score: {c['score']}): {c['justificativa']}")
            for k, v in c['explicacao'].items():
                print(f"  {k}: {v}")

def executar_fluxo():
    """
    Executa o fluxo principal do sistema com menu interativo.
    """
    try:
        criar_tabelas()
        while True:
            opcao = exibir_menu()
            if opcao == "1":
                cadastrar_estudante() 
            elif opcao == "2":
                estudantes = listar_estudantes()
                exibir_estudantes(estudantes)
            elif opcao == "3":
                buscar_estudante()
            elif opcao == "4":
                ver_recomendacoes()
            elif opcao == "5":
                exportar_tendencias_para_csv('reports/tendencias_carreira.csv')
            elif opcao == "6":
                if input("\nTem certeza que deseja sair? (s/n): ").lower() == 's':
                    print("\nEncerrando o sistema...")
                    break
            else:
                print("\nOpção inválida! Por favor, escolha uma opção válida.")
    except Exception as e:
        print(f"\nErro no sistema: {str(e)}")
        print("O sistema será encerrado.")
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
from logic.motor import MotorDeInferencia, criar_estudante
from utils.gestor_interface import executar_menu_gestor

def exibir_menu():
    """
    Exibe o menu principal do sistema.
    """
    print("\n=== Sistema de Recomendação de Carreiras ===")
    print("1. Cadastrar novo estudante")
    print("2. Listar estudantes cadastrados")
    print("3. Buscar estudante por nome")
    print("4. Ver recomendações de carreira")
    print("5. Menu do Gestor Acadêmico")
    print("6. Sair")
    return input("\nEscolha uma opção: ").strip()

def main():
    """
    Função principal que inicia o sistema.
    """
    CAMINHO_REGRAS = os.path.join(os.path.dirname(__file__), 'data', 'regras.json')
    
    while True:
        opcao = exibir_menu()
        
        if opcao == "1":  
            estudante = criar_estudante(CAMINHO_REGRAS)
            motor = MotorDeInferencia(CAMINHO_REGRAS)
            recomendadas, proximas = motor.processa_estudante(estudante)
            
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
        
        elif opcao == "2": #mock, só deixar o menu preenchido
            print("\nFuncionalidade ainda não implementada.")
        
        elif opcao == "3":  #mock, só deixar o menu preenchido
            print("\nFuncionalidade ainda não implementada.")
        
        elif opcao == "4":  #mock, só deixar o menu preenchido
            print("\nFuncionalidade ainda não implementada.")
        
        elif opcao == "5": 
            executar_menu_gestor(CAMINHO_REGRAS)
        
        elif opcao == "6":  
            if input("\nTem certeza que deseja sair? (s/n): ").lower() == 's':
                print("\nEncerrando o sistema...")
                break
        
        else:
            print("\nOpção inválida! Por favor, escolha uma opção válida.")
        
        input("\nPressione Enter para continuar...")

if __name__ == "__main__":
    main()

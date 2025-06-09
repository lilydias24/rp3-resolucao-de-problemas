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

def exibir_recomendacoes(recomendadas, proximas):
    """
    Exibe as recomendações de carreira de forma mais detalhada e informativa.
    """
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
        # Ordena as carreiras próximas pelo score
        proximas.sort(key=lambda x: x['score'], reverse=True)
        
        for c in proximas:
            print(f"\n- {c['carreira']} (score: {c['score']}%)")
            print(f"  Justificativa: {c['justificativa']}")
            print("\n  Explicação:")
            for tipo, explicacao in c['explicacao'].items():
                print(f"  - {explicacao}")
            
            # Adiciona sugestões de melhoria
            print("\n  Sugestões para transformar em carreira recomendada:")
            for tipo, explicacao in c['explicacao'].items():
                if "Faltam" in explicacao:
                    print(f"  - {explicacao.replace('Faltam', 'Adquira')}")
    else:
        print("Nenhuma carreira próxima no momento.")

def main():
    """
    Função principal que inicia o sistema.
    """
    CAMINHO_REGRAS = os.path.join(os.path.dirname(__file__), 'data', 'regras.json')
    estudante = criar_estudante(CAMINHO_REGRAS)
    motor = MotorDeInferencia(CAMINHO_REGRAS)
    recomendadas, proximas = motor.processa_estudante(estudante)
    
    exibir_recomendacoes(recomendadas, proximas)

if __name__ == "__main__":
    main()

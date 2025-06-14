"""
Teste do sistema de recomendação de carreiras usando paradigma lógico.
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from logic.logica import pode_seguir_carreira, carreiras_proximas, CARREIRAS, regra_interesse, regra_habilidade, regra_desempenho
from logic.motor import MotorDeInferencia

def test_estudante_multiplas_carreiras():
    """
    Testa o processamento de um estudante com múltiplas carreiras recomendadas.
    """

    estudante = {
        'interesses': ['tecnologia', 'matematica', 'estatistica', 'sociologia', 'historia', 'literatura'],
        'habilidades': ['programacao', 'resolucao_problemas', 'analise_dados', 'analise', 'pesquisa', 'escrita', 'trabalho_equipe'],
        'desempenho_escolar': {
            'matematica': 10,
            'fisica': 10,
            'programacao': 5,
            'estatistica': 7,
            'historia': 2,
            'literatura': 10,
            'geografia': 3,
            'sociologia': 4
        }
    }
    
    # Processa o estudante
    motor = MotorDeInferencia()
    analise = motor.processa_estudante(estudante)
    
    # Imprime o perfil do estudante
    print("\nTestando estudante com perfil:")
    print(f"Interesses: {estudante['interesses']}")
    print(f"Habilidades: {estudante['habilidades']}")
    print(f"Desempenho: {estudante['desempenho_escolar']}")
    

    print("\nCarreiras recomendadas (atende aos requisitos mínimos com pontuação >= 0.8):")
    for carreira_info in analise['carreiras_recomendadas']:
        carreira = carreira_info['carreira']
        score = float(carreira_info['score'])
        print(f"\n- {carreira} (score: {score:.2f})")
        for tipo, explicacao in carreira_info['explicacao'].items():
            print(f"  {explicacao}")
        print("  ✓ Atende aos requisitos mínimos: pontuação total >= 0.8 e pelo menos 2 critérios com pontuação >= 0.7")
    

    print("\nCarreiras com potencial (não atende aos requisitos mínimos):")
    for carreira_info in analise['carreiras_proximas']:
        carreira = carreira_info['carreira']
        score = float(carreira_info['proximidade'])
        print(f"\n- {carreira} (score: {score:.2f})")
        for tipo, explicacao in carreira_info['explicacao'].items():
            print(f"  {explicacao}")
        print("  ⚠ Não atende aos requisitos mínimos, mas tem potencial para desenvolvimento")

if __name__ == "__main__":
    test_estudante_multiplas_carreiras() 
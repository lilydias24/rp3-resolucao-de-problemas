"""
Teste do sistema de recomendação de carreiras usando paradigma lógico.
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from logic.logica import pode_seguir_carreira, carreiras_proximas, CARRERAS, regra_interesse, regra_habilidade, regra_desempenho
from logic.motor import MotorDeInferencia

def test_estudante_multiplas_carreiras():
    """Testa um estudante que tem perfil para múltiplas carreiras."""
    estudante = {
        'interesses': ['tecnologia', 'matematica', 'estatistica', 'sociologia', 'historia', 'literatura'],
        'habilidades': ['programacao', 'resolucao_problemas', 'analise_dados', 'analise', 'pesquisa', 'escrita', 'trabalho_equipe'],
        'desempenho_escolar': {
            'matematica': 10,
            'fisica': 10,
            'programacao': 5,
            'estatistica': 7,
            'historia': 10,
            'literatura': 10,
            'geografia': 10,
            'sociologia': 10
        }
    }
    
    motor = MotorDeInferencia()
    analise = motor.processa_estudante(estudante)
    
    print("\nTestando estudante com perfil:")
    print(f"Interesses: {estudante['interesses']}")
    print(f"Habilidades: {estudante['habilidades']}")
    print(f"Desempenho: {estudante['desempenho_escolar']}\n")
    
    print("Carreiras recomendadas (atende aos requisitos mínimos):")
    for carreira, score, explicacao in analise['carreiras_recomendadas']:
        print(f"\n- {carreira} (score: {score:.2f})")
        print(f"  {explicacao['interesse']}")
        print(f"  {explicacao['habilidade']}")
        print(f"  {explicacao['desempenho']}")
        print(f"  ✓ Atende aos requisitos mínimos: pontuação total >= 0.8 e pelo menos 2 critérios com pontuação >= 0.7")
    
    print("\nCarreiras com potencial (não atende aos requisitos mínimos):")
    for carreira in analise['carreiras_proximas']:
        print(f"\n- {carreira['carreira']} (proximidade: {carreira['proximidade']:.2f})")
        print(f"  {carreira['explicacao']['interesse']}")
        print(f"  {carreira['explicacao']['habilidade']}")
        print(f"  {carreira['explicacao']['desempenho']}")
        if carreira.get('faltam_interesses'):
            print(f"  Recomendação: Desenvolva interesse em: {', '.join(carreira['interesses_faltantes'])}")
        print(f"  ✗ Não atende aos requisitos mínimos: pontuação total < 0.8 ou menos de 2 critérios com pontuação >= 0.7")

if __name__ == "__main__":
    test_estudante_multiplas_carreiras() 
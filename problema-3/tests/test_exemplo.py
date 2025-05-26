import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from logic.motor import MotorDeInferencia
from models.estudante import Estudante

def test_estudante_multiplas_carreiras():
    """
    Testa o processamento de um estudante que atende aos critérios de múltiplas carreiras.
    """
    # estudante pra teste
    estudante_exemplo = Estudante(
        interesses=["tecnologia", "matematica", "estatistica", "ciencia", "antropologia"],
        habilidades=["programação", "análise", "resolução de problemas", "historia", "literatura"],
        desempenho_escolar={
            "matematica": 9,
            "fisica": 8,
            "portugues": 7,
            "estatistica": 9,
            "geografia": 8,
            "sociologia": 10,
            "literatura": 10,
            "espanhol": 6,
            "programacao": 10,
            "historia": 10
        }
    )

    print(f"\nTestando estudante: {estudante_exemplo}")

    motor = MotorDeInferencia()
    resultado = motor.processa_estudante(estudante_exemplo)

    print("\nResultado da Análise:")
    
    if resultado["nenhuma_recomendacao"]:
        print("\nNenhuma carreira atende completamente aos seus critérios atuais.")
        
        if resultado["carreiras_proximas"]:
            print("\nCarreiras com potencial baseado em suas habilidades e desempenho:")
            for carreira in resultado["carreiras_proximas"]:
                print(f"\n- {carreira['carreira']}")
                print(f"  Proximidade: {carreira['proximidade']*100:.1f}%")
                if carreira['proximidade'] > 0.5:
                    print("  Você tem as habilidades necessárias, mas precisa desenvolver interesse na área.")
                else:
                    print("  Você precisaria desenvolver mais habilidades e interesse na área.")
        else:
            print("\nNão encontramos carreiras próximas dos seus critérios atuais.")
    else:
        print("\nCarreiras recomendadas:")
        recomendacoes_ordenadas = sorted(resultado["recomendacoes"].items(), key=lambda item: item[1], reverse=True)
        for recomendacao, pontuacao in recomendacoes_ordenadas:
            print(f"- {recomendacao}: Pontuação {pontuacao:.2f}")

if __name__ == "__main__":
    test_estudante_multiplas_carreiras() 
"""
Módulo que implementa o motor de inferência para recomendações de carreira.
"""
import json
from typing import Dict, List, Any, Tuple
from utils.gestor_interface import DISCIPLINAS, INTERESSES, HABILIDADES, selecionar_opcoes

def criar_estudante(caminho_regras: str) -> Dict[str, Any]:
    """
    Cria um estudante a partir da entrada do usuário.
    
    Args:
        caminho_regras: Caminho para o arquivo de regras
        
    Returns:
        Dicionário com os dados do estudante
    """
    print("\n=== Cadastro de Estudante ===")
    
    nome = input("\nNome do estudante: ").strip()
    while not nome:
        print("O nome não pode estar vazio!")
        nome = input("Nome do estudante: ").strip()
    
    interesses = selecionar_opcoes(INTERESSES, "Selecione seus Interesses")
    while not interesses:
        print("Você deve selecionar pelo menos um interesse!")
        interesses = selecionar_opcoes(INTERESSES, "Selecione seus Interesses")
    
    habilidades = selecionar_opcoes(HABILIDADES, "Selecione suas Habilidades")
    while not habilidades:
        print("Você deve selecionar pelo menos uma habilidade!")
        habilidades = selecionar_opcoes(HABILIDADES, "Selecione suas Habilidades")
    
    print("\nInforme suas notas nas disciplinas (0 a 10):")
    notas = {}
    for disciplina in DISCIPLINAS:
        while True:
            try:
                nota = float(input(f"Nota em {disciplina}: "))
                if 0 <= nota <= 10:
                    notas[disciplina] = nota
                    break
                else:
                    print("A nota deve estar entre 0 e 10!")
            except ValueError:
                print("Por favor, digite um número válido!")
    
    return {
        "nome": nome,
        "interesses": interesses,
        "habilidades": habilidades,
        "notas": notas
    }

class MotorDeInferencia:
    """
    Motor de inferência que processa o perfil do estudante e retorna recomendações de carreiras.
    Implementa o paradigma lógico através de fatos e regras.
    """
    
    def __init__(self, caminho_regras: str = None):
        """
        Inicializa o motor de inferência.
        
        Args:
            caminho_regras: Caminho para o arquivo JSON com as regras de carreira
        """
        self.regras = []
        if caminho_regras:
            try:
                with open(caminho_regras, 'r', encoding='utf-8') as f:
                    dados = json.load(f)
                    if isinstance(dados, dict):
                        self.regras = dados.get('carreiras', [])
                    elif isinstance(dados, list):
                        self.regras = dados
                    else:
                        print("\nAviso: Formato de regras inválido!")
            except (FileNotFoundError, json.JSONDecodeError) as e:
                print(f"\nAviso: Erro ao carregar regras: {str(e)}")
    
    def _explica_regra(self, estudante, carreira, tipo_regra, pontuacao):
        """
        Gera uma explicação sobre como uma regra foi aplicada.
        
        Args:
            estudante (dict): Perfil do estudante
            carreira (str): Nome da carreira
            tipo_regra (str): Tipo da regra (interesse, habilidade, desempenho)
            pontuacao (float): Pontuação obtida na regra
            
        Returns:
            str: Explicação da regra
        """
        if tipo_regra == 'interesse':
            interesses_carreira = carreira['condicoes']['interesses']
            interesses_estudante = set(estudante['interesses'])
            interesses_faltantes = [i for i in interesses_carreira if i not in interesses_estudante]
            return f"Regra de Interesse: Você tem {len(interesses_estudante)} dos {len(interesses_carreira)} interesses necessários. " + \
                   (f"Faltam: {', '.join(interesses_faltantes)}" if interesses_faltantes else "Todos os interesses necessários foram atendidos.")
        
        elif tipo_regra == 'habilidade':
            habilidades_carreira = carreira['condicoes']['habilidades']
            habilidades_estudante = set(estudante['habilidades'])
            habilidades_faltantes = [h for h in habilidades_carreira if h not in habilidades_estudante]
            return f"Regra de Habilidade: Você tem {len(habilidades_estudante)} das {len(habilidades_carreira)} habilidades necessárias. " + \
                   (f"Faltam: {', '.join(habilidades_faltantes)}" if habilidades_faltantes else "Todas as habilidades necessárias foram atendidas.")
        
        elif tipo_regra == 'desempenho':
            desempenho_carreira = carreira['condicoes']['desempenho']
            desempenho_estudante = estudante['notas']
            materias_faltantes = [m for m in desempenho_carreira if m not in desempenho_estudante or desempenho_estudante[m] < desempenho_carreira[m]]
            return f"Regra de Desempenho: Você tem {len(desempenho_carreira) - len(materias_faltantes)} das {len(desempenho_carreira)} notas necessárias. " + \
                   (f"Faltam notas adequadas em: {', '.join(materias_faltantes)}" if materias_faltantes else "Todas as notas necessárias foram atendidas.")
    
    def processa_estudante(self, estudante):
        """
        Processa o perfil do estudante e retorna as carreiras recomendadas e próximas.
        """
        # Converte o objeto Estudante para dicionário
        dados_estudante = estudante.to_dict() if hasattr(estudante, 'to_dict') else estudante
        
        carreiras_recomendadas = []
        carreiras_proximas = []
        
        for regra in self.regras:
            cond = regra['condicoes']
            pesos = cond.get('pesos', {})
            score = 0
            score_max = 0

            # interesses e habilidades: exige pelo menos um de cada
            interesses_ok = any(i.lower() in [ei.lower() for ei in estudante['interesses']] for i in cond.get('interesses', []))
            habilidades_ok = any(h.lower() in [eh.lower() for eh in estudante['habilidades']] for h in cond.get('habilidades', []))

            # desempenho ponderado
            desempenho_ok = True
            materias_faltantes = []
            for materia, nota_min in cond.get('desempenho', {}).items():
                peso = pesos.get(materia, 1)
                score_max += 10 * peso  # nota máxima considerada é 10
                nota_estudante = estudante['notas'].get(materia, 0)
                score += max(0, min(nota_estudante, 10)) * peso
                if nota_estudante < nota_min:
                    desempenho_ok = False
                    materias_faltantes.append(materia)

            # pra explicação
            interesses_carreira = set([i.lower() for i in cond.get('interesses', [])])
            interesses_estudante = set([i.lower() for i in estudante['interesses']])
            interesses_faltantes = list(interesses_carreira - interesses_estudante)
            interesses_atendidos = len(interesses_estudante.intersection(interesses_carreira))

            habilidades_carreira = set([h.lower() for h in cond.get('habilidades', [])])
            habilidades_estudante = set([h.lower() for h in estudante['habilidades']])
            habilidades_faltantes = list(habilidades_carreira - habilidades_estudante)
            habilidades_atendidas = len(habilidades_estudante.intersection(habilidades_carreira))

            desempenho_carreira = cond.get('desempenho', {})
            desempenho_estudante = estudante['notas']
            materias_atendidas = len([m for m in desempenho_carreira if desempenho_estudante.get(m, 0) >= desempenho_carreira[m]])

            explicacao = {
                'interesse': f"Regra de Interesse: Você tem {interesses_atendidos} dos {len(interesses_carreira)} interesses necessários. " +
                            (f"Faltam: {', '.join(interesses_faltantes)}" if interesses_faltantes else "Todos os interesses necessários foram atendidos."),
                'habilidade': f"Regra de Habilidade: Você tem {habilidades_atendidas} das {len(habilidades_carreira)} habilidades necessárias. " +
                             (f"Faltam: {', '.join(habilidades_faltantes)}" if habilidades_faltantes else "Todas as habilidades necessárias foram atendidas."),
                'desempenho': f"Regra de Desempenho: Você tem {materias_atendidas} das {len(desempenho_carreira)} notas necessárias. " +
                             (f"Faltam notas adequadas em: {', '.join(materias_faltantes)}" if materias_faltantes else "Todas as notas necessárias foram atendidas.")
            }

            # carreira recomendada
            if interesses_ok and habilidades_ok and desempenho_ok:
                carreiras_recomendadas.append({
                    'carreira': regra['carreira'],
                    'score': round(score / score_max * 100, 2) if score_max > 0 else 0,
                    'justificativa': regra.get('justificativa', ''),
                    'explicacao': explicacao
                })
            # carreira próxima: falta só um dos critérios
            else:
                faltas = sum([not interesses_ok, not habilidades_ok, not desempenho_ok])
                if faltas == 1:
                    carreiras_proximas.append({
                        "carreira": regra['carreira'],
                        "score": round(score / score_max * 100, 2) if score_max > 0 else 0,
                        "justificativa": regra.get('justificativa', ''),
                        "explicacao": explicacao
                    })
        
        carreiras_recomendadas.sort(key=lambda x: x['score'], reverse=True)
        carreiras_proximas.sort(key=lambda x: x['score'], reverse=True)
        return carreiras_recomendadas, carreiras_proximas

def carregar_regras(caminho_regras):
    with open(caminho_regras, encoding='utf-8') as f:
        return json.load(f)


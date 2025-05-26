"""
Representação dos fatos e regras do sistema de recomendação de carreiras.
Seguindo o paradigma lógico, definimos fatos e regras de forma declarativa.
"""

# fatos sobre carreiras e seus requisitos
CARRERAS = {
    'desenvolvimento_software': {
        'interesses': {
            'tecnologia': 0.4,
            'matematica': 0.3,
            'logica': 0.3
        },
        'habilidades': {
            'programacao': 0.4,
            'resolucao_problemas': 0.3,
            'trabalho_equipe': 0.3
        },
        'desempenho': {
            'matematica': 0.4,
            'fisica': 0.3,
            'programacao': 0.3
        }
    },
    'data_science': {
        'interesses': {
            'matematica': 0.4,
            'estatistica': 0.3,
            'tecnologia': 0.3
        },
        'habilidades': {
            'analise_dados': 0.4,
            'programacao': 0.3,
            'resolucao_problemas': 0.3
        },
        'desempenho': {
            'matematica': 0.4,
            'estatistica': 0.3,
            'programacao': 0.3
        }
    },
    'ciencias_humanas': {
        'interesses': {
            'historia': 0.4,
            'sociologia': 0.3,
            'literatura': 0.3
        },
        'habilidades': {
            'analise': 0.4,
            'pesquisa': 0.3,
            'escrita': 0.3
        },
        'desempenho': {
            'historia': 0.4,
            'sociologia': 0.3,
            'literatura': 0.3
        }
    }
}

# regras de inferência
def regra_interesse(estudante, carreira):
    """
    Regra: Um estudante tem interesse em uma carreira se possui os interesses necessários.
    """
    interesses_carreira = CARRERAS[carreira]['interesses']
    interesses_estudante = set(estudante['interesses'])
    
    pontuacao = sum(
        peso for interesse, peso in interesses_carreira.items()
        if interesse in interesses_estudante
    )
    
    total_pesos = sum(interesses_carreira.values())
    pontuacao_normalizada = pontuacao / total_pesos
    
    return pontuacao_normalizada >= 0.5, pontuacao_normalizada

def regra_habilidade(estudante, carreira):
    """
    Regra: Um estudante tem habilidade para uma carreira se possui as habilidades necessárias.
    """
    habilidades_carreira = CARRERAS[carreira]['habilidades']
    habilidades_estudante = set(estudante['habilidades'])
    
    pontuacao = sum(
        peso for habilidade, peso in habilidades_carreira.items()
        if habilidade in habilidades_estudante
    )
    
    total_pesos = sum(habilidades_carreira.values())
    pontuacao_normalizada = pontuacao / total_pesos
    
    return pontuacao_normalizada >= 0.5, pontuacao_normalizada

def regra_desempenho(estudante, carreira):
    """
    Regra: Um estudante tem desempenho adequado para uma carreira se possui as notas necessárias.
    """
    desempenho_carreira = CARRERAS[carreira]['desempenho']
    desempenho_estudante = estudante['desempenho_escolar']
    
    pontuacao = sum(
        peso for materia, peso in desempenho_carreira.items()
        if materia in desempenho_estudante and desempenho_estudante[materia] >= 7
    )
    
    total_pesos = sum(desempenho_carreira.values())
    pontuacao_normalizada = pontuacao / total_pesos
    
    return pontuacao_normalizada >= 0.5, pontuacao_normalizada

# func de inferência

def pode_seguir_carreira(estudante, carreira):
    """
    Inferência: Um estudante pode seguir uma carreira se atende às regras de interesse,
    habilidade e desempenho.
    """
    tem_int, pont_int = regra_interesse(estudante, carreira)
    tem_hab, pont_hab = regra_habilidade(estudante, carreira)
    tem_des, pont_des = regra_desempenho(estudante, carreira)
    
    pontuacao_total = (pont_int + pont_hab + pont_des) / 3
    criterios_altos = sum([pont_int >= 0.7, pont_hab >= 0.7, pont_des >= 0.7])
    
    return pontuacao_total >= 0.8 and criterios_altos >= 2, pontuacao_total

def carreiras_proximas(estudante):
    """
    Inferência: Retorna as carreiras que o estudante tem potencial para seguir,
    mesmo que não atenda todos os requisitos.
    """
    resultados = []
    
    for carreira in CARRERAS:
        pode_seguir, pontuacao = pode_seguir_carreira(estudante, carreira)
        if not pode_seguir:
            tem_hab, pont_hab = regra_habilidade(estudante, carreira)
            tem_des, pont_des = regra_desempenho(estudante, carreira)
            tem_int, pont_int = regra_interesse(estudante, carreira)
            
            # Calcula o que o estudante tem e o que falta
            interesses_estudante = set(estudante['interesses'])
            interesses_carreira = set(CARRERAS[carreira]['interesses'])
            interesses_faltantes = list(interesses_carreira - interesses_estudante)
            interesses_atendidos = len(interesses_estudante.intersection(interesses_carreira))
            
            habilidades_estudante = set(estudante['habilidades'])
            habilidades_carreira = set(CARRERAS[carreira]['habilidades'])
            habilidades_faltantes = list(habilidades_carreira - habilidades_estudante)
            habilidades_atendidas = len(habilidades_estudante.intersection(habilidades_carreira))
            
            desempenho_carreira = CARRERAS[carreira]['desempenho']
            desempenho_estudante = estudante['desempenho_escolar']
            materias_faltantes = [m for m in desempenho_carreira if m not in desempenho_estudante or desempenho_estudante[m] < 7]
            materias_atendidas = len([m for m in desempenho_carreira if m in desempenho_estudante and desempenho_estudante[m] >= 7])
            
            explicacao = {
                'interesse': f"Regra de Interesse: Você tem {interesses_atendidos} dos {len(interesses_carreira)} interesses necessários. " + \
                           (f"Faltam: {', '.join(interesses_faltantes)}" if interesses_faltantes else "Todos os interesses necessários foram atendidos."),
                'habilidade': f"Regra de Habilidade: Você tem {habilidades_atendidas} das {len(habilidades_carreira)} habilidades necessárias. " + \
                            (f"Faltam: {', '.join(habilidades_faltantes)}" if habilidades_faltantes else "Todas as habilidades necessárias foram atendidas."),
                'desempenho': f"Regra de Desempenho: Você tem {materias_atendidas} das {len(desempenho_carreira)} notas necessárias. " + \
                             (f"Faltam notas adequadas em: {', '.join(materias_faltantes)}" if materias_faltantes else "Todas as notas necessárias foram atendidas.")
            }
            
            if tem_hab and tem_des and not tem_int:
                resultados.append({
                    'carreira': carreira,
                    'proximidade': pontuacao,
                    'faltam_interesses': True,
                    'interesses_faltantes': interesses_faltantes,
                    'explicacao': explicacao
                })
            elif pontuacao >= 0.5:
                resultados.append({
                    'carreira': carreira,
                    'proximidade': pontuacao,
                    'explicacao': explicacao
                })
    
    return sorted(resultados, key=lambda x: x['proximidade'], reverse=True) 
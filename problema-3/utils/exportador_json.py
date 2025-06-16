"""
Módulo para exportação de dados em formato JSON.
"""
import sys
import os
import json
from typing import List, Dict, Any

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def exportar_estudantes_para_json(caminho_json: str) -> None:
    """
    Exporta a lista de estudantes para JSON.
    
    Args:
        caminho_json: Caminho do arquivo JSON de saída
    """
    from data.conexao import conectar
    from logic.estudante import listar_estudantes
    
    estudantes = listar_estudantes()
    
    # Converte os dados para um formato mais amigável
    dados = []
    for id, nome, interesses, habilidades, desempenho in estudantes:
        dados.append({
            'id': id,
            'nome': nome,
            'interesses': interesses if interesses else [],
            'habilidades': habilidades if habilidades else [],
            'desempenho': desempenho if desempenho else {}
        })
    
    # Cria o diretório se não existir
    os.makedirs(os.path.dirname(caminho_json), exist_ok=True)
    
    # Salva os dados em JSON
    with open(caminho_json, 'w', encoding='utf-8') as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)
    
    print(f"Lista de estudantes exportada para {caminho_json} com sucesso!") 
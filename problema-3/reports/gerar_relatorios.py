"""
Módulo para geração de relatórios do sistema.
"""
from typing import Dict, List, Any
import json
import os
from datetime import datetime
from data.conexao import conectar, ConexaoErro
from logic.recomendacao import listar_regras
from reports.graficos import GeradorGraficos

def gerar_relatorios() -> None:
    """
    Gera todos os relatórios do sistema.
    
    Raises:
        Exception: Se houver erro ao gerar relatórios
    """
    try:
        # Importação movida para dentro da função para evitar importação circular
        from logic.estudante import listar_estudantes
        
        # Cria diretório para relatórios
        relatorios_dir = 'reports/relatorios'
        os.makedirs(relatorios_dir, exist_ok=True)
        
        # Gera relatório de estudantes
        estudantes = listar_estudantes()
        with open(os.path.join(relatorios_dir, 'relatorio_estudantes.json'), 'w', encoding='utf-8') as f:
            json.dump(estudantes, f, ensure_ascii=False, indent=2)
            
        # Gera relatório de regras
        regras = listar_regras()
        with open(os.path.join(relatorios_dir, 'relatorio_regras.json'), 'w', encoding='utf-8') as f:
            json.dump(regras, f, ensure_ascii=False, indent=2)
            
        # Gera relatório de estatísticas
        stats = {
            'total_estudantes': len(estudantes),
            'total_regras': len(regras),
            'data_geracao': datetime.now().isoformat()
        }
        with open(os.path.join(relatorios_dir, 'relatorio_stats.json'), 'w', encoding='utf-8') as f:
            json.dump(stats, f, ensure_ascii=False, indent=2)
            
        # Gera gráficos
        gerador = GeradorGraficos()
        gerador.gerar_todos_graficos()
            
    except Exception as e:
        raise Exception(f"Erro ao gerar relatórios: {str(e)}")

if __name__ == "__main__":
    gerar_relatorios()
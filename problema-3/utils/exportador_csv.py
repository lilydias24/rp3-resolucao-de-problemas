"""
Módulo para exportação de dados em formato CSV.
"""
import sys
import os
import csv
from typing import List, Dict, Any
from datetime import datetime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from data.conexao import conectar

def criar_diretorio_relatorios() -> str:
    """
    Cria o diretório de relatórios se não existir.
    
    Returns:
        str: Caminho do diretório de relatórios
    """
    diretorio = os.path.join(os.path.dirname(os.path.dirname(__file__)), "reports", "relatorios")
    os.makedirs(diretorio, exist_ok=True)
    return diretorio

def exportar_estudantes_para_csv() -> None:
    """
    Exporta todos os estudantes para um arquivo CSV.
    """
    conn = conectar()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT e.nome, e.email, e.telefone, e.curso, e.periodo,
                       GROUP_CONCAT(i.interesse) as interesses,
                       GROUP_CONCAT(h.habilidade) as habilidades
                FROM estudantes e
                LEFT JOIN estudantes_interesses ei ON e.id = ei.estudante_id
                LEFT JOIN interesses i ON ei.interesse_id = i.id
                LEFT JOIN estudantes_habilidades eh ON e.id = eh.estudante_id
                LEFT JOIN habilidades h ON eh.habilidade_id = h.id
                GROUP BY e.id
            """)
            estudantes = cursor.fetchall()
            
            diretorio = criar_diretorio_relatorios()
            data_atual = datetime.now().strftime("%Y%m%d_%H%M%S")
            arquivo = os.path.join(diretorio, f"estudantes_{data_atual}.csv")
            
            with open(arquivo, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['Nome', 'Email', 'Telefone', 'Curso', 'Período', 'Interesses', 'Habilidades'])
                for estudante in estudantes:
                    writer.writerow(estudante)
    finally:
        conn.close()

def exportar_regras_para_csv() -> None:
    """
    Exporta todas as regras de carreira para um arquivo CSV.
    """
    conn = conectar()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT r.carreira, r.justificativa,
                       GROUP_CONCAT(DISTINCT i.interesse) as interesses,
                       GROUP_CONCAT(DISTINCT h.habilidade) as habilidades,
                       GROUP_CONCAT(DISTINCT d.disciplina || ': ' || rd.nota_min) as desempenho
                FROM regras_carreira r
                LEFT JOIN regras_interesses ri ON r.id = ri.regra_id
                LEFT JOIN interesses i ON ri.interesse_id = i.id
                LEFT JOIN regras_habilidades rh ON r.id = rh.regra_id
                LEFT JOIN habilidades h ON rh.habilidade_id = h.id
                LEFT JOIN regras_desempenho rd ON r.id = rd.regra_id
                LEFT JOIN disciplinas d ON rd.disciplina_id = d.id
                GROUP BY r.id
            """)
            regras = cursor.fetchall()
            
            diretorio = criar_diretorio_relatorios()
            data_atual = datetime.now().strftime("%Y%m%d_%H%M%S")
            arquivo = os.path.join(diretorio, f"regras_carreira_{data_atual}.csv")
            
            with open(arquivo, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['Carreira', 'Justificativa', 'Interesses', 'Habilidades', 'Desempenho'])
                for regra in regras:
                    writer.writerow(regra)
    finally:
        conn.close()

def exportar_estatisticas_para_csv() -> None:
    """
    Exporta estatísticas do sistema para um arquivo CSV.
    """
    conn = conectar()
    try:
        with conn.cursor() as cursor:
            # Estatísticas de estudantes
            cursor.execute("SELECT COUNT(*) FROM estudantes")
            total_estudantes = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(DISTINCT curso) FROM estudantes")
            total_cursos = cursor.fetchone()[0]
            
            # Estatísticas de carreiras
            cursor.execute("SELECT COUNT(*) FROM regras_carreira")
            total_carreiras = cursor.fetchone()[0]
            
            # Estatísticas de recomendações
            cursor.execute("""
                SELECT r.carreira, COUNT(*) as total_recomendacoes
                FROM regras_carreira r
                LEFT JOIN recomendacoes rec ON r.id = rec.regra_id
                GROUP BY r.id
            """)
            recomendacoes_por_carreira = cursor.fetchall()
            
            diretorio = criar_diretorio_relatorios()
            data_atual = datetime.now().strftime("%Y%m%d_%H%M%S")
            arquivo = os.path.join(diretorio, f"estatisticas_{data_atual}.csv")
            
            with open(arquivo, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['Métrica', 'Valor'])
                writer.writerow(['Total de Estudantes', total_estudantes])
                writer.writerow(['Total de Cursos', total_cursos])
                writer.writerow(['Total de Carreiras', total_carreiras])
                writer.writerow([])
                writer.writerow(['Carreira', 'Total de Recomendações'])
                for carreira, total in recomendacoes_por_carreira:
                    writer.writerow([carreira, total])
    finally:
        conn.close()

def exportar_todos_relatorios_csv() -> None:
    """
    Exporta todos os relatórios em CSV.
    """
    exportar_estudantes_para_csv()
    exportar_regras_para_csv()
    exportar_estatisticas_para_csv()

if __name__ == "__main__":
    exportar_todos_relatorios_csv()
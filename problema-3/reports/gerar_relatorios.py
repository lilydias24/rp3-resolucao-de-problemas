"""
Script para gerar relatórios visuais de desempenho acadêmico.
"""
import sys
import os
import json
from typing import List, Tuple, Any

# Adiciona o diretório raiz ao PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from reports.graficos import GeradorGraficos
from data.relatorio_db import RelatorioDB
from data.conexao import conectar
from data.transacao import ConexaoErro

def obter_estudantes_silencioso() -> List[Tuple[Any, ...]]:
    """
    Obtém a lista de estudantes sem imprimir dados de debug.
    
    Returns:
        Lista de tuplas contendo dados dos estudantes
        
    Raises:
        ConexaoErro: Se houver erro ao acessar o banco de dados
    """
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT id, nome, interesses, habilidades, desempenho_escolar FROM estudantes")
        estudantes = []
        
        for row in cursor.fetchall():
            id_, nome, interesses_raw, habilidades_raw, desempenho_raw = row
            
            # Converte os dados JSON
            interesses = json.loads(interesses_raw) if interesses_raw else []
            habilidades = json.loads(habilidades_raw) if habilidades_raw else []
            desempenho = json.loads(desempenho_raw) if desempenho_raw else {}
            
            estudantes.append((id_, nome, interesses, habilidades, desempenho))
        
        return estudantes
    except Exception as e:
        raise ConexaoErro(f"Erro ao obter estudantes: {str(e)}")

def gerar_relatorios() -> None:
    """
    Gera relatórios visuais de desempenho acadêmico.
    
    Raises:
        Exception: Se houver erro ao gerar os relatórios
    """
    try:
        print("\nIniciando geração de relatórios...")
        
        # Inicializa o gerador de gráficos
        gerador = GeradorGraficos()
        
        # Inicializa o gerador de relatórios
        db = RelatorioDB()
        
        # Obtém todos os dados de uma vez
        estudantes = obter_estudantes_silencioso()
        estudantes_com_dados = [(id_, nome, interesses, habilidades, desempenho) 
                               for id_, nome, interesses, habilidades, desempenho in estudantes 
                               if desempenho]  # Filtra apenas estudantes com dados de desempenho
        
        if not estudantes_com_dados:
            print("Nenhum estudante com dados de desempenho encontrado.")
            return
        
        print(f"Processando {len(estudantes_com_dados)} estudantes com dados...")
        
        # Obtém dados de desempenho por disciplina
        disciplinas = db.obter_disciplinas()
        print(f"\nGerando gráficos para {len(disciplinas)} disciplinas...")
        for disciplina in disciplinas:
            dados_disciplina = db.obter_desempenho_disciplina(disciplina)
            if dados_disciplina:
                gerador.grafico_desempenho_disciplina(dados_disciplina, disciplina)
        
        # Obtém dados de desempenho por estudante
        print("\nGerando gráficos por estudante...")
        for _, nome, _, _, desempenho in estudantes_com_dados:
            dados_estudante = db.obter_desempenho_estudante(nome)
            if dados_estudante:
                gerador.grafico_desempenho_estudante(dados_estudante, nome)
        
        # Gera gráfico de distribuição de recomendações
        print("\nGerando gráfico de recomendações...")
        dados_recomendacoes = db.obter_recomendacoes()
        if dados_recomendacoes:
            gerador.grafico_recomendacoes(dados_recomendacoes)
        
        print("\nRelatórios gerados com sucesso!")
        print(f"Os gráficos estão disponíveis em: {os.path.abspath('reports/graficos')}")
        
    except Exception as e:
        print(f"\nErro ao gerar relatórios: {str(e)}")
        raise

if __name__ == "__main__":
    gerar_relatorios()
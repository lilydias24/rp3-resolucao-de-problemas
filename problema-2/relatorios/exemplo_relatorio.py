from datetime import datetime, timedelta
from relatorios import gerar_relatorio, FILTROS_PADRAO

def exemplo_uso_relatorios():
    # exemplo de usuario qualquer so pra fins de teste
    usuario = {
        'id': '123',
        'nome': 'João Silva'
    }
    
    # ex 1: relatorio simples dos ultimos 30 dias (ou todos os dados disponiveis)
    # usando datas que cobrem os exemplos de dados
    data_inicio = "01-08-2023"
    data_fim = "10-08-2023"
    
    print("Gerando relatório de batimentos cardíacos...")
    caminho_relatorio = gerar_relatorio(
        usuario=usuario,
        tipo_dado='batimentos',
        periodo=(data_inicio, data_fim)
    )
    print(f"Relatório gerado em: {caminho_relatorio}")
    
    # ex 2: relatorio de pressao alta em csv
    print("Gerando relatório de pressão alta...")
    caminho_relatorio = gerar_relatorio(
        usuario=usuario,
        tipo_dado='pressao',
        filtros=[FILTROS_PADRAO['pressao_alta']],
        periodo=(data_inicio, data_fim)
    )
    print(f"Relatório de pressão alta gerado em: {caminho_relatorio}")
    
    # ex 3: relatorio de glicose com valor elevado
    print("Gerando relatório de glicose alta...")
    caminho_relatorio = gerar_relatorio(
        usuario=usuario,
        tipo_dado='glicose',
        filtros=[FILTROS_PADRAO['glicose_alta']],  
        periodo=(data_inicio, data_fim)
    )
    print(f"Relatório de glicose gerado em: {caminho_relatorio}")

if __name__ == '__main__':
    exemplo_uso_relatorios() 
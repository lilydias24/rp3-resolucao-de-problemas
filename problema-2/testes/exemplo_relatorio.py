from datetime import datetime
from relatorios import gerar_relatorio, FILTROS_PADRAO
import os


def exemplo_uso_relatorios():
    # usuário de exemplo
    usuario = {"id": "123", "nome": "João Silva"}

    # usando as datas no formato brasileiro (DD/MM/AAAA)
    # os dados do csv estão com a data 05/05/2025
    data_inicio = "01/05/2025"
    data_fim = "10/05/2025"

    print("\n=== Relatórios dos dados de saúde (Formato brasileiro de datas) ===\n")

    print("1. Relatório completo de batimentos cardíacos:")
    caminho_relatorio = gerar_relatorio(
        usuario=usuario, tipo_dado="batimentos", periodo=(data_inicio, data_fim)
    )
    print(f"Relatório gerado em: {caminho_relatorio}")

    print("\n2. Relatório de batimentos cardíacos altos:")
    caminho_relatorio = gerar_relatorio(
        usuario=usuario,
        tipo_dado="batimentos",
        filtros=[FILTROS_PADRAO["batimentos_alto"]],
        periodo=(data_inicio, data_fim),
    )
    print(f"Relatório gerado em: {caminho_relatorio}")

    print("\n3. Relatório completo de pressão arterial:")
    caminho_relatorio = gerar_relatorio(
        usuario=usuario, tipo_dado="pressao", periodo=(data_inicio, data_fim)
    )
    print(f"Relatório gerado em: {caminho_relatorio}")

    print("\n4. Relatório de pressão arterial alta:")
    caminho_relatorio = gerar_relatorio(
        usuario=usuario,
        tipo_dado="pressao",
        filtros=[FILTROS_PADRAO["pressao_alta"]],
        periodo=(data_inicio, data_fim),
    )
    print(f"Relatório gerado em: {caminho_relatorio}")

    print("\n5. Relatório completo de glicose:")
    caminho_relatorio = gerar_relatorio(
        usuario=usuario, tipo_dado="glicose", periodo=(data_inicio, data_fim)
    )
    print(f"Relatório gerado em: {caminho_relatorio}")

    print("\n6. Relatório de glicose baixa:")
    caminho_relatorio = gerar_relatorio(
        usuario=usuario,
        tipo_dado="glicose",
        filtros=[FILTROS_PADRAO["glicose_baixa"]],
        periodo=(data_inicio, data_fim),
    )
    print(f"Relatório gerado em: {caminho_relatorio}")


if __name__ == "__main__":
    exemplo_uso_relatorios()

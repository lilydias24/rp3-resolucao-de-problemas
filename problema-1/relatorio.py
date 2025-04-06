import csv
import os
from estoque import transportar_dados
from datetime import datetime

def gerar_relatorio():
    """Gera um relatório das movimentações de entrada e saída no formato CSV."""

    dir = os.path.dirname(os.path.abspath(__file__))  
    add_csv = os.path.join(dir, "relatorio_movimentacoes.csv")

    dados1 = transportar_dados('estoque.json')
    produtos = dados1.get('produtos', {})
    dados2 = transportar_dados('movimentacoes.json')
    movimentacoes = dados2.get('movimentacoes', [])

    if not movimentacoes:
        print(f'\n <<<--- Nenhuma movimentação registrada no sistema. --->>>')
        return

    # Ordenar por data (opcional)
    movimentacoes.sort(key=lambda x: x.get('data', ''))

    with open(add_csv, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        # Cabeçalhos
        writer.writerow([
            'ID Movimento',
            'Tipo de Movimento',
            'ID Produto',
            'Nome do Produto',
            'Quantidade',
            'Data da Movimentação',
            'ID Pessoa',
            'Tipo de Pessoa'
        ])

        for mov in movimentacoes:
            id_produto = str(mov.get('id_produto', ''))
            nome_produto = produtos.get(id_produto, {}).get('nome', 'Desconhecido')

            
            try:
                data_mov = datetime.strptime(mov.get('data', ''), '%Y-%m-%d')
                data_formatada = data_mov.strftime('%d/%m/%Y')
            except:
                data_formatada = mov.get('data', '')

            writer.writerow([
                mov.get('id_movimento', ''),
                mov.get('tipo_movimento', '').capitalize(),
                id_produto,
                nome_produto,
                mov.get('quantidade', ''),
                data_formatada,
                mov.get('id_pessoa', ''),
                mov.get('tipo_pessoa', '').capitalize()
            ])

    print(f'\n <<<--- Relatório gerado com sucesso = relatorio_movimentacoes.csv --->>>')

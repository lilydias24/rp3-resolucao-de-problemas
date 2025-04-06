import pessoas
import produtos
import movimentacoes
import estoque
import relatorio

def main():
    while True:
        print('\n\t <<<--- Sistema de Controle de Estoque --->>>')
        print('\n\t 1. Gerenciar Pessoas')
        print('\t 2. Gerenciar Produtos')
        print('\t 3. Gerenciar Movimentações')
        print('\t 4. Verificar o Estoque Atual')
        print('\t 5. Gerar Relatório de Movimentações')
        print('\t 6. Sair')
        print('\n\t <<<-------------------------------------->>>')

        opcao = input('\n > Selecione uma das opções acima: ')

        if opcao == '1':
            pessoas.main()
        elif opcao == '2':
            produtos.main()
        elif opcao == '3':
            movimentacoes.main()
        elif opcao == '4':
            estoque.listar_estoque()
        elif opcao == '5':
            relatorio.gerar_relatorio()
        elif opcao == '6':
            print('\n <<<--- Encerrando o sistema. Até mais! --->>>\n')
            break
        else:
            print('\n <<<--- Opção inválida. Tente novamente. --->>>\n')

if __name__ == '__main__':
    main()

import pydoc
from src import pessoas, produtos, movimentacoes, estoque, relatorio
<<<<<<< HEAD
from estilo import print_terminal
=======
pydoc.writedoc("main")
>>>>>>> bb34a614cd59ada5f53f0daf9f1fd5973152f4ff

def main():
    while True:
        print_terminal('_._' * 25, cor='ciano', estilo='negrito')
        print_terminal('\n | \t\t<<<--- Sistema de Controle de Estoque --->>> \t\t |', cor='ciano', estilo='negrito')
        print_terminal('_._' * 25, cor='ciano', estilo='negrito')
        
        print_terminal('\n\n\t\t 1. 🧑  Gerenciar Pessoas', cor='roxo', estilo='negrito')
        print_terminal('\n\t\t 2. 📦  Gerenciar Produtos', cor='roxo', estilo='negrito')
        print_terminal('\n\t\t 3. 🔄  Gerenciar Movimentações', cor='roxo', estilo='negrito')
        print_terminal('\n\t\t 4. 📊  Verificar o Estoque Atual', cor='roxo', estilo='negrito')
        print_terminal('\n\t\t 5. 🧾  Gerar Relatório de Movimentações', cor='roxo', estilo='negrito')
        print_terminal('\n\t\t 6. ⚙️   Sair \n', cor='roxo', estilo='negrito')
        print_terminal('_._' * 25, cor='ciano', estilo='negrito')

        opcao = input('\n\t\033[1;32m >>> Selecione uma das opções acima: \033[0m').strip()
        print_terminal('_._' * 25, cor='ciano', estilo='negrito')

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
            print_terminal('\n\t <<<--- Encerrando o sistema. Até mais! --->>>\n', cor='amarelo', estilo='sublinhado')
            return
        else:
           print_terminal('\n\t <<<--- Opção inválida! --->>>\n', cor='vermelho', estilo='normal')
           break
    
if __name__ == '__main__':
    main()

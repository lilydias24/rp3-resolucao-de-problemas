import json
from datetime import datetime

# carregar de novo estoque que na teoria nem existe
def carregar_estoque():
    try:
       with open('C:/REP3/grupo-05/problema-1/estoque.json', 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

# salva ele 
def salvar_estoque(estoque):
    with open('estoque.json', 'w') as file:
        json.dump(estoque, file, indent=4)

# registra a saida de um negocio que nao existe ainda
def registrar_saida(id_produto, quantidade):
    if quantidade <= 0:
        print("Quantidade inválida. Insira um valor positivo.")
        return

    estoque = carregar_estoque()

    if id_produto in estoque:
        produto = estoque[id_produto]
        produto['entradas'] = produto.get('entradas', [])
        total_em_estoque = sum(entrada['quantidade'] for entrada in produto['entradas'])

        if total_em_estoque >= quantidade:
            produto['saidas'] = produto.get('saidas', [])

            saida = {
                'quantidade': quantidade,
                'data': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }

            produto['saidas'].append(saida)

            # remove a quantidade pedida
            quantidade_restante = quantidade
            for entrada in produto['entradas']:
                if entrada['quantidade'] <= quantidade_restante:
                    quantidade_restante -= entrada['quantidade']
                    entrada['quantidade'] = 0
                else:
                    entrada['quantidade'] -= quantidade_restante
                    break

            salvar_estoque(estoque)
            print(f"Saída registrada em {saida['data']}: {quantidade} unidades do produto {id_produto}.")
        else:
            print(f"Estoque insuficiente para remover {quantidade} unidades do produto {id_produto}.")
    else:
        print(f"Produto com ID {id_produto} não encontrado no estoque.")

        

# chamando pra testar
if __name__ == "__main__":
    registrar_saida('1', 4)


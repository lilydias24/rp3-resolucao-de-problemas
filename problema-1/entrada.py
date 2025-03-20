import json
from datetime import datetime

#carregar estoque que na teoria nem existe 
def carregar_estoque():
    with open('grupo-05/problema-1/estoque.json', 'r') as file:
        return json.load(file)

#registrar a entrada do produto
def registrar_entrada(id_produto, quantidade):
    estoque = carregar_estoque()
    
    # if pra ver se o produto existe mesmo 
    if id_produto in estoque:

        

        produto = estoque[id_produto]
        produto['entradas'] = produto.get('entradas', [])
        
        # entrada nova com timestap
        entrada = {
            'quantidade': quantidade,
            'data': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        produto['entradas'].append(entrada)
        
        # abre o estoque 
        with open('estoque.json', 'w') as file:
            json.dump(estoque, file, indent=4)
        
        print(f"entrada registrada em {entrada['data']}: {quantidade} unidades do produto {id_produto}.")
    else:
        print(f"produto com ID {id_produto} não encontrado no estoque.")

# teste pra ver se ta chamando memo
if __name__ == "__main__":
    registrar_entrada('1', 10)  


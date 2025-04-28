import csv
import os

# aumento do tamanho de leitura do csv, para evitar o erro de falta de memória
csv.field_size_limit(1_400_000)

dir_base = os.path.dirname(os.path.abspath(__file__))

path = "dataset_saude.csv"


def load(path):
    '''
    a função load() verifica o arquivo csv e o retorna se encontrá-lo,
    se o arquivo csv não for encontrado retorna um except,
    se ao abrir o arquivo ocorrer erro de excesso de memória, ocorre outro except
    '''
    path_csv = os.path.join(dir_base, path)

    try:
        with open(path_csv, "r", newline="", encoding="utf-8") as file:
            leitor = csv.DictReader(file, delimiter=",")
            return list(leitor)

    except FileNotFoundError:
        return "documento não encontrado, reveja a referencia do documento"

    except csv.Error:
        return "não foi possivel carregar o documento, tente lazy iteration"


def listar(path):
    '''
    a função listar(), exibe os itens do arquivo csv com excessão da tag "observações"
    '''
    with open(path, "r", newline="", encoding="utf-8") as file:
        leitor = csv.reader(file)
        '''
         o next(leitor) fornece o cabeçalho do arquivo csv,
         ao usar enumerate(next(leitor)) associo um indice ao 
         valor do cabeçalho
        '''
        dados = {tag: valor for valor, tag in enumerate(next(leitor))}

        '''
        a função lambda retorna os valores da dict comprehension com f-strings
        para melhorar a legibilidade da saida do código
        '''
        formatacao = lambda linhas: (
            f"data = {linhas[dados["Data"]]}",
            f"hora = {linhas[dados["Hora"]]}",
            f"batimentos = {linhas[dados["Batimentos Cardíacos"]]}",
            f"pressao = {linhas[dados["Pressão Arterial"]]}",
            f"glicose = {linhas[dados["Glicose"]]}"
        )
        '''
        a primeira função map() aplica a função lambda formatação nos iteráveis da variavel leitor,
        a segunda função map() usa a função print e o retorno do primeiro map() como iterável,
        a função list() serve para retornar um valor legível, pois a função map por padrão
        retorna um generator object
        '''
        list(map(print, map(formatacao, leitor)))

def adiciona_dados(valor_batimentos=0, valor_pressao=0, valor_glicose=0, obs=""):
    with open("dados_pacientes.csv", "a", newline="", encoding="utf-8") as file:
        fieldnames = {"Data", "Hora", "Batimentos", "Pressao", "Glicose", "obs"}
        caneta = csv.DictWriter(file, delimiter=",", fieldnames=fieldnames)
        caneta.writeheader()
        caneta.writerow(
            {
                "Data": 28, "Hora": 12, "Batimentos": valor_batimentos, "Pressao": valor_pressao,
                "Glicose": valor_glicose, "obs": obs
            }
        )

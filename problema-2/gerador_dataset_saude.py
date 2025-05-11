<<<<<<< HEAD
"""Gerador conjuntos de dados médicos sintéticos (batimentos cardíacos, pressão arterial, glicose) no formato CSV.

Como usar:

python3 -B gerador_dataset_saude.py --linhas 10000 --caracteres 900000 --nome-arquivo dataset_saude.csv
"""

# Importando dependências
from csv import writer
from random import randint, choice
from string import ascii_letters as letras_ascii, digits as digitos
from datetime import datetime, timedelta
from argparse import ArgumentParser
from logging import basicConfig, getLogger, INFO


def gerar_dataset_csv(logger: object, numero_linhas: int = 1_000, caracteres_descricao: int = 900_000, nome_arquivo: str = "dataset.csv"):
    """
    Gera um dataset em formato CSV com dados de saúde e uma coluna de observações.

    Cada registro contém:
      - Data: data no formato YYYY-MM-DD.
      - Hora: hora no formato HH:MM:SS.
      - Batimentos Cardíacos: valor inteiro aleatório entre 50 e 120.
      - Pressão Arterial: string formatada como "sistólica/diastólica", onde sistólica varia de 90 a 180 e diastólica de 60 a 120.
      - Glicose: valor inteiro aleatório entre 70 e 140 (em mg/dL).
      - Observações: string aleatória com um número de caracteres definido por 'caracteres_descricao',
        para aumentar o tamanho do arquivo.

    As datas e horas dos registros serão sempre crescentes.

    Args:
        logger (object): Objeto de log para exibir mensagens sobre o funcionamento do script.
        numero_linhas (int): Número de registros (linhas) a serem gerados.
        caracteres_descricao (int, optional): Quantidade de caracteres para a coluna "Observações". Defaults to 900_000.
        nome_arquivo (str, optional): Nome do arquivo CSV a ser criado. Defaults to "dataset_saude.csv".
    """
    # Definindo um ponto inicial para data e hora
    timestamp_atual = datetime(2025, 1, 1, 0, 0, 0)

    with open(nome_arquivo, mode="w", newline="", encoding="utf-8") as file:
        # Definindo o escritor CSV
        csv_writer = writer(file)

        # Escrevendo o cabeçalho do CSV
        csv_writer.writerow(["Data", "Hora", "Batimentos Cardíacos", "Pressão Arterial", "Glicose", "Observações"])

        # Exibindo os campos do cabeçalho criados
        logger.info(f"Criando Cabeçalho CSV. Campos: Data, Hora, Batimentos Cardíacos, Pressão Arterial, Glicose, Observações")

        # Criando as linhas do CSV com as observações médicas
        for cont_linhas in range(numero_linhas):
            # Definindo os campos de data e hora (incremento de no mínimo 24h entre os registros)
            incremento_segundos = randint(86400, 90000)
            timestamp_atual += timedelta(seconds=incremento_segundos)
            data_str = timestamp_atual.strftime("%Y-%m-%d")
            hora_str = timestamp_atual.strftime("%H:%M:%S")

            # Gerando registro de batimentos cardíacos
            batimentos = randint(50, 120)

            # Gerando registro de pressão arterial (sistólica/diastólica)
            pressao = f"{randint(90, 180)}/{randint(60, 120)}"

            # Gerando registro de glicose
            glicose = randint(70, 140)

            # Gerando observações (texto que simula uma anotação do paciente sobre o momento do registro)
            observacoes = "".join(choice(letras_ascii + digitos + " ") for _ in range(caracteres_descricao))

            # Consolidando os dados da linha
            dados_linha = [data_str, hora_str, batimentos, pressao, glicose, observacoes]

            # Exibindo os valores gerados (omitindo a coluna de observações para não poluir o log)
            logger.info(f"[Linha {cont_linhas}] {dados_linha[:-1]}")

            # Escrevendo a linha no CSV com os dados gerados
            csv_writer.writerow(dados_linha)


if __name__ == "__main__":
    # Definindo um objeto de log para exibir mensagens sobre o funcionamento do script
    basicConfig(level=INFO, format="%(asctime)s [%(levelname)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
    logger = getLogger("gerador_dataset_saude")

    # Definindo argumentos para o script
    gerenciador_args = ArgumentParser()
    gerenciador_args.add_argument("--linhas", "-l", help="Número de linhas para serem geradas no CSV", default="10000", required=False)
    gerenciador_args.add_argument("--caracteres", "-c", help="Número de caracteres da descrição", default="900000", required=False)
    gerenciador_args.add_argument("--nome-arquivo", "-n", help="Nome do arquivo de saída", default="dataset_saude.csv", required=False)
    args = gerenciador_args.parse_args()

    # Exibindo os argumentos recebidos
    logger.info(f"[Argumentos Recebidos] linhas={args.linhas}. caracteres={args.caracteres}. nome_arquivo={args.nome_arquivo}")

    # Chamando função principal
    gerar_dataset_csv(
        logger=logger,
        numero_linhas=int(args.linhas),
        caracteres_descricao=int(args.caracteres),
        nome_arquivo=args.nome_arquivo,
    )
=======
"""Gerador conjuntos de dados médicos sintéticos (batimentos cardíacos, pressão arterial, glicose) no formato CSV.

Como usar:

python3 -B gerador_dataset_saude.py --linhas 10000 --caracteres 900000 --nome-arquivo dataset_saude.csv
"""

# Importando dependências
from csv import writer
from random import randint, choice
from string import ascii_letters as letras_ascii, digits as digitos
from datetime import datetime, timedelta
from argparse import ArgumentParser
from logging import basicConfig, getLogger, INFO


def gerar_dataset_csv(logger: object, numero_linhas: int = 1_000, caracteres_descricao: int = 900_000, nome_arquivo: str = "dataset.csv"):
    """
    Gera um dataset em formato CSV com dados de saúde e uma coluna de observações.

    Cada registro contém:
      - Data: data no formato YYYY-MM-DD.
      - Hora: hora no formato HH:MM:SS.
      - Batimentos Cardíacos: valor inteiro aleatório entre 50 e 120.
      - Pressão Arterial: string formatada como "sistólica/diastólica", onde sistólica varia de 90 a 180 e diastólica de 60 a 120.
      - Glicose: valor inteiro aleatório entre 70 e 140 (em mg/dL).
      - Observações: string aleatória com um número de caracteres definido por 'caracteres_descricao',
        para aumentar o tamanho do arquivo.

    As datas e horas dos registros serão sempre crescentes.

    Args:
        logger (object): Objeto de log para exibir mensagens sobre o funcionamento do script.
        numero_linhas (int): Número de registros (linhas) a serem gerados.
        caracteres_descricao (int, optional): Quantidade de caracteres para a coluna "Observações". Defaults to 900_000.
        nome_arquivo (str, optional): Nome do arquivo CSV a ser criado. Defaults to "dataset_saude.csv".
    """
    # Definindo um ponto inicial para data e hora
    timestamp_atual = datetime(2025, 1, 1, 0, 0, 0)

    with open(nome_arquivo, mode="w", newline="", encoding="utf-8") as file:
        # Definindo o escritor CSV
        csv_writer = writer(file)

        # Escrevendo o cabeçalho do CSV
        csv_writer.writerow(["Data", "Hora", "Batimentos Cardíacos", "Pressão Arterial", "Glicose", "Observações"])

        # Exibindo os campos do cabeçalho criados
        logger.info(f"Criando Cabeçalho CSV. Campos: Data, Hora, Batimentos Cardíacos, Pressão Arterial, Glicose, Observações")

        # Criando as linhas do CSV com as observações médicas
        for cont_linhas in range(numero_linhas):
            # Definindo os campos de data e hora (incremento de no mínimo 24h entre os registros)
            incremento_segundos = randint(86400, 90000)
            timestamp_atual += timedelta(seconds=incremento_segundos)
            data_str = timestamp_atual.strftime("%Y-%m-%d")
            hora_str = timestamp_atual.strftime("%H:%M:%S")

            # Gerando registro de batimentos cardíacos
            batimentos = randint(50, 120)

            # Gerando registro de pressão arterial (sistólica/diastólica)
            pressao = f"{randint(90, 180)}/{randint(60, 120)}"

            # Gerando registro de glicose
            glicose = randint(70, 140)

            # Gerando observações (texto que simula uma anotação do paciente sobre o momento do registro)
            observacoes = "".join(choice(letras_ascii + digitos + " ") for _ in range(caracteres_descricao))

            # Consolidando os dados da linha
            dados_linha = [data_str, hora_str, batimentos, pressao, glicose, observacoes]

            # Exibindo os valores gerados (omitindo a coluna de observações para não poluir o log)
            logger.info(f"[Linha {cont_linhas}] {dados_linha[:-1]}")

            # Escrevendo a linha no CSV com os dados gerados
            csv_writer.writerow(dados_linha)


if __name__ == "__main__":
    # Definindo um objeto de log para exibir mensagens sobre o funcionamento do script
    basicConfig(level=INFO, format="%(asctime)s [%(levelname)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
    logger = getLogger("gerador_dataset_saude")

    # Definindo argumentos para o script
    gerenciador_args = ArgumentParser()
    gerenciador_args.add_argument("--linhas", "-l", help="Número de linhas para serem geradas no CSV", default="10000", required=False)
    gerenciador_args.add_argument("--caracteres", "-c", help="Número de caracteres da descrição", default="900000", required=False)
    gerenciador_args.add_argument("--nome-arquivo", "-n", help="Nome do arquivo de saída", default="dataset_saude.csv", required=False)
    args = gerenciador_args.parse_args()

    # Exibindo os argumentos recebidos
    logger.info(f"[Argumentos Recebidos] linhas={args.linhas}. caracteres={args.caracteres}. nome_arquivo={args.nome_arquivo}")

    # Chamando função principal
    gerar_dataset_csv(
        logger=logger,
        numero_linhas=int(args.linhas),
        caracteres_descricao=int(args.caracteres),
        nome_arquivo=args.nome_arquivo,
    )
>>>>>>> bb34a614cd59ada5f53f0daf9f1fd5973152f4ff

def print_terminal(mensagem, cor="branco", estilo="normal"):
    cores = {
        "preto": 30,
        "vermelho": 31,
        "verde": 32,
        "amarelo": 33,
        "azul": 34,
        "roxo": 35,
        "ciano": 36,
        "branco": 37
    }

    estilos = {
        "normal": 0,
        "negrito": 1,
        "sublinhado": 4
    }

    cor_codigo = cores.get(cor.lower(), 37)  # branco como padrão
    estilo_codigo = estilos.get(estilo.lower(), 0)

    print(f"\033[{estilo_codigo};{cor_codigo}m{mensagem}\033[0m")

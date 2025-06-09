"""
Interface para o Gestor Acadêmico gerenciar as regras de carreiras.
"""
import os
from typing import Dict, Any, List
from .gestor import GestorRegras


DISCIPLINAS = [
    "Matemática",
    "Física",
    "Química",
    "Biologia",
    "Português",
    "História",
    "Geografia",
    "Artes",
    "Inglês",
    "Literatura",
    "Sociologia",
    "Filosofia"
]

INTERESSES = [
    "Tecnologia",
    "Ciências",
    "Saúde",
    "Humanas",
    "Arte",
    "Comunicação",
    "Negócios",
    "Construção",
    "Comportamento humano",
    "Justiça",
    "Gestão",
    "Comunicação visual",
    "Ajuda ao próximo"
]

HABILIDADES = [
    "Programação",
    "Lógica",
    "Redação",
    "Comunicação",
    "Atenção aos detalhes",
    "Empatia",
    "Argumentação",
    "Leitura",
    "Raciocínio lógico",
    "Desenho técnico",
    "Criatividade",
    "Edição de imagens",
    "Liderança",
    "Organização",
    "Escuta ativa"
]

CARREIRAS = [
    "Engenharia de Software",
    "Ciência da Computação",
    "Engenharia Civil",
    "Medicina",
    "Direito",
    "Psicologia",
    "Administração",
    "Design Gráfico",
    "Jornalismo",
    "Arquitetura",
    "Ciência de Dados",
    "Engenharia Elétrica",
    "Engenharia Mecânica",
    "Fisioterapia",
    "Nutrição"
]

def exibir_menu_gestor() -> str:
    """
    Exibe o menu do gestor acadêmico.
    
    Returns:
        Opção escolhida pelo usuário
    """
    print("\n=== Menu do Gestor Acadêmico ===")
    print("1. Listar todas as regras")
    print("2. Adicionar nova regra")
    print("3. Editar regra existente")
    print("4. Remover regra")
    print("5. Visualizar regra específica")
    print("6. Voltar ao menu principal")
    return input("\nEscolha uma opção: ").strip()

def selecionar_opcoes(lista_opcoes: List[str], titulo: str) -> List[str]:
    """
    Permite selecionar múltiplas opções de uma lista.
    
    Args:
        lista_opcoes: Lista de opções disponíveis
        titulo: Título da seleção
        
    Returns:
        Lista de opções selecionadas
    """
    selecionados = []
    print(f"\n=== {titulo} ===")
    
    while True:
        print("\nOpções disponíveis:")
        for i, opcao in enumerate(lista_opcoes, 1):
            print(f"{i}. {opcao}")
        print("0. Finalizar seleção")
        
        try:
            escolha = int(input("\nEscolha uma opção (número): "))
            if escolha == 0:
                break
            if 1 <= escolha <= len(lista_opcoes):
                opcao = lista_opcoes[escolha - 1]
                if opcao not in selecionados:
                    selecionados.append(opcao)
                    print(f"\n{opcao} adicionado!")
                else:
                    print("\nEsta opção já foi selecionada!")
            else:
                print("\nOpção inválida!")
        except ValueError:
            print("\nPor favor, digite um número válido!")
    
    return selecionados

def coletar_dados_regra() -> Dict[str, Any]:
    """
    Coleta os dados para uma nova regra.
    
    Returns:
        Dicionário com os dados da regra
    """
    print("\n=== Nova Regra de Carreira ===")
    
    carreira = input("\nNome da carreira: ").strip()
    while not carreira:
        print("O nome da carreira não pode estar vazio!")
        carreira = input("Nome da carreira: ").strip()
    
    interesses = selecionar_opcoes(INTERESSES, "Selecione os Interesses")
    while not interesses:
        print("Você deve selecionar pelo menos um interesse!")
        interesses = selecionar_opcoes(INTERESSES, "Selecione os Interesses")
    
    habilidades = selecionar_opcoes(HABILIDADES, "Selecione as Habilidades")
    while not habilidades:
        print("Você deve selecionar pelo menos uma habilidade!")
        habilidades = selecionar_opcoes(HABILIDADES, "Selecione as Habilidades")
    
    print("\nNotas mínimas necessárias:")
    desempenho = {}
    disciplinas_selecionadas = selecionar_opcoes(DISCIPLINAS, "Selecione as Disciplinas")
    while not disciplinas_selecionadas:
        print("Você deve selecionar pelo menos uma disciplina!")
        disciplinas_selecionadas = selecionar_opcoes(DISCIPLINAS, "Selecione as Disciplinas")
    
    for disciplina in disciplinas_selecionadas:
        while True:
            try:
                nota = float(input(f"\nNota mínima para {disciplina} (0-10): "))
                if 0 <= nota <= 10:
                    desempenho[disciplina] = nota
                    break
                else:
                    print("A nota deve estar entre 0 e 10!")
            except ValueError:
                print("Por favor, digite um número válido!")
    
    print("\nPesos das disciplinas:")
    pesos = {}
    for disciplina in disciplinas_selecionadas:
        while True:
            try:
                peso = float(input(f"\nPeso para {disciplina} (1-3): "))
                if 1 <= peso <= 3:
                    pesos[disciplina] = peso
                    break
                else:
                    print("O peso deve estar entre 1 e 3!")
            except ValueError:
                print("Por favor, digite um número válido!")
    
    justificativa = input("\nJustificativa para a carreira: ").strip()
    while not justificativa:
        print("A justificativa não pode estar vazia!")
        justificativa = input("Justificativa para a carreira: ").strip()
    
    return {
        "carreira": carreira,
        "condicoes": {
            "interesses": interesses,
            "habilidades": habilidades,
            "desempenho": desempenho,
            "pesos": pesos
        },
        "justificativa": justificativa
    }

def exibir_regra(regra: Dict[str, Any]) -> None:
    """
    Exibe os detalhes de uma regra.
    
    Args:
        regra: Regra a ser exibida
    """
    print(f"\n=== Regra: {regra['carreira']} ===")
    print(f"\nJustificativa: {regra['justificativa']}")
    
    print("\nCondições:")
    condicoes = regra['condicoes']
    
    if condicoes.get('interesses'):
        print("\nInteresses necessários:")
        for interesse in condicoes['interesses']:
            print(f"- {interesse}")
    
    if condicoes.get('habilidades'):
        print("\nHabilidades necessárias:")
        for habilidade in condicoes['habilidades']:
            print(f"- {habilidade}")
    
    if condicoes.get('desempenho'):
        print("\nNotas mínimas necessárias:")
        for disciplina, nota in condicoes['desempenho'].items():
            print(f"- {disciplina}: {nota}")
    
    if condicoes.get('pesos'):
        print("\nPesos das disciplinas:")
        for disciplina, peso in condicoes['pesos'].items():
            print(f"- {disciplina}: {peso}")

def executar_menu_gestor(caminho_regras: str) -> None:
    """
    Executa o menu do gestor acadêmico.
    
    Args:
        caminho_regras: Caminho para o arquivo de regras
    """
    gestor = GestorRegras(caminho_regras)
    
    while True:
        opcao = exibir_menu_gestor()
        
        if opcao == "1":  # listar regras
            regras = gestor.listar_regras()
            if regras:
                print("\nRegras existentes:")
                for regra in regras:
                    print(f"- {regra['carreira']}")
            else:
                print("\nNenhuma regra cadastrada.")
        
        elif opcao == "2":  # adicionar regra
            regra = coletar_dados_regra()
            if gestor.adicionar_regra(regra):
                print("\nRegra adicionada com sucesso!")
            else:
                print("\nErro ao adicionar regra. Verifique se os dados estão corretos.")
        
        elif opcao == "3":  # editar regra
            regras = gestor.listar_regras()
            if not regras:
                print("\nNenhuma regra cadastrada para editar.")
                continue
                
            print("\nCarreiras disponíveis:")
            for i, regra in enumerate(regras, 1):
                print(f"{i}. {regra['carreira']}")
            
            while True:
                try:
                    escolha = int(input("\nEscolha o número da carreira a ser editada: "))
                    if 1 <= escolha <= len(regras):
                        carreira = regras[escolha - 1]['carreira']
                        regra_atual = gestor.obter_regra(carreira)
                        print("\nRegra atual:")
                        exibir_regra(regra_atual)
                        print("\nNovos dados:")
                        nova_regra = coletar_dados_regra()
                        if gestor.editar_regra(carreira, nova_regra):
                            print("\nRegra atualizada com sucesso!")
                        else:
                            print("\nErro ao atualizar regra. Verifique se os dados estão corretos.")
                        break
                    else:
                        print("\nOpção inválida!")
                except ValueError:
                    print("\nPor favor, digite um número válido!")
        
        elif opcao == "4":  # remover regra
            regras = gestor.listar_regras()
            if not regras:
                print("\nNenhuma regra cadastrada para remover.")
                continue
                
            print("\nCarreiras disponíveis:")
            for i, regra in enumerate(regras, 1):
                print(f"{i}. {regra['carreira']}")
            
            while True:
                try:
                    escolha = int(input("\nEscolha o número da carreira a ser removida: "))
                    if 1 <= escolha <= len(regras):
                        carreira = regras[escolha - 1]['carreira']
                        if gestor.remover_regra(carreira):
                            print("\nRegra removida com sucesso!")
                        else:
                            print(f"\nCarreira '{carreira}' não encontrada.")
                        break
                    else:
                        print("\nOpção inválida!")
                except ValueError:
                    print("\nPor favor, digite um número válido!")
        
        elif opcao == "5":  # visualizar regra
            regras = gestor.listar_regras()
            if not regras:
                print("\nNenhuma regra cadastrada para visualizar.")
                continue
                
            print("\nCarreiras disponíveis:")
            for i, regra in enumerate(regras, 1):
                print(f"{i}. {regra['carreira']}")
            
            while True:
                try:
                    escolha = int(input("\nEscolha o número da carreira a ser visualizada: "))
                    if 1 <= escolha <= len(regras):
                        carreira = regras[escolha - 1]['carreira']
                        regra = gestor.obter_regra(carreira)
                        if regra:
                            exibir_regra(regra)
                        else:
                            print(f"\nCarreira '{carreira}' não encontrada.")
                        break
                    else:
                        print("\nOpção inválida!")
                except ValueError:
                    print("\nPor favor, digite um número válido!")
        
        elif opcao == "6":  # voltar
            break
        
        else:
            print("\nOpção inválida!")
        
        input("\nPressione Enter para continuar...") 
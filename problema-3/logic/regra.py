import json

class Regra:
    """
    Classe que representa uma regra de recomendação de carreira.
    
    Uma regra define os critérios necessários para recomendar uma carreira,
    incluindo interesses, habilidades e desempenho escolar requeridos.
    """

    def __init__(self, rule_data):
        """
        Inicializa uma regra com base em um dicionário de dados.

        Args:
            regras_data (dict): Dicionário contendo os dados da regra:
                - id: Identificador único da regra
                - descricao: Descrição da regra
                - criterios: Critérios necessários (interesses, habilidades, desempenho)
                - recomendacao: Carreira recomendada
                - peso_total_regra: Peso total da regra
                - pesos_criterios: Pesos individuais para cada critério
        """
        self.id = rule_data.get("id")
        self.descricao = rule_data.get("descricao")
        self.criterios = rule_data.get("criterios", {})
        self.recomendacao = rule_data.get("recomendacao")
        self.peso_total_regra = rule_data.get("peso_total_regra", 1)
        self.pesos_criterios = rule_data.get("pesos_criterios", {})

  
    def checa_criterios(self, estudante):
        """
        Verifica se um estudante atende aos critérios definidos nesta regra.

        Args:
            estudante (Estudante): Objeto estudante com seus dados.

        Returns:
            bool: True se o estudante atende a todos os critérios, False caso contrário.
        """
        regra_aplica = True

        for criterio_tipo, valores_requeridos in self.criterios.items():
            dados_estudante = getattr(estudante, criterio_tipo, None)

            if dados_estudante is None:
                 if valores_requeridos:
                     regra_aplica = False
                     break
                 else:
                     continue

            if isinstance(valores_requeridos, list):
                if not any(item in dados_estudante for item in valores_requeridos):
                    regra_aplica = False
                    break

            elif isinstance(valores_requeridos, dict):
                for disciplina_requerida, nota_minima in valores_requeridos.items():
                    if disciplina_requerida not in dados_estudante or dados_estudante[disciplina_requerida] < nota_minima:
                        regra_aplica = False
                        break
                if not regra_aplica:
                    break

        return regra_aplica

    def __str__(self):
        return f"Regra(ID: {self.id}, Recomendacao: {self.recomendacao})"

    def __repr__(self):
        return self.__str__() 
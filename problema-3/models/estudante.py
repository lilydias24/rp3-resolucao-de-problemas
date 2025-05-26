"""
Módulo de definição da classe Estudante.

A classe Estudante representa um indivíduo com interesses, habilidades
e desempenho escolar, utilizados para recomendação de carreiras.
"""
class Estudante:
    """
    Representa um estudante com dados relevantes para recomendação de carreira.

    Atributos:
        interesses (list[str]): Lista de áreas de interesse (ex: 'artes', 'tecnologia').
        habilidades (list[str]): Lista de habilidades do estudante (ex: 'programação').
        desempenho_escolar (dict): Notas em disciplinas, no formato {'matemática': 8.5}.
    """
    def __init__(self, nome, interesses=None, habilidades=None, desempenho_escolar=None):
        """
        Inicializa um estudante com dados fornecidos.

        Args:
            nome (str): Nome do estudante.
            interesses (list[str], optional): Interesses pessoais.
            habilidades (list[str], optional): Habilidades do estudante.
            desempenho_escolar (dict, optional): Desempenho por disciplina.
        """
        self.nome = nome
        self.interesses = interesses if interesses is not None else []
        self.habilidades = habilidades if habilidades is not None else []
        self.desempenho_escolar = desempenho_escolar if desempenho_escolar is not None else {}

    def __str__(self):
        """
        Retorna uma representação legível do estudante.

        Returns:
            str: Nome do estudante.
            str: Texto com os dados principais do estudante.
        """
        return (f"Estudante(Nome: {self.nome}, Interesses: {self.interesses}, "
                f"Habilidades: {self.habilidades}, Desempenho Escolar: {self.desempenho_escolar})")

    def __repr__(self):
        return self.__str__() 
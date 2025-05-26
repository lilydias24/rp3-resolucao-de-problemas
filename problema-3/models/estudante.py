class Estudante:
    def __init__(self, interesses=None, habilidades=None, desempenho_escolar=None):
        self.interesses = interesses if interesses is not None else []
        self.habilidades = habilidades if habilidades is not None else []
        self.desempenho_escolar = desempenho_escolar if desempenho_escolar is not None else {}

    def __str__(self):
        return f"Estudante(Interesses: {self.interesses}, Habilidades: {self.habilidades}, Desempenho Escolar: {self.desempenho_escolar})"

    def __repr__(self):
        return self.__str__() 
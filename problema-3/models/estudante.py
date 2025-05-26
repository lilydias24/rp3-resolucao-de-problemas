"""
Módulo de definição da classe Estudante.

A classe Estudante representa um indivíduo com interesses, habilidades
e desempenho escolar, utilizados para recomendação de carreiras.
"""
class Estudante:
    """
    Representa um estudante com dados relevantes para recomendação de carreira.

    Atributos:
        nome (str): Nome do estudante.
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

    def adicionar_habilidade(self, habilidade: str) -> None:
        """
        Adiciona uma habilidade ao estudante após validação.

        Args:
            habilidade (str): Habilidade a ser adicionada.

        Raises:
            TypeError: Se a habilidade não for uma string.
            ValueError: Se a habilidade for uma string vazia.
        """
        if not isinstance(habilidade, str):
            raise TypeError("A habilidade precisa ser uma string.")

        texto = habilidade.strip().lower()
        if not texto:
            raise ValueError("Campo vazio.")

        if texto not in self.habilidades:
            self.habilidades.append(texto)

    def to_dict(self):
        """
        Converte o objeto Estudante em um dicionário para uso nas regras lógicas.

        Returns:
            dict: Dicionário com os dados do estudante.
        """
        return {
            'nome': self.nome,
            'interesses': self.interesses,
            'habilidades': self.habilidades,
            'desempenho_escolar': self.desempenho_escolar
        }

    def __str__(self):
        """
        Retorna uma representação legível do estudante.

        Returns:
            str: Texto com os dados principais do estudante.
        """
        return (f"Estudante(Nome: {self.nome}, Interesses: {self.interesses}, "
                f"Habilidades: {self.habilidades}, Desempenho Escolar: {self.desempenho_escolar})")

    def __repr__(self):
        return self.__str__()


if __name__ == "__main__":
    # Testes básicos
    aluno = Estudante("Mariana")
    aluno.adicionar_habilidade("programação")
    aluno.adicionar_habilidade("física")
    print(aluno.to_dict())
    # saída esperada --> {'nome': 'Mariana', 'interesses': [], 'habilidades': ['programação', 'física'], 'desempenho_escolar': {}}
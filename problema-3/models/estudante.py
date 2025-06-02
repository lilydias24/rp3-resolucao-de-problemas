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
    REGRAS_CARREIRA: dict[str, str] = \
        {
            "programação": "Desenvolvedor(a)",
            "física": "Engenheiro(a) de Hardware",
            "gerenciar": "Gerente de Tarefas",
            "matemática": "Analista de Dados",
        }

    def __init__(self, nome: str, interesses: list[str] = None) -> None:
        """
        Inicializa um estudante com dados fornecidos.

        Args:
            nome (str): Nome do estudante.
            interesses (list[str], optional): Interesses pessoais.
        """
        self.nome: str = nome
        self.interesses: list[str] = interesses or []
        self.habilidades: set[str] = set()
        self.desempenho_escolar: dict[str, float] = {}

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
            self.habilidades.add(texto)

    def to_dict(self) -> dict:
        """
        Converte o objeto Estudante em um dicionário para uso nas regras lógicas.

        Returns:
            dict: Dicionário com os dados do estudante.
        """
        return {
            'nome': self.nome,
            'interesses': self.interesses,
            'habilidades': list(self.habilidades),
            'desempenho': self.desempenho_escolar
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

    def metricas_escola(self, materia_escola: str, desempenho: float) -> dict[str, float]:
        '''
        Registra (ou atualiza) o desempenho do estudante em uma determinada matéria.
        Se a matéria já existir no histórico, atualiza a nota; caso contrário, adiciona.
        Retorna sempre o dicionário completo de desempenho.
        '''
        # validações básicas
        if not isinstance(materia_escola, str):
            raise TypeError("O nome da matéria precisa ser uma string")

        if not materia_escola.strip():
            raise ValueError("O nome da matéria não pode ser vazio")

        if not isinstance(desempenho, (int, float)):
            raise TypeError("O desempenho precisa ser um número")

        chave = materia_escola.strip()
        self.desempenho_escolar[chave] = float(desempenho)
        return self.desempenho_escolar


if __name__ == "__main__":
    # Testes básicos
    aluno = Estudante("Mariana")
    aluno.adicionar_habilidade("programação")
    aluno.adicionar_habilidade("física")
    print(aluno.to_dict())
    # saída esperada --> {'nome': 'Mariana', 'interesses': [], 'habilidades': ['programação', 'física'], 'desempenho': {}}
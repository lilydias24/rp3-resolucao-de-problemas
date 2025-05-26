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
    
# Merge with student.py    
    
    '''
    regras de inferencia básicas
    '''
    REGRAS_CARREIRA: dict[str, str] = \
        {
            "programação": "Desenvolvedor(a)",
            "física": "Engenheiro(a) de Hardware",
            "gerenciamento": "Gerente de Tarefas",
            "matemática": "Analista de Dados",
        }

    def __init__(self, nome: str) -> None:
        self.nome: str = nome
        self.habilidades: set[str] = set()

    def adicionar_habilidade(self, habilidade: str) -> None:

        '''
        valida dados inseridos entradas inválidas,
        e adiciona uma habilidade ao estudante caso passe nas validações
        '''
        if not isinstance(habilidade, str):
            raise TypeError("a habilidade precisa ser uma string.")

        texto = habilidade.strip().lower()
        if not texto:
            raise ValueError("campo vazio.")

        self.habilidades.add(texto)

    def possiveis_carreiras(self) -> list[str]:

        '''
        retorna carreiras compatíveis com as habilidades informadas,
        caso não haja carreira compativel retorna 'carreira não definida'
        '''
        carreiras = [
            carreira
            for chave, carreira in self.REGRAS_CARREIRA.items()
            if chave in self.habilidades
        ]
        return carreiras or ["carreira não definida"]


if __name__ == "__main__":
    aluno = Estudante("Mariana")
    aluno.adicionar_habilidade(" programação ")
    aluno.adicionar_habilidade("física")
    print(aluno.possiveis_carreiras())
    '''
    saída esperada --> ['desenvolvedor(a)', 'engenheiro(a) de hardware']
    '''

    outro = Estudante("carlos")
    outro.adicionar_habilidade("culinária")
    print(outro.possiveis_carreiras())
    '''
    saída esperada --> ['carreira não definida']
    '''
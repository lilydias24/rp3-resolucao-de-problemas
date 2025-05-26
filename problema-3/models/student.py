class Estudante:
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

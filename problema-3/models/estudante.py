class Estudante:
    '''
    Regras de inferência básicas
    '''
    REGRAS_CARREIRA: dict[str, str] = {
        "programação": "Desenvolvedor(a)",
        "física": "Engenheiro(a) de Hardware",
        "gerenciar": "Gerente de Tarefas",
        "matemática": "Analista de Dados",
    }

    def __init__(self, nome: str) -> None:
        self.nome: str = nome
        self.habilidades: set[str] = set()
        self.desempenho_escolar: dict[str, float] = {}

    def adicionar_habilidade(self, habilidade: str) -> None:
        '''
        Valida dados e adiciona habilidade ao estudante
        '''
        if not isinstance(habilidade, str):
            raise TypeError("A habilidade precisa ser uma string.")

        texto = habilidade.strip().lower()
        if not texto:
            raise ValueError("Campo vazio.")

        self.habilidades.add(texto)

    def metricas_escola(self, materia_escola: str, desempenho: float) -> dict[str, float]:
        '''
        Registra ou atualiza o desempenho do estudante em uma determinada matéria.
        '''
        if not isinstance(materia_escola, str):
            raise TypeError("O nome da matéria precisa ser uma string.")
        if not materia_escola.strip():
            raise ValueError("O nome da matéria não pode ser vazio.")
        if not isinstance(desempenho, (int, float)):
            raise TypeError("O desempenho precisa ser um número.")

        chave = materia_escola.strip().lower()
        self.desempenho_escolar[chave] = float(desempenho)
        return self.desempenho_escolar

    def possiveis_carreiras(self) -> list[str]:
        '''
        Retorna carreiras compatíveis com as habilidades.
        '''
        carreiras = [
            carreira
            for chave, carreira in self.REGRAS_CARREIRA.items()
            if chave in self.habilidades
        ]
        return carreiras or ["carreira não definida"]

    def __str__(self) -> str:
        return str({
            "nome": self.nome,
            "interesses": [],  # ainda não implementado
            "habilidades": list(self.habilidades),
            "desempenho_escolar": self.desempenho_escolar
        })


# Teste
if __name__ == "__main__":
    aluno = Estudante("Mariana")
    aluno.adicionar_habilidade(" programação ")
    aluno.adicionar_habilidade("física")
    print(aluno)
    print(aluno.possiveis_carreiras())

    outro = Estudante("carlos")
    outro.adicionar_habilidade("culinária")
    print(outro.possiveis_carreiras())

    print(aluno.metricas_escola("matemática", 2.0))
    print(aluno.metricas_escola("física", 4.0))
    print(aluno.metricas_escola("matemática", 6.0))
    print(aluno.metricas_escola("resolução problemas", 12.0))

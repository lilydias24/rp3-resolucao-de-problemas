class Estudante:
    '''
    regras de inferencia básicas
    '''
    REGRAS_CARREIRA: dict[str, str] = \
        {
            "programação": "Desenvolvedor(a)",
            "física": "Engenheiro(a) de Hardware",
            "gerenciar": "Gerente de Tarefas",
            "matemática": "Analista de Dados",
        }

    def __init__(self, nome: str) -> None:
        self.nome: str = nome
        self.habilidades: set[str] = set()
        self.historico_desempenho: list[dict[str, float]] = []

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

    def metricas_escola(self, materia_escola: str, desempenho: float) -> list[dict[str, float]]:
        '''
        Registra (ou atualiza) o desempenho do estudante em uma determinada matéria.
        Se a matéria já existir no histórico, atualiza a nota; caso contrário, adiciona.
        Retorna sempre a lista completa de histórico de desempenho.
        '''
        # validações básicas
        if not isinstance(materia_escola, str):
            raise TypeError("O nome da matéria precisa ser uma string")

        if not materia_escola.strip():
            raise ValueError("O nome da matéria não pode ser vazio")

        if not isinstance(desempenho, (int, float)):
            raise TypeError("O desempenho precisa ser um número")


        chave = materia_escola.strip()
        # dicionário a ser inserido ou atualizado
        novo_registro = {chave: float(desempenho)}

        # se a lista estiver vazia, basta adicionar
        if not self.historico_desempenho:
            self.historico_desempenho.append(novo_registro)

        else:
            # tenta encontrar registro existente para essa matéria
            for registro in self.historico_desempenho:
                if chave in registro:
                    registro[chave] = float(desempenho)
                    break
            else:
                # só chega aqui se não encontrou a matéria
                self.historico_desempenho.append(novo_registro)

        return self.historico_desempenho


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
    aluno = Estudante("Mariana")
    aluno.adicionar_habilidade(" programação ")
    aluno.adicionar_habilidade("física")
    print(aluno.to_dict())
    # saída esperada --> {'nome': 'Mariana', 'interesses': [], 'habilidades': ['programação', 'física'], 'desempenho_escolar': {}}                                      
    
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
    print(aluno.metricas_escola("matematica",2.0))
    print(aluno.metricas_escola("fisica", 4.0))
    print(aluno.metricas_escola("matematica", 6.0))
    print(aluno.metricas_escola("resolução problemas", 12.0))
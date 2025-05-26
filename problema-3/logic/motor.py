import json
import os 
from .regra import Regra

class MotorDeInferencia:
    """
    Motor de inferência responsável por processar as regras e gerar recomendações de carreiras.
    
    Esta classe carrega as regras de um arquivo JSON, processa os dados do estudante
    e gera recomendações baseadas nas regras aplicáveis ou carreiras próximas.
    """

    def __init__(self, regras_file_path=None):
        """
        Inicializa o motor de inferência.

        Args:
            regras_file_path (str, optional): Caminho para o arquivo de regras.
                Se não fornecido, usa o caminho padrão.
        """
        # construir o caminho do arquivo de regras relativo a esse arquivo, no caso o motor.py
        # se um caminho especifico for dado, usa ele, se nao, constroi o caminho padrao
        if regras_file_path is None:
            current_dir = os.path.dirname(__file__) 
            self.regras_file_path = os.path.join(current_dir, "..", "data", "regras.json")
        else:
             self.regras_file_path = regras_file_path

        self.regras = []
        self.carregar_regras()

    def carregar_regras(self):
        """
        Carrega as regras do arquivo JSON especificado.
        
        Raises:
            FileNotFoundError: Se o arquivo de regras não for encontrado.
            json.JSONDecodeError: Se o arquivo JSON estiver mal formatado.
        """
        try:
            # usar o caminho construido, ja citado
            with open(self.regras_file_path, 'r', encoding='utf-8') as f:
                regras_data = json.load(f)
                self.regras = [Regra(regra_data) for regra_data in regras_data]
        except FileNotFoundError:
            print(f"Erro: Arquivo de regras não encontrado em {self.regras_file_path}")
        except json.JSONDecodeError:
            print(f"Erro ao decodificar JSON no arquivo {self.regras_file_path}")
        except Exception as e:
            print(f"Ocorreu um erro ao carregar as regras: {e}")

    def calcula_proximidade(self, estudante, regra):
        """
        Calcula a proximidade do estudante com uma regra específica.

        Args:
            estudante (Estudante): Objeto estudante com seus dados.
            regra (Regra): Regra a ser comparada.

        Returns:
            float: Valor entre 0 e 1 representando a proximidade, onde 1 é a maior proximidade.
        """
        pontuacao = 0
        total_criterios = 0

        # verif os interesses
        if "interesses" in regra.criterios and estudante.interesses:
            interesses_regra = set(regra.criterios["interesses"])
            interesses_estudante = set(estudante.interesses)
            if interesses_regra and interesses_estudante:
                total_criterios += 1
                pontuacao += len(interesses_regra.intersection(interesses_estudante)) / len(interesses_regra)

        # verif as habilidades
        if "habilidades" in regra.criterios and estudante.habilidades:
            habilidades_regra = set(regra.criterios["habilidades"])
            habilidades_estudante = set(estudante.habilidades)
            if habilidades_regra and habilidades_estudante:
                total_criterios += 1
                pontuacao += len(habilidades_regra.intersection(habilidades_estudante)) / len(habilidades_regra)

        # verif o desempenho escolar
        if "desempenho_escolar" in regra.criterios and estudante.desempenho_escolar:
            desempenho_regra = regra.criterios["desempenho_escolar"]
            desempenho_estudante = estudante.desempenho_escolar
            if desempenho_regra and desempenho_estudante:
                total_criterios += 1
                materias_comuns = set(desempenho_regra.keys()).intersection(set(desempenho_estudante.keys()))
                if materias_comuns:
                    pontuacao_desempenho = sum(1 for materia in materias_comuns 
                                             if desempenho_estudante[materia] >= desempenho_regra[materia])
                    pontuacao += pontuacao_desempenho / len(materias_comuns)

        return pontuacao / total_criterios if total_criterios > 0 else 0

    def processa_estudante(self, estudante):
        """
        Processa os dados do estudante e gera recomendações de carreiras.

        Args:
            estudante (Estudante): Objeto estudante com seus dados.

        Returns:
            dict: Dicionário contendo:
                - recomendacoes: Dict com carreiras recomendadas e suas pontuações
                - carreiras_proximas: Lista de carreiras próximas com suas proximidades
                - nenhuma_recomendacao: Boolean indicando se não há recomendações diretas
        """
        recomendacoes_pontuadas = {}
        carreiras_proximas = []

        # verif cada regra pra ver se se aplica ao estudante
        for regra in self.regras:
            if regra.checa_criterios(estudante):
                recomendacao = regra.recomendacao
                peso = regra.peso_total_regra

                if recomendacao:
                    if recomendacao in recomendacoes_pontuadas:
                        recomendacoes_pontuadas[recomendacao] += peso
                    else:
                        recomendacoes_pontuadas[recomendacao] = peso
            else:
                # calcula a proximidade pra regras não atendidas
                proximidade = self.calcula_proximidade(estudante, regra)
                if proximidade > 0.3:  # considera so carreiras com proximidade maior que 30%
                    carreiras_proximas.append({
                        "carreira": regra.recomendacao,
                        "proximidade": proximidade,
                        "descricao": regra.descricao
                    })

        # ordena as carreiras próximas por proximidade
        carreiras_proximas.sort(key=lambda x: x["proximidade"], reverse=True)

        resultado = {
            "recomendacoes": recomendacoes_pontuadas,
            "carreiras_proximas": carreiras_proximas[:3] if carreiras_proximas else [],  # retorna as 3 mais próximas
            "nenhuma_recomendacao": len(recomendacoes_pontuadas) == 0
        }

        return resultado
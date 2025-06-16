"""
Módulo controlador do sistema.
"""
from typing import Dict, List, Tuple, Any
from data.conexao import conectar, ConexaoErro
from data.criar_banco import criar_tabelas
from data.transacao import executar_consulta, executar_comando, transacao
from logic.estudante import salvar_estudante, buscar_estudante_completo_por_nome, listar_estudantes
from logic.motor import MotorDeInferencia
from logic.recomendacao import salvar_recomendacao, listar_recomendacoes, cadastrar_regra, listar_regras, atualizar_peso_regra, atualizar_regra, remover_regra
from reports.gerar_relatorios import gerar_relatorios
from utils.cores import erro, sucesso, aviso
from utils.interface import Interface
from utils.gestor_interface import GestorInterface
from reports.graficos import GeradorGraficos
from data.relatorio_db import RelatorioDB
import json
from datetime import datetime
import os

class Controlador:
    """
    Classe controladora do sistema.
    """
    
    def __init__(self):
        """
        Inicializa o controlador.
        """
        try:
            # Inicializa o banco
            criar_tabelas()
            
            # Conecta ao banco
            self.conexao = conectar()
            
            # Inicializa o motor
            self.motor = MotorDeInferencia()
            
            self.relatorio_db = RelatorioDB()
            
        except ConexaoErro as e:
            raise ConexaoErro(f"Erro ao inicializar o sistema: {str(e)}")

    def cadastrar_novo_estudante(self) -> Dict[str, List]:
        """
        Cadastra um novo estudante e retorna suas recomendações.
        
        Returns:
            Dict com as recomendações do estudante
        """
        dados = Interface.cadastrar_estudante()
        query = """
            INSERT INTO estudantes (nome, interesses, habilidades, desempenho)
            VALUES (?, ?, ?, ?)
        """
        executar_comando(self.conexao, query, (
            dados['nome'],
            json.dumps(dados['interesses']),
            json.dumps(dados['habilidades']),
            json.dumps(dados['desempenho'])
        ))
        return self.obter_recomendacoes(dados['nome'])

    def buscar_estudante(self, nome: str) -> Tuple:
        """
        Busca um estudante pelo nome.
        
        Args:
            nome: Nome do estudante
            
        Returns:
            Tupla com dados do estudante ou None se não encontrado
        """
        query = """
            SELECT e.id, e.nome, 
                   GROUP_CONCAT(DISTINCT i.interesse) as interesses,
                   GROUP_CONCAT(DISTINCT h.habilidade) as habilidades,
                   json_group_object(d.disciplina, de.nota) as desempenho
            FROM estudantes e
            LEFT JOIN estudantes_interesses ei ON e.id = ei.estudante_id
            LEFT JOIN interesses i ON ei.interesse_id = i.id
            LEFT JOIN estudantes_habilidades eh ON e.id = eh.estudante_id
            LEFT JOIN habilidades h ON eh.habilidade_id = h.id
            LEFT JOIN desempenho_estudante de ON e.id = de.estudante_id
            LEFT JOIN disciplinas d ON de.disciplina_id = d.id
            WHERE e.nome = ?
            GROUP BY e.id, e.nome
        """
        resultado = executar_consulta(self.conexao, query, (nome,))
        if resultado:
            id_, nome, interesses, habilidades, desempenho = resultado[0]
            return (
                id_,
                nome,
                interesses.split(',') if interesses else [],
                habilidades.split(',') if habilidades else [],
                json.loads(desempenho) if desempenho else {}
            )
        return None

    def listar_todos_estudantes(self) -> List[Tuple]:
        """
        Lista todos os estudantes cadastrados.
        
        Returns:
            Lista de tuplas com dados dos estudantes
        """
        return self.relatorio_db.listar_estudantes()

    def obter_recomendacoes(self, nome: str) -> Dict[str, List]:
        """
        Obtém as recomendações de carreira para um estudante.
        
        Args:
            nome: Nome do estudante
            
        Returns:
            Dict com as recomendações do estudante
        """
        estudante = self.buscar_estudante(nome)
        if not estudante:
            raise ConexaoErro(f"Estudante '{nome}' não encontrado!")
        
        query = "SELECT * FROM regras_carreira"
        regras = executar_consulta(self.conexao, query)
        
        recomendacoes = {
            'recomendadas': [],
            'proximas': []
        }
        
        for regra in regras:
            id_, carreira, justificativa = regra
            
            # Busca interesses
            interesses = executar_consulta(self.conexao, """
                SELECT DISTINCT i.interesse FROM regras_interesses ri
                JOIN interesses i ON ri.interesse_id = i.id
                WHERE ri.regra_id = ?
                ORDER BY i.interesse
            """, (id_,))
            
            # Busca habilidades
            habilidades = executar_consulta(self.conexao, """
                SELECT DISTINCT h.habilidade FROM regras_habilidades rh
                JOIN habilidades h ON rh.habilidade_id = h.id
                WHERE rh.regra_id = ?
                ORDER BY h.habilidade
            """, (id_,))
            
            # Busca desempenho
            desempenho = executar_consulta(self.conexao, """
                SELECT DISTINCT d.disciplina, rd.nota_min, rd.peso FROM regras_desempenho rd
                JOIN disciplinas d ON rd.disciplina_id = d.id
                WHERE rd.regra_id = ?
                ORDER BY d.disciplina
            """, (id_,))
            
            # Organiza os critérios
            criterios = {
                'interesses': [i[0] for i in interesses],
                'habilidades': [h[0] for h in habilidades],
                'desempenho': {d[0]: d[1] for d in desempenho},
                'pesos': {d[0]: d[2] for d in desempenho}
            }
            
            # Verifica se o estudante atende aos critérios
            score = 0
            explicacao = {}
            
            # Verifica interesses
            if criterios['interesses']:
                interesses_comuns = set(estudante[2]) & set(criterios['interesses'])
                if interesses_comuns:
                    score += len(interesses_comuns) / len(criterios['interesses'])
                    explicacao['interesses'] = f"Interesses compatíveis: {', '.join(interesses_comuns)}"
                else:
                    explicacao['interesses'] = f"Faltam interesses: {', '.join(criterios['interesses'])}"
            
            # Verifica habilidades
            if criterios['habilidades']:
                habilidades_comuns = set(estudante[3]) & set(criterios['habilidades'])
                if habilidades_comuns:
                    score += len(habilidades_comuns) / len(criterios['habilidades'])
                    explicacao['habilidades'] = f"Habilidades compatíveis: {', '.join(habilidades_comuns)}"
                else:
                    explicacao['habilidades'] = f"Faltam habilidades: {', '.join(criterios['habilidades'])}"
            
            # Verifica desempenho
            if criterios['desempenho']:
                desempenho_ok = True
                for disciplina, nota_min in criterios['desempenho'].items():
                    if disciplina not in estudante[4] or estudante[4][disciplina] < nota_min:
                        desempenho_ok = False
                        break
                if desempenho_ok:
                    score += 1
                    explicacao['desempenho'] = "Desempenho acadêmico adequado"
                else:
                    explicacao['desempenho'] = f"Faltam notas mínimas em algumas disciplinas"
            
            # Normaliza o score
            num_criterios = sum(1 for c in [criterios['interesses'], criterios['habilidades'], criterios['desempenho']] if c)
            if num_criterios > 0:
                score = score / num_criterios
            
            # Adiciona à lista apropriada
            recomendacao = {
                'carreira': carreira,
                'score': score,
                'justificativa': justificativa or f"Score de {score:.2%} baseado nos critérios da carreira",
                'explicacao': explicacao
            }
            
            if score >= 0.8:  # 80% ou mais de compatibilidade
                recomendacoes['recomendadas'].append(recomendacao)
            elif score >= 0.5:  # 50% ou mais de compatibilidade
                recomendacoes['proximas'].append(recomendacao)
        
        return recomendacoes

    def gerar_relatorios_sistema(self) -> None:
        """
        Gera todos os relatórios do sistema.
        
        Raises:
            Exception: Se houver erro ao gerar relatórios
        """
        try:
            gerar_relatorios()
        except Exception as e:
            raise Exception(f"Erro ao gerar relatórios: {str(e)}")

    def executar_menu_gestor(self) -> None:
        """
        Executa o menu do gestor acadêmico.
        """
        while True:
            opcao = GestorInterface.exibir_menu_gestor()
            
            if opcao == "1":
                try:
                    dados = Interface.cadastrar_regra()
                    cadastrar_regra(dados['carreira'], dados['criterios'])
                    Interface.exibir_sucesso("Regra adicionada com sucesso!")
                except Exception as e:
                    Interface.exibir_erro(f"Erro ao adicionar regra: {str(e)}")
            
            elif opcao == "2":
                try:
                    nome = Interface.solicitar_nome_carreira()
                    if not nome:
                        Interface.exibir_erro("Nome da carreira não pode estar vazio!")
                        continue
                    
                    # Busca a regra
                    query = "SELECT id FROM regras_carreira WHERE carreira = ?"
                    regra = executar_consulta(self.conexao, query, (nome,))
                    if not regra:
                        Interface.exibir_erro(f"Regra para carreira '{nome}' não encontrada!")
                        continue
                    
                    regra_id = regra[0][0]
                    
                    # Busca dados atuais
                    interesses = executar_consulta(self.conexao, """
                        SELECT DISTINCT i.interesse FROM regras_interesses ri
                        JOIN interesses i ON ri.interesse_id = i.id
                        WHERE ri.regra_id = ?
                        ORDER BY i.interesse
                    """, (regra_id,))
                    
                    habilidades = executar_consulta(self.conexao, """
                        SELECT DISTINCT h.habilidade FROM regras_habilidades rh
                        JOIN habilidades h ON rh.habilidade_id = h.id
                        WHERE rh.regra_id = ?
                        ORDER BY h.habilidade
                    """, (regra_id,))
                    
                    desempenho = executar_consulta(self.conexao, """
                        SELECT DISTINCT d.disciplina, rd.nota_min, rd.peso FROM regras_desempenho rd
                        JOIN disciplinas d ON rd.disciplina_id = d.id
                        WHERE rd.regra_id = ?
                        ORDER BY d.disciplina
                    """, (regra_id,))
                    
                    regra_atual = {
                        'carreira': nome,
                        'condicoes': {
                            'interesses': [i[0] for i in interesses],
                            'habilidades': [h[0] for h in habilidades],
                            'desempenho': {d[0]: d[1] for d in desempenho},
                            'pesos': {d[0]: d[2] for d in desempenho}
                        }
                    }
                    
                    dados = Interface.editar_regra(regra_atual)
                    atualizar_regra(regra_id, dados)
                    Interface.exibir_sucesso("Regra atualizada com sucesso!")
                except Exception as e:
                    Interface.exibir_erro(f"Erro ao editar regra: {str(e)}")
            
            elif opcao == "3":
                try:
                    nome = Interface.solicitar_nome_carreira()
                    if not nome:
                        Interface.exibir_erro("Nome da carreira não pode estar vazio!")
                        continue
                    
                    # Busca a regra
                    query = "SELECT id FROM regras_carreira WHERE carreira = ?"
                    regra = executar_consulta(self.conexao, query, (nome,))
                    if not regra:
                        Interface.exibir_erro(f"Regra para carreira '{nome}' não encontrada!")
                        continue
                    
                    regra_id = regra[0][0]
                    remover_regra(regra_id)
                    Interface.exibir_sucesso("Regra removida com sucesso!")
                except Exception as e:
                    Interface.exibir_erro(f"Erro ao remover regra: {str(e)}")
            
            elif opcao == "4":
                try:
                    regras = listar_regras()
                    Interface.exibir_lista_regras(regras)
                except Exception as e:
                    Interface.exibir_erro(f"Erro ao listar regras: {str(e)}")
            
            elif opcao == "5":
                self.executar_menu_relatorios()
            
            elif opcao == "6":
                self.executar_menu_graficos()
            
            elif opcao == "7":
                break
            
            else:
                Interface.exibir_erro("Opção inválida!")
            
            Interface.aguardar_continuar()

    def executar_menu_relatorios(self) -> None:
        """
        Executa o menu de relatórios.
        """
        while True:
            opcao = GestorInterface.exibir_menu_relatorios()
            
            # Cria diretório para relatórios
            relatorios_dir = 'reports/relatorios'
            os.makedirs(relatorios_dir, exist_ok=True)
            
            if opcao == "6":
                break
                
            # Pula a seleção de formato se a opção for inválida
            if opcao not in ["1", "2", "3", "4", "5"]:
                Interface.exibir_erro("Opção inválida!")
                Interface.aguardar_continuar()
                continue
                
            # Solicita o formato do relatório
            formato = GestorInterface.exibir_menu_formato_relatorio()
            if formato not in ["1", "2"]:
                Interface.exibir_erro("Formato inválido!")
                Interface.aguardar_continuar()
                continue
                
            try:
                if opcao == "1":  # Relatório de estudantes
                    estudantes = self.relatorio_db.listar_estudantes()
                    if formato == "1":  # JSON
                        with open(os.path.join(relatorios_dir, 'relatorio_estudantes.json'), 'w', encoding='utf-8') as f:
                            json.dump(estudantes, f, ensure_ascii=False, indent=2)
                        Interface.exibir_sucesso("Relatório de estudantes gerado em JSON com sucesso!")
                    else:  # CSV
                        from utils.exportador_csv import exportar_estudantes_para_csv
                        exportar_estudantes_para_csv(os.path.join(relatorios_dir, 'estudantes.csv'))
                        Interface.exibir_sucesso("Relatório de estudantes gerado em CSV com sucesso!")
                
                elif opcao == "2":  # Relatório de regras
                    regras = listar_regras()
                    if formato == "1":  # JSON
                        with open(os.path.join(relatorios_dir, 'relatorio_regras.json'), 'w', encoding='utf-8') as f:
                            json.dump(regras, f, ensure_ascii=False, indent=2)
                        Interface.exibir_sucesso("Relatório de regras gerado em JSON com sucesso!")
                    else:  # CSV
                        from utils.exportador_csv import exportar_regras_para_csv
                        exportar_regras_para_csv(os.path.join(relatorios_dir, 'regras.csv'))
                        Interface.exibir_sucesso("Relatório de regras gerado em CSV com sucesso!")
                
                elif opcao == "3":  # Relatório de estatísticas
                    stats = {
                        'total_estudantes': len(self.relatorio_db.listar_estudantes()),
                        'total_regras': len(listar_regras()),
                        'data_geracao': datetime.now().isoformat()
                    }
                    if formato == "1":  # JSON
                        with open(os.path.join(relatorios_dir, 'relatorio_stats.json'), 'w', encoding='utf-8') as f:
                            json.dump(stats, f, ensure_ascii=False, indent=2)
                        Interface.exibir_sucesso("Relatório de estatísticas gerado em JSON com sucesso!")
                    else:  # CSV
                        from utils.exportador_csv import exportar_estatisticas_para_csv
                        exportar_estatisticas_para_csv(os.path.join(relatorios_dir, 'estatisticas.csv'))
                        Interface.exibir_sucesso("Relatório de estatísticas gerado em CSV com sucesso!")
                
                elif opcao == "4":  # Relatório de tendências
                    if formato == "1":  # JSON
                        from data.conexao import conectar
                        conn = conectar()
                        cursor = conn.cursor()
                        cursor.execute("""
                            SELECT carreira, COUNT(*) as total
                            FROM recomendacoes
                            GROUP BY carreira
                            ORDER BY total DESC
                        """)
                        resultados = cursor.fetchall()
                        conn.close()
                        
                        with open(os.path.join(relatorios_dir, 'relatorio_tendencias.json'), 'w', encoding='utf-8') as f:
                            json.dump([{"carreira": c, "total": t} for c, t in resultados], f, ensure_ascii=False, indent=2)
                        Interface.exibir_sucesso("Relatório de tendências gerado em JSON com sucesso!")
                    else:  # CSV
                        from utils.exportador_csv import exportar_tendencias_para_csv
                        exportar_tendencias_para_csv(os.path.join(relatorios_dir, 'tendencias.csv'))
                        Interface.exibir_sucesso("Relatório de tendências gerado em CSV com sucesso!")
                
                elif opcao == "5":  # Todos os relatórios
                    if formato == "1":  # JSON
                        gerar_relatorios()
                        Interface.exibir_sucesso("Todos os relatórios gerados em JSON com sucesso!")
                    else:  # CSV
                        from utils.exportador_csv import exportar_todos_relatorios_csv
                        exportar_todos_relatorios_csv()
                        Interface.exibir_sucesso("Todos os relatórios gerados em CSV com sucesso!")
                
            except Exception as e:
                Interface.exibir_erro(f"Erro ao gerar relatório: {str(e)}")
            
            Interface.aguardar_continuar()

    def executar_menu_graficos(self) -> None:
        """
        Executa o menu de gráficos.
        """
        while True:
            opcao = GestorInterface.exibir_menu_graficos()
            
            if opcao == "1":
                try:
                    gerador = GeradorGraficos()
                    estudantes = self.relatorio_db.listar_estudantes()
                    for _, nome, _, _, desempenho in estudantes:
                        if desempenho:
                            gerador.grafico_desempenho_estudante(desempenho, nome)
                    Interface.exibir_sucesso("Gráficos de desempenho por estudante gerados com sucesso!")
                except Exception as e:
                    Interface.exibir_erro(f"Erro ao gerar gráficos de desempenho por estudante: {str(e)}")
            
            elif opcao == "2":
                try:
                    gerador = GeradorGraficos()
                    disciplinas = self.relatorio_db.obter_disciplinas()
                    for disciplina in disciplinas:
                        dados = self.relatorio_db.obter_desempenho_disciplina(disciplina)
                        if dados:
                            gerador.grafico_desempenho_disciplina(
                                {d['estudante']: d['nota'] for d in dados},
                                disciplina
                            )
                    Interface.exibir_sucesso("Gráficos de desempenho por disciplina gerados com sucesso!")
                except Exception as e:
                    Interface.exibir_erro(f"Erro ao gerar gráficos de desempenho por disciplina: {str(e)}")
            
            elif opcao == "3":
                try:
                    gerador = GeradorGraficos()
                    recomendacoes = self.relatorio_db.obter_recomendacoes()
                    if recomendacoes:
                        gerador.grafico_recomendacoes(recomendacoes)
                        Interface.exibir_sucesso("Gráfico de distribuição de recomendações gerado com sucesso!")
                    else:
                        Interface.exibir_aviso("Não há recomendações para gerar o gráfico.")
                except Exception as e:
                    Interface.exibir_erro(f"Erro ao gerar gráfico de recomendações: {str(e)}")
            
            elif opcao == "4":
                try:
                    gerador = GeradorGraficos()
                    gerador.gerar_todos_graficos()
                    Interface.exibir_sucesso("Todos os gráficos gerados com sucesso!")
                except Exception as e:
                    Interface.exibir_erro(f"Erro ao gerar gráficos: {str(e)}")
            
            elif opcao == "5":
                break
            
            else:
                Interface.exibir_erro("Opção inválida!")
            
            Interface.aguardar_continuar() 
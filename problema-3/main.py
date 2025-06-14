"""
Sistema de recomendação de carreiras usando paradigma lógico.

Este módulo executa o fluxo principal do sistema:
- Coleta os interesses de um estudante via terminal
- Coleta o desempenho acadêmico do estudante
- Constrói os fatos lógicos a partir dos interesses e desempenho
- Salva os dados no banco SQLite
- Lista os estudantes registrados
"""
import os
from data.conexao import conectar
from logic.estudante import buscar_estudante, cadastrar_estudante, listar_estudantes, buscar_estudante_completo_por_nome, recomendar_carreiras
from logic.logica import carreiras_proximas, gerar_fatos_de_interesses
from logic.motor import MotorDeInferencia
from logic.recomendacao import salvar_recomendacao, listar_recomendacoes
from utils.gestor_interface import executar_menu_gestor
from data.transacao import ConexaoErro
from utils.cores import titulo, sucesso, erro, aviso, destaque, cabecalho, menu_item, info, score, negrito, sublinhado

def exibir_menu():
    """
    Exibe o menu principal do sistema.
    """
    print(cabecalho("Sistema de Recomendação de Carreiras"))
    print(menu_item("1", "Cadastrar novo estudante"))
    print(menu_item("2", "Listar estudantes cadastrados"))
    print(menu_item("3", "Buscar estudante por nome"))
    print(menu_item("4", "Ver recomendações de carreira"))
    print(menu_item("5", "Menu do Gestor Acadêmico"))
    print(menu_item("6", "Sair"))
    return input("\n" + destaque("Escolha uma opção: ")).strip()

def exibir_dados_estudante(estudante):
    """
    Exibe os dados de um estudante.
    
    Args:
        estudante: Tupla com os dados do estudante (id, nome, interesses, habilidades, desempenho)
    """
    id_, nome, interesses, habilidades, desempenho = estudante
    
    print(cabecalho(f"Dados do Estudante"))
    print(destaque("ID:") + f" {id_}")
    print(destaque("Nome:") + f" {nome}")
    
    print("\n" + destaque("Interesses:"))
    if interesses:
        for interesse in interesses:
            print(f"  • {info(interesse)}")
    else:
        print(aviso("  Nenhum interesse registrado"))
    
    print("\n" + destaque("Habilidades:"))
    if habilidades:
        for habilidade in habilidades:
            print(f"  • {info(habilidade)}")
    else:
        print(aviso("  Nenhuma habilidade registrada"))
    
    print("\n" + destaque("Desempenho Acadêmico:"))
    if desempenho:
        for disciplina, nota in desempenho.items():
            print(f"  • {disciplina}: {nota(nota)}")
    else:
        print(aviso("  Nenhum desempenho registrado"))

def exibir_recomendacoes(estudante, motor):
    """
    Exibe as recomendações de carreira para um estudante.
    
    Args:
        estudante: Tupla com os dados do estudante
        motor: Instância do motor de inferência
    """
    id_, nome, interesses, habilidades, desempenho = estudante
    
    # Cria um dicionário com os dados do estudante
    dados_estudante = {
        'nome': nome,
        'interesses': interesses,
        'habilidades': habilidades,
        'notas': desempenho
    }
    
    # Processa o estudante no motor de inferência
    recomendadas, proximas = motor.processa_estudante(dados_estudante)
    
    print(cabecalho(f"Recomendações de Carreira para {nome}"))
    
    print("\n" + destaque("Carreiras Recomendadas:"))
    if recomendadas:
        for c in recomendadas:
            print(f"\n  {destaque('•')} {negrito(c['carreira'])} {score(c['score'])}")
            print(f"    {sublinhado('Justificativa:')} {c['justificativa']}")
            print(f"\n    {sublinhado('Explicação:')}")
            for tipo, explicacao in c['explicacao'].items():
                print(f"    {destaque('•')} {explicacao}")
    else:
        print("\n" + aviso("  Nenhuma carreira recomendada no momento."))
        print(aviso("  Para ter uma carreira recomendada, você precisa atender TODOS os critérios"))
        print(aviso("  (interesses, habilidades e desempenho) para pelo menos uma carreira."))
    
    print("\n" + destaque("Carreiras Próximas:"))
    if proximas:
        proximas.sort(key=lambda x: x['score'], reverse=True)
        
        for c in proximas:
            print(f"\n  {destaque('•')} {negrito(c['carreira'])} {score(c['score'])}")
            print(f"    {sublinhado('Justificativa:')} {c['justificativa']}")
            print(f"\n    {sublinhado('Explicação:')}")
            for tipo, explicacao in c['explicacao'].items():
                print(f"    {destaque('•')} {explicacao}")
            
            print(f"\n    {sublinhado('Sugestões para transformar em carreira recomendada:')}")
            for tipo, explicacao in c['explicacao'].items():
                if "Faltam" in explicacao:
                    print(f"    {destaque('•')} {explicacao.replace('Faltam', 'Adquira')}")
    else:
        print(aviso("  Nenhuma carreira próxima no momento."))
    
    # Atualiza as recomendações no banco de dados
    try:
        salvar_recomendacao(id_, {
            'recomendadas': recomendadas,
            'proximas': proximas
        })
    except ConexaoErro as e:
        print(erro(f"\nAviso: Não foi possível salvar as recomendações: {str(e)}"))

def main():
    """
    Função principal que inicia o sistema.
    """
    CAMINHO_REGRAS = os.path.join(os.path.dirname(__file__), 'data', 'regras.json')
    motor = MotorDeInferencia()  # Remova o argumento CAMINHO_REGRAS
    
    # Inicializa o banco de dados
    try:
        conectar()
    except ConexaoErro as e:
        print(erro(f"\nErro ao inicializar banco de dados: {str(e)}"))
        return
    
    while True:
        opcao = exibir_menu()
        
        if opcao == "1":  
            estudante = cadastrar_estudante(CAMINHO_REGRAS)
            recomendadas, proximas = motor.processa_estudante(estudante)
            
            print("\n" + destaque("Carreiras recomendadas:"))
            if recomendadas:
                for c in recomendadas:
                    print(f"\n  {destaque('•')} {negrito(c['carreira'])} {score(c['score'])}")
                    print(f"    {sublinhado('Justificativa:')} {c['justificativa']}")
                    print(f"\n    {sublinhado('Explicação:')}")
                    for tipo, explicacao in c['explicacao'].items():
                        print(f"    {destaque('•')} {explicacao}")
            else:
                print("\n" + aviso("  Nenhuma carreira recomendada no momento."))
                print(aviso("  Para ter uma carreira recomendada, você precisa atender TODOS os critérios"))
                print(aviso("  (interesses, habilidades e desempenho) para pelo menos uma carreira."))
            
            print("\n" + destaque("Carreiras próximas:"))
            if proximas:
                proximas.sort(key=lambda x: x['score'], reverse=True)
                
                for c in proximas:
                    print(f"\n  {destaque('•')} {negrito(c['carreira'])} {score(c['score'])}")
                    print(f"    {sublinhado('Justificativa:')} {c['justificativa']}")
                    print(f"\n    {sublinhado('Explicação:')}")
                    for tipo, explicacao in c['explicacao'].items():
                        print(f"    {destaque('•')} {explicacao}")
                    
                    print(f"\n    {sublinhado('Sugestões para transformar em carreira recomendada:')}")
                    for tipo, explicacao in c['explicacao'].items():
                        if "Faltam" in explicacao:
                            print(f"    {destaque('•')} {explicacao.replace('Faltam', 'Adquira')}")
            else:
                print(aviso("  Nenhuma carreira próxima no momento."))
        
        elif opcao == "2":
            print("\n" + aviso("Funcionalidade ainda não implementada."))
        
        elif opcao == "3":
            nome = input("\n" + destaque("Digite o nome do estudante: ")).strip()
            if not nome:
                print(erro("\nNome não pode estar vazio!"))
                continue
            
            try:
                estudante = buscar_estudante_completo_por_nome(nome)
                if estudante:
                    exibir_dados_estudante(estudante)
                else:
                    print(aviso(f"\nNenhum estudante encontrado com o nome '{nome}'"))
            except ConexaoErro as e:
                print(erro(f"\nErro ao buscar estudante: {str(e)}"))
        
        elif opcao == "4":
            nome = input("\n" + destaque("Digite o nome do estudante: ")).strip()
            if not nome:
                print(erro("\nNome não pode estar vazio!"))
                continue
            
            try:
                estudante = buscar_estudante_completo_por_nome(nome)
                if estudante:
                    exibir_recomendacoes(estudante, motor)
                else:
                    print(aviso(f"\nNenhum estudante encontrado com o nome '{nome}'"))
            except ConexaoErro as e:
                print(erro(f"\nErro ao buscar estudante: {str(e)}"))
        
        elif opcao == "5":
            executar_menu_gestor(CAMINHO_REGRAS)
        
        elif opcao == "6":
            if input("\n" + destaque("Tem certeza que deseja sair? (s/n): ")).lower() == 's':
                print(sucesso("\nEncerrando o sistema..."))
                break
        
        else:
            print(erro("\nOpção inválida! Por favor, escolha uma opção válida."))
        
        input("\n" + destaque("Pressione Enter para continuar..."))

if __name__ == "__main__":
    main()

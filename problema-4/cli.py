import typer
import requests
import sys
import os
from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict
from src.utils.colors import (
    print_header, print_success, print_error, print_warning, print_info,
    print_menu_title, print_menu_option, print_separator, print_highlight,
    print_muted, print_accent, print_primary, print_secondary,
    format_id, format_name, format_status, format_priority, format_timestamp,
    format_description, format_list_item, format_table_header, format_table_row,
    print_loading, print_done, print_processing, print_section_header,
    print_subsection_header, print_field_label, print_field_value
)

API_URL = "http://localhost:8000"
TOKEN_FILE = ".token"

app = typer.Typer()

def save_token(token: str):
    with open(TOKEN_FILE, "w") as f:
        f.write(token)

def load_token() -> Optional[str]:
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE) as f:
            return f.read().strip()
    return None

def auth_headers():
    token = load_token()
    if not token:
        typer.echo("Você precisa fazer login primeiro.")
        raise typer.Exit()
    return {"Authorization": f"Bearer {token}"}

# --- AUTENTICAÇÃO ---
@app.command()
def register():
    """Registrar novo usuário"""
    print_header("REGISTRO DE USUÁRIO")
    email = typer.prompt("Email")
    name = typer.prompt("Nome")
    password = typer.prompt("Senha", hide_input=False)
    data = {"email": email, "name": name, "password": password}
    resp = requests.post(f"{API_URL}/auth/register", json=data)
    if resp.status_code == 201:
        print_success("Usuário registrado com sucesso!")
    else:
        print_error(f"Erro: {resp.json().get('detail', resp.text)}")

@app.command()
def login():
    """Login de usuário"""
    print_header("LOGIN DE USUÁRIO")
    email = typer.prompt("Email")
    password = typer.prompt("Senha", hide_input=True)
    data = {"username": email, "password": password}
    resp = requests.post(f"{API_URL}/auth/login", data=data)
    if resp.status_code == 200:
        token = resp.json()["access_token"]
        save_token(token)
        print_success("Login realizado com sucesso!")
    else:
        print_error(f"Erro: {resp.json().get('detail', resp.text)}")

# --- PRODUTOS ---
def produtos_menu():
    while True:
        print_menu_title("Produtos")
        print_menu_option("\t 1", "Listar produtos")
        print_menu_option("\t 2", "Cadastrar produto")
        print_menu_option("\t 3", "Visualizar produto")
        print_menu_option("\t 4", "Editar produto")
        print_menu_option("\t 5", "Remover produto")
        print_menu_option("\t 0", "Voltar")
        opt = typer.prompt(">>> Opção : ")
        if opt == "1":
            resp = requests.get(f"{API_URL}/dashboard/recent-products", headers=auth_headers())
            if resp.status_code == 200:
                print_info("Produtos encontrados:")
                for p in resp.json():
                    typer.echo(f"{format_id(str(p['id']))} | {format_name(p['name'])} | {format_description(p['description'])}")
            else:
                print_error("Erro ao listar produtos.")
        elif opt == "2":
            name = typer.prompt("Nome do produto (deve conter espaço)")
            description = typer.prompt("Descrição do produto")
            personas = typer.prompt("Personas envolvidas (separe por vírgula)")
            personas = [p.strip() for p in personas.split(",") if p.strip()]
            value_proposition = typer.prompt("Proposta de valor")
            platforms = typer.prompt("Plataformas (web, mobile, desktop, api) [separe por vírgula]")
            platforms = [p.strip() for p in platforms.split(",") if p.strip()]
            data = {
                "name": name,
                "description": description,
                "personas": personas,
                "value_proposition": value_proposition,
                "platforms": platforms
            }
            resp = requests.post(f"{API_URL}/products/", json=data, headers=auth_headers())
            if resp.status_code == 201:
                print_success(f"Produto cadastrado: {resp.json()['name']} (ID: {resp.json()['product_id']})")
            else:
                print_error(f"Erro: {resp.json().get('detail', resp.text)}")
        elif opt == "3":
            pid = typer.prompt("ID do produto")
            resp = requests.get(f"{API_URL}/products/{pid}", headers=auth_headers())
            if resp.status_code == 200:
                p = resp.json()
                print_section_header("Detalhes do Produto")
                typer.echo(f"{format_id(str(p.get('product_id', p.get('id', 'N/A'))))}")
                typer.echo(f"{format_name(p.get('name', 'N/A'))}")
                typer.echo(f"{format_description(p.get('description', 'N/A'))}")
                if 'personas' in p and p['personas']:
                    typer.echo(f"Personas: {', '.join(p['personas'])}")
                if 'value_proposition' in p:
                    typer.echo(f"{print_field_label('Proposta de Valor')} {print_field_value(p['value_proposition'])}")
                if 'platforms' in p:
                    typer.echo(f"{print_field_label('Plataformas')} {print_field_value(', '.join(p['platforms']))}")
            else:
                print_error("Produto não encontrado.")
        elif opt == "4":
            pid = typer.prompt("ID do produto a editar")
            name = typer.prompt("Novo nome", default="")
            description = typer.prompt("Nova descrição", default="")
            personas = typer.prompt("Novas personas (separe por vírgula)", default="")
            value_proposition = typer.prompt("Nova proposta de valor", default="")
            platforms = typer.prompt("Novas plataformas (separe por vírgula)", default="")
            data = {}
            if name: data["name"] = name
            if description: data["description"] = description
            if personas: data["personas"] = [p.strip() for p in personas.split(",") if p.strip()]
            if value_proposition: data["value_proposition"] = value_proposition
            if platforms: data["platforms"] = [p.strip() for p in platforms.split(",") if p.strip()]
            resp = requests.put(f"{API_URL}/products/{pid}", json=data, headers=auth_headers())
            if resp.status_code == 200:
                print_success("Produto atualizado!")
            else:
                print_error(f"Erro: {resp.json().get('detail', resp.text)}")
        elif opt == "5":
            pid = typer.prompt("ID do produto a remover")
            resp = requests.delete(f"{API_URL}/products/{pid}", headers=auth_headers())
            if resp.status_code == 204:
                print_success("Produto removido!")
            else:
                print_error(f"Erro: {resp.json().get('detail', resp.text)}")
        elif opt == "0":
            break
        else:
            typer.echo("Opção inválida!")

# --- ÉPICOS ---
def epicos_menu():
    while True:
        print_menu_title("Épicos")
        print_menu_option("\t 1", "Listar épicos de um produto")
        print_menu_option("\t 2", "Criar épico para produto")
        print_menu_option("\t 3", "Visualizar épico")
        print_menu_option("\t 4", "Editar épico")
        print_menu_option("\t 5", "Remover épico")
        print_menu_option("\t 6", "Visualizar histórico de revisões")
        print_menu_option("\t 7", "Gerenciar revisões")
        print_menu_option("\t 8", "Revisar épicos")
        print_menu_option("\t 0", "Voltar")
        opt = typer.prompt(">>> Opção : ")
        if opt == "1":
            pid = typer.prompt("ID do produto")
            resp = requests.get(f"{API_URL}/products/{pid}/epics", headers=auth_headers())
            if resp.status_code == 200:
                for e in resp.json():
                    typer.echo(f"{format_id(str(e['epic_id']))} | {format_name(e['title'])} | {format_description(e['description'])}")
            else:
                print_error("Erro ao listar épicos.")
        elif opt == "2":
            pid = typer.prompt("ID do produto")
            title = typer.prompt("Título do épico")
            description = typer.prompt("Descrição do épico")
            data = {"title": title, "description": description}
            resp = requests.post(f"{API_URL}/products/{pid}/epics", json=data, headers=auth_headers())
            if resp.status_code == 200 or resp.status_code == 201:
                print_success(f"Épico criado: {resp.json()['title']} (ID: {resp.json()['epic_id']})")
            else:
                print_error(f"Erro: {resp.json().get('detail', resp.text)}")
        elif opt == "3":
            eid = typer.prompt("ID do épico")
            resp = requests.get(f"{API_URL}/epics/{eid}", headers=auth_headers())
            if resp.status_code == 200:
                e = resp.json()
                print_section_header("Detalhes do Épico")
                typer.echo(f"{format_id(str(e.get('epic_id', 'N/A')))}")
                typer.echo(f"{format_name(e.get('title', 'N/A'))}")
                typer.echo(f"{format_description(e.get('description', 'N/A'))}")
                if 'status' in e:
                    typer.echo(f"{print_field_label('Status')} {format_status(e['status'])}")
                if 'created_at' in e:
                    typer.echo(f"{print_field_label('Criado em')} {format_timestamp(e['created_at'])}")
                if 'updated_at' in e:
                    typer.echo(f"{print_field_label('Atualizado em')} {format_timestamp(e['updated_at'])}")
            else:
                print_error("Épico não encontrado.")
        elif opt == "4":
            eid = typer.prompt("ID do épico a editar")
            title = typer.prompt("Novo título", default="")
            description = typer.prompt("Nova descrição", default="")
            data = {}
            if title: data["title"] = title
            if description: data["description"] = description
            resp = requests.put(f"{API_URL}/epics/{eid}", json=data, headers=auth_headers())
            if resp.status_code == 200:
                print_success("Épico atualizado!")
            else:
                print_error(f"Erro: {resp.json().get('detail', resp.text)}")
        elif opt == "5":
            eid = typer.prompt("ID do épico a remover")
            resp = requests.delete(f"{API_URL}/epics/{eid}", headers=auth_headers())
            if resp.status_code == 204:
                print_success("Épico removido!")
            else:
                print_error(f"Erro: {resp.json().get('detail', resp.text)}")
        elif opt == "6":
            eid = typer.prompt("ID do épico")
            resp = requests.get(f"{API_URL}/products/epics/{eid}/revisions", headers=auth_headers())
            if resp.status_code == 200:
                revisions = resp.json()
                if revisions:
                    print_section_header(f"Histórico de revisões do épico {eid}")
                    for rev in revisions:
                        typer.echo(f"{print_field_label('Campo')} {print_field_value(rev['field_changed'])}")
                        typer.echo(f"{print_field_label('Antes')} {print_muted(str(rev['old_value']))}")
                        typer.echo(f"{print_field_label('Depois')} {print_highlight(str(rev['new_value']))}")
                        typer.echo(f"{print_field_label('Data')} {format_timestamp(rev['changed_at'])}")
                        typer.echo(f"{print_field_label('Motivo')} {print_accent(str(rev['change_reason']))}")
                        print_separator()
                else:
                    print_info("Nenhuma revisão encontrada para este épico.")
            else:
                print_error("Erro ao obter histórico de revisões.")
        elif opt == "7":
            eid = typer.prompt("ID do épico")
            typer.echo("\n--- Gerenciamento de Revisão ---")
            typer.echo("\t 1 - Ver informações de revisão")
            typer.echo("\t 2 - Adicionar comentário")
            typer.echo("\t 3 - Aprovar épico")
            typer.echo("\t 4 - Rejeitar épico")
            typer.echo("\t 5 - Solicitar revisão")
            typer.echo("\t 6 - Marcar como implementado")
            typer.echo("\t 0 - Voltar")
            review_opt = typer.prompt(">>> Opção : ")
            
            if review_opt == "1":
                resp = requests.get(f"{API_URL}/review/epic/{eid}/info", headers=auth_headers())
                if resp.status_code == 200:
                    info = resp.json()
                    typer.echo(f"Status atual: {info['current_status']}")
                    typer.echo(f"Total de comentários: {info['total_comments']}")
                    typer.echo(f"Revisões pendentes: {info['pending_reviews']}")
                    if info['last_review_date']:
                        typer.echo(f"Última revisão: {info['last_review_date']} por {info['reviewed_by']}")
                else:
                    print_error("Erro ao buscar informações de revisão.")
            
            elif review_opt == "2":
                comment = typer.prompt("Comentário")
                is_suggestion = typer.confirm("É uma sugestão de melhoria?")
                suggested_changes = ""
                if is_suggestion:
                    suggested_changes = typer.prompt("Sugestões específicas de mudanças")
                
                data = {
                    "entity_type": "epic",
                    "entity_id": int(eid),
                    "comment": comment,
                    "is_suggestion": is_suggestion,
                    "suggested_changes": suggested_changes
                }
                resp = requests.post(f"{API_URL}/review/comments", json=data, headers=auth_headers())
                if resp.status_code == 200:
                    print_success("Comentário adicionado com sucesso!")
                else:
                    print_error(f"Erro: {resp.json().get('detail', resp.text)}")
            
            elif review_opt == "3":
                comment = typer.prompt("Comentário (opcional)", default="")
                reason = typer.prompt("Motivo da aprovação (opcional)", default="")
                data = {
                    "action": "approve",
                    "comment": comment if comment else None,
                    "reason": reason if reason else None
                }
                resp = requests.post(f"{API_URL}/review/epic/{eid}/action", json=data, headers=auth_headers())
                if resp.status_code == 200:
                    print_success("Épico aprovado com sucesso!")
                else:
                    print_error(f"Erro: {resp.json().get('detail', resp.text)}")
            
            elif review_opt == "4":
                comment = typer.prompt("Comentário (opcional)", default="")
                reason = typer.prompt("Motivo da rejeição")
                data = {
                    "action": "reject",
                    "comment": comment if comment else None,
                    "reason": reason
                }
                resp = requests.post(f"{API_URL}/review/epic/{eid}/action", json=data, headers=auth_headers())
                if resp.status_code == 200:
                    print_success("Épico rejeitado.")
                else:
                    print_error(f"Erro: {resp.json().get('detail', resp.text)}")
            
            elif review_opt == "5":
                comment = typer.prompt("Comentário sobre o que precisa ser revisado")
                reason = typer.prompt("Motivo da solicitação de revisão")
                data = {
                    "action": "request_revision",
                    "comment": comment,
                    "reason": reason
                }
                resp = requests.post(f"{API_URL}/review/epic/{eid}/action", json=data, headers=auth_headers())
                if resp.status_code == 200:
                    print_success("Solicitação de revisão enviada!")
                else:
                    print_error(f"Erro: {resp.json().get('detail', resp.text)}")
            
            elif review_opt == "6":
                comment = typer.prompt("Comentário (opcional)", default="")
                reason = typer.prompt("Motivo (opcional)", default="")
                data = {
                    "action": "mark_implemented",
                    "comment": comment if comment else None,
                    "reason": reason if reason else None
                }
                resp = requests.post(f"{API_URL}/review/epic/{eid}/action", json=data, headers=auth_headers())
                if resp.status_code == 200:
                    print_success("Épico marcado como implementado!")
                else:
                    print_error(f"Erro: {resp.json().get('detail', resp.text)}")
            
            elif review_opt == "0":
                continue
            else:
                print_warning("Opção inválida!")
        elif opt == "8":
            revisar_epicos_menu()
        elif opt == "0":
            break
        else:
            print_warning("Opção inválida!")

def revisar_epicos_menu():
    while True:
        print_menu_title("Revisão de Épicos")
        print_menu_option("1", "Listar épicos de um produto")
        print_menu_option("2", "Visualizar detalhes e revisão de um épico")
        print_menu_option("3", "Editar épico")
        print_menu_option("4", "Adicionar comentário/sugestão")
        print_menu_option("5", "Executar ação de revisão (aprovar, rejeitar, etc.)")
        print_menu_option("6", "Visualizar histórico de revisões do épico")
        print_menu_option("0", "Voltar")
        opt = typer.prompt(">>> Opção : ")
        if opt == "1":
            pid = typer.prompt("ID do produto")
            resp = requests.get(f"{API_URL}/products/{pid}/epics", headers=auth_headers())
            if resp.status_code == 200:
                for e in resp.json():
                    typer.echo(f"ID: {e['epic_id']} | {e['title']}\n  {e['description']}")
            else:
                print_error("Erro ao listar épicos.")
        elif opt == "2":
            eid = typer.prompt("ID do épico")
            resp = requests.get(f"{API_URL}/products/epics/{eid}", headers=auth_headers())
            if resp.status_code == 200:
                e = resp.json()
                print_section_header("Detalhes do Épico")
                typer.echo(f"ID: {e.get('epic_id', 'N/A')}")
                typer.echo(f"Título: {e.get('title', 'N/A')}")
                typer.echo(f"Descrição: {e.get('description', 'N/A')}")
                # Status de revisão
                info = requests.get(f"{API_URL}/review/epic/{eid}/info", headers=auth_headers())
                if info.status_code == 200:
                    i = info.json()
                    typer.echo(f"Status: {i['current_status']}")
                    typer.echo(f"Total de comentários: {i['total_comments']}")
                    typer.echo(f"Revisões pendentes: {i['pending_reviews']}")
                    if i['last_review_date']:
                        typer.echo(f"Última revisão: {i['last_review_date']} por {i['reviewed_by']}")
                # Comentários
                comments = requests.get(f"{API_URL}/review/comments/epic/{eid}", headers=auth_headers())
                if comments.status_code == 200:
                    print_info("Comentários:")
                    for c in comments.json():
                        typer.echo(f"- {c['comment']} (Sugestão: {'Sim' if c['is_suggestion'] else 'Não'})")
                else:
                    print_info("Nenhum comentário.")
            else:
                print_error("Épico não encontrado.")
        elif opt == "3":
            eid = typer.prompt("ID do épico a editar")
            title = typer.prompt("Novo título", default="")
            description = typer.prompt("Nova descrição", default="")
            data = {}
            if title: data["title"] = title
            if description: data["description"] = description
            resp = requests.put(f"{API_URL}/products/epics/{eid}", json=data, headers=auth_headers())
            if resp.status_code == 200:
                print_success("Épico atualizado!")
            else:
                print_error(f"Erro: {resp.json().get('detail', resp.text)}")
        elif opt == "4":
            eid = typer.prompt("ID do épico")
            comment = typer.prompt("Comentário")
            is_suggestion = typer.confirm("É uma sugestão de melhoria?")
            suggested_changes = ""
            if is_suggestion:
                suggested_changes = typer.prompt("Sugestões específicas de mudanças")
            data = {
                "entity_type": "epic",
                "entity_id": int(eid),
                "comment": comment,
                "is_suggestion": is_suggestion,
                "suggested_changes": suggested_changes
            }
            resp = requests.post(f"{API_URL}/review/comments", json=data, headers=auth_headers())
            if resp.status_code == 200:
                print_success("Comentário adicionado com sucesso!")
            else:
                print_error(f"Erro: {resp.json().get('detail', resp.text)}")
        elif opt == "5":
            eid = typer.prompt("ID do épico")
            typer.echo("Ações disponíveis: 1-Aprovar, 2-Rejeitar, 3-Solicitar revisão, 4-Marcar como implementado")
            action_opt = typer.prompt("Escolha a ação")
            action_map = {
                "1": "approve",
                "2": "reject",
                "3": "request_revision",
                "4": "mark_implemented"
            }
            action = action_map.get(action_opt)
            if not action:
                print_warning("Ação inválida!")
                continue
            comment = typer.prompt("Comentário (opcional)", default="")
            reason = typer.prompt("Motivo (opcional)", default="")
            data = {
                "action": action,
                "comment": comment if comment else None,
                "reason": reason if reason else None
            }
            resp = requests.post(f"{API_URL}/review/epic/{eid}/action", json=data, headers=auth_headers())
            if resp.status_code == 200:
                print_success(f"Ação '{action}' executada com sucesso!")
            else:
                print_error(f"Erro: {resp.json().get('detail', resp.text)}")
        elif opt == "6":
            eid = typer.prompt("ID do épico")
            resp = requests.get(f"{API_URL}/products/epics/{eid}/revisions", headers=auth_headers())
            if resp.status_code == 200:
                revisions = resp.json()
                if revisions:
                    print_section_header(f"Histórico de revisões do épico {eid}")
                    for rev in revisions:
                        typer.echo(f"{print_field_label('Campo')} {print_field_value(rev['field_changed'])}")
                        typer.echo(f"{print_field_label('Antes')} {print_muted(str(rev['old_value']))}")
                        typer.echo(f"{print_field_label('Depois')} {print_highlight(str(rev['new_value']))}")
                        typer.echo(f"{print_field_label('Data')} {format_timestamp(rev['changed_at'])}")
                        typer.echo(f"{print_field_label('Motivo')} {print_accent(str(rev['change_reason']))}")
                        print_separator()
                else:
                    print_info("Nenhuma revisão encontrada para este épico.")
            else:
                print_error("Erro ao obter histórico de revisões.")
        elif opt == "0":
            break
        else:
            print_warning("Opção inválida!")

# --- HISTÓRIAS DE USUÁRIO ---
def historias_menu():
    while True:
        print_menu_title("Histórias de Usuário")
        print_menu_option("\t 1", "Listar histórias de um épico")
        print_menu_option("\t 2", "Criar história para épico")
        print_menu_option("\t 3", "Visualizar história")
        print_menu_option("\t 4", "Editar história")
        print_menu_option("\t 5", "Remover história")
        print_menu_option("\t 6", "Visualizar histórico de revisões")
        print_menu_option("\t 7", "Revisar histórias")
        print_menu_option("\t 0", "Voltar")
        opt = typer.prompt(">>> Opção : ")
        if opt == "1":
            eid = typer.prompt("ID do épico")
            resp = requests.get(f"{API_URL}/epics/{eid}/user-stories", headers=auth_headers())
            if resp.status_code == 200:
                for hs in resp.json():
                    typer.echo(f"{format_id(str(hs['user_story_id']))} | {format_name(hs['title'])} | {format_description(hs['description'])}")
            else:
                print_error("Erro ao listar histórias.")
        elif opt == "2":
            eid = typer.prompt("ID do épico")
            title = typer.prompt("Título da história")
            description = typer.prompt("Descrição da história")
            data = {"title": title, "description": description}
            resp = requests.post(f"{API_URL}/epics/{eid}/user-stories", json=data, headers=auth_headers())
            if resp.status_code == 200 or resp.status_code == 201:
                print_success(f"História criada: {resp.json()['title']} (ID: {resp.json()['user_story_id']})")
            else:
                print_error(f"Erro: {resp.json().get('detail', resp.text)}")
        elif opt == "3":
            hs_id = typer.prompt("ID da história")
            resp = requests.get(f"{API_URL}/user-stories/{hs_id}", headers=auth_headers())
            if resp.status_code == 200:
                hs = resp.json()
                print_section_header("Detalhes da História")
                typer.echo(f"{format_id(str(hs.get('user_story_id', 'N/A')))}")
                typer.echo(f"{format_name(hs.get('title', 'N/A'))}")
                typer.echo(f"{format_description(hs.get('description', 'N/A'))}")
                if 'status' in hs:
                    typer.echo(f"{print_field_label('Status')} {format_status(hs['status'])}")
                if 'created_at' in hs:
                    typer.echo(f"{print_field_label('Criado em')} {format_timestamp(hs['created_at'])}")
                if 'updated_at' in hs:
                    typer.echo(f"{print_field_label('Atualizado em')} {format_timestamp(hs['updated_at'])}")
            else:
                print_error("História não encontrada.")
        elif opt == "4":
            hs_id = typer.prompt("ID da história a editar")
            title = typer.prompt("Novo título", default="")
            description = typer.prompt("Nova descrição", default="")
            data = {}
            if title: data["title"] = title
            if description: data["description"] = description
            resp = requests.put(f"{API_URL}/user-stories/{hs_id}", json=data, headers=auth_headers())
            if resp.status_code == 200:
                print_success("História atualizada!")
            else:
                print_error(f"Erro: {resp.json().get('detail', resp.text)}")
        elif opt == "5":
            hs_id = typer.prompt("ID da história a remover")
            resp = requests.delete(f"{API_URL}/user-stories/{hs_id}", headers=auth_headers())
            if resp.status_code == 204:
                print_success("História removida!")
            else:
                print_error(f"Erro: {resp.json().get('detail', resp.text)}")
        elif opt == "6":
            hs_id = typer.prompt("ID da história")
            resp = requests.get(f"{API_URL}/products/stories/{hs_id}/revisions", headers=auth_headers())
            if resp.status_code == 200:
                revisions = resp.json()
                if revisions:
                    print_section_header(f"Histórico de revisões da história {hs_id}")
                    for rev in revisions:
                        typer.echo(f"{print_field_label('Campo')} {print_field_value(rev['field_changed'])}")
                        typer.echo(f"{print_field_label('Antes')} {print_muted(str(rev['old_value']))}")
                        typer.echo(f"{print_field_label('Depois')} {print_highlight(str(rev['new_value']))}")
                        typer.echo(f"{print_field_label('Data')} {format_timestamp(rev['changed_at'])}")
                        typer.echo(f"{print_field_label('Motivo')} {print_accent(str(rev['change_reason']))}")
                        print_separator()
                else:
                    print_info("Nenhuma revisão encontrada para esta história.")
            else:
                print_error("Erro ao obter histórico de revisões.")
        elif opt == "7":
            revisar_historias_menu()
        elif opt == "0":
            break
        else:
            print_warning("Opção inválida!")

def revisar_historias_menu():
    while True:
        print_menu_title("Revisão de Histórias de Usuário")
        print_menu_option("1", "Listar histórias de um épico")
        print_menu_option("2", "Visualizar detalhes e revisão de uma história")
        print_menu_option("3", "Editar história")
        print_menu_option("4", "Adicionar comentário/sugestão")
        print_menu_option("5", "Executar ação de revisão (aprovar, rejeitar, etc.)")
        print_menu_option("6", "Visualizar histórico de revisões da história")
        print_menu_option("0", "Voltar")
        opt = typer.prompt(">>> Opção : ")
        if opt == "1":
            eid = typer.prompt("ID do épico")
            resp = requests.get(f"{API_URL}/epics/{eid}/user-stories", headers=auth_headers())
            if resp.status_code == 200:
                for hs in resp.json():
                    typer.echo(f"ID: {hs['user_story_id']} | {hs['title']}\n  {hs['description']}")
            else:
                print_error("Erro ao listar histórias.")
        elif opt == "2":
            hs_id = typer.prompt("ID da história")
            resp = requests.get(f"{API_URL}/user-stories/{hs_id}", headers=auth_headers())
            if resp.status_code == 200:
                hs = resp.json()
                print_section_header("Detalhes da História")
                typer.echo(f"ID: {hs.get('user_story_id', 'N/A')}")
                typer.echo(f"Título: {hs.get('title', 'N/A')}")
                typer.echo(f"Descrição: {hs.get('description', 'N/A')}")
                # Status de revisão
                info = requests.get(f"{API_URL}/review/user_story/{hs_id}/info", headers=auth_headers())
                if info.status_code == 200:
                    i = info.json()
                    typer.echo(f"Status: {i['current_status']}")
                    typer.echo(f"Total de comentários: {i['total_comments']}")
                    typer.echo(f"Revisões pendentes: {i['pending_reviews']}")
                    if i['last_review_date']:
                        typer.echo(f"Última revisão: {i['last_review_date']} por {i['reviewed_by']}")
                # Comentários
                comments = requests.get(f"{API_URL}/review/comments/user_story/{hs_id}", headers=auth_headers())
                if comments.status_code == 200:
                    print_info("Comentários:")
                    for c in comments.json():
                        typer.echo(f"- {c['comment']} (Sugestão: {'Sim' if c['is_suggestion'] else 'Não'})")
                else:
                    print_info("Nenhum comentário.")
            else:
                print_error("História não encontrada.")
        elif opt == "3":
            hs_id = typer.prompt("ID da história a editar")
            title = typer.prompt("Novo título", default="")
            description = typer.prompt("Nova descrição", default="")
            data = {}
            if title: data["title"] = title
            if description: data["description"] = description
            resp = requests.put(f"{API_URL}/user-stories/{hs_id}", json=data, headers=auth_headers())
            if resp.status_code == 200:
                print_success("História atualizada!")
            else:
                print_error(f"Erro: {resp.json().get('detail', resp.text)}")
        elif opt == "4":
            hs_id = typer.prompt("ID da história")
            comment = typer.prompt("Comentário")
            is_suggestion = typer.confirm("É uma sugestão de melhoria?")
            suggested_changes = ""
            if is_suggestion:
                suggested_changes = typer.prompt("Sugestões específicas de mudanças")
            data = {
                "entity_type": "user_story",
                "entity_id": int(hs_id),
                "comment": comment,
                "is_suggestion": is_suggestion,
                "suggested_changes": suggested_changes
            }
            resp = requests.post(f"{API_URL}/review/comments", json=data, headers=auth_headers())
            if resp.status_code == 200:
                print_success("Comentário adicionado com sucesso!")
            else:
                print_error(f"Erro: {resp.json().get('detail', resp.text)}")
        elif opt == "5":
            hs_id = typer.prompt("ID da história")
            typer.echo("Ações disponíveis: 1-Aprovar, 2-Rejeitar, 3-Solicitar revisão, 4-Marcar como implementado")
            action_opt = typer.prompt("Escolha a ação")
            action_map = {
                "1": "approve",
                "2": "reject",
                "3": "request_revision",
                "4": "mark_implemented"
            }
            action = action_map.get(action_opt)
            if not action:
                print_warning("Ação inválida!")
                continue
            comment = typer.prompt("Comentário (opcional)", default="")
            reason = typer.prompt("Motivo (opcional)", default="")
            data = {
                "action": action,
                "comment": comment if comment else None,
                "reason": reason if reason else None
            }
            resp = requests.post(f"{API_URL}/review/user_story/{hs_id}/action", json=data, headers=auth_headers())
            if resp.status_code == 200:
                print_success(f"Ação '{action}' executada com sucesso!")
            else:
                print_error(f"Erro: {resp.json().get('detail', resp.text)}")
        elif opt == "6":
            hs_id = typer.prompt("ID da história")
            resp = requests.get(f"{API_URL}/products/stories/{hs_id}/revisions", headers=auth_headers())
            if resp.status_code == 200:
                revisions = resp.json()
                if revisions:
                    print_section_header(f"Histórico de revisões da história {hs_id}")
                    for rev in revisions:
                        typer.echo(f"{print_field_label('Campo')} {print_field_value(rev['field_changed'])}")
                        typer.echo(f"{print_field_label('Antes')} {print_muted(str(rev['old_value']))}")
                        typer.echo(f"{print_field_label('Depois')} {print_highlight(str(rev['new_value']))}")
                        typer.echo(f"{print_field_label('Data')} {format_timestamp(rev['changed_at'])}")
                        typer.echo(f"{print_field_label('Motivo')} {print_accent(str(rev['change_reason']))}")
                        print_separator()
                else:
                    print_info("Nenhuma revisão encontrada para esta história.")
            else:
                print_error("Erro ao obter histórico de revisões.")
        elif opt == "0":
            break
        else:
            print_warning("Opção inválida!")

# --- REQUISITOS FUNCIONAIS ---
def requisitos_menu():
    while True:
        print_menu_title("Requisitos Funcionais")
        print_menu_option("\t 1", "Listar requisitos de um produto")
        print_menu_option("\t 2", "Criar requisito para produto")
        print_menu_option("\t 3", "Visualizar requisito")
        print_menu_option("\t 4", "Editar requisito")
        print_menu_option("\t 5", "Remover requisito")
        print_menu_option("\t 6", "Visualizar histórico de revisões")
        print_menu_option("\t 7", "Gerar requisitos via LLM")
        print_menu_option("\t 8", "Revisar requisitos")
        print_menu_option("\t 0", "Voltar")
        opt = typer.prompt(">>> Opção : ")
        if opt == "1":
            pid = typer.prompt("ID do produto")
            resp = requests.get(f"{API_URL}/products/{pid}/requirements", headers=auth_headers())
            if resp.status_code == 200:
                for r in resp.json():
                    typer.echo(f"{format_id(str(r['requirement_id']))} | {format_name(r['title'])} | {format_description(r['description'])}")
            else:
                print_error("Erro ao listar requisitos.")
        elif opt == "2":
            pid = typer.prompt("ID do produto")
            title = typer.prompt("Título do requisito")
            description = typer.prompt("Descrição do requisito")
            data = {"title": title, "description": description}
            resp = requests.post(f"{API_URL}/products/{pid}/requirements", json=data, headers=auth_headers())
            if resp.status_code == 200 or resp.status_code == 201:
                print_success(f"Requisito criado: {resp.json()['title']} (ID: {resp.json()['requirement_id']})")
            else:
                print_error(f"Erro: {resp.json().get('detail', resp.text)}")
        elif opt == "3":
            rid = typer.prompt("ID do requisito")
            resp = requests.get(f"{API_URL}/requirements/{rid}", headers=auth_headers())
            if resp.status_code == 200:
                r = resp.json()
                print_section_header("Detalhes do Requisito")
                typer.echo(f"{format_id(str(r.get('requirement_id', 'N/A')))}")
                typer.echo(f"{format_name(r.get('title', 'N/A'))}")
                typer.echo(f"{format_description(r.get('description', 'N/A'))}")
                if 'status' in r:
                    typer.echo(f"{print_field_label('Status')} {format_status(r['status'])}")
                if 'created_at' in r:
                    typer.echo(f"{print_field_label('Criado em')} {format_timestamp(r['created_at'])}")
                if 'updated_at' in r:
                    typer.echo(f"{print_field_label('Atualizado em')} {format_timestamp(r['updated_at'])}")
            else:
                print_error("Requisito não encontrado.")
        elif opt == "4":
            rid = typer.prompt("ID do requisito a editar")
            title = typer.prompt("Novo título", default="")
            description = typer.prompt("Nova descrição", default="")
            data = {}
            if title: data["title"] = title
            if description: data["description"] = description
            resp = requests.put(f"{API_URL}/requirements/{rid}", json=data, headers=auth_headers())
            if resp.status_code == 200:
                print_success("Requisito atualizado!")
            else:
                print_error(f"Erro: {resp.json().get('detail', resp.text)}")
        elif opt == "5":
            rid = typer.prompt("ID do requisito a remover")
            resp = requests.delete(f"{API_URL}/requirements/{rid}", headers=auth_headers())
            if resp.status_code == 204:
                print_success("Requisito removido!")
            else:
                print_error(f"Erro: {resp.json().get('detail', resp.text)}")
        elif opt == "6":
            rid = typer.prompt("ID do requisito")
            resp = requests.get(f"{API_URL}/products/requirements/{rid}/revisions", headers=auth_headers())
            if resp.status_code == 200:
                revisions = resp.json()
                if revisions:
                    print_section_header(f"Histórico de revisões do requisito {rid}")
                    for rev in revisions:
                        typer.echo(f"{print_field_label('Campo')} {print_field_value(rev['field_changed'])}")
                        typer.echo(f"{print_field_label('Antes')} {print_muted(str(rev['old_value']))}")
                        typer.echo(f"{print_field_label('Depois')} {print_highlight(str(rev['new_value']))}")
                        typer.echo(f"{print_field_label('Data')} {format_timestamp(rev['changed_at'])}")
                        typer.echo(f"{print_field_label('Motivo')} {print_accent(str(rev['change_reason']))}")
                        print_separator()
                else:
                    print_info("Nenhuma revisão encontrada para este requisito.")
            else:
                print_error("Erro ao obter histórico de revisões.")
        elif opt == "7":
            print_section_header("Geração de Requisitos Funcionais via LLM")
            product_id = typer.prompt("ID do produto para gerar requisitos")
            custom_prompt = typer.prompt("Prompt customizado (opcional)", default="")
            data = {
                "product_id": int(product_id),
                "userPromptAdjustment": custom_prompt if custom_prompt else None
            }
            resp = requests.post(f"{API_URL}/llm-project/generate-requirements", json=data, headers=auth_headers())
            if resp.status_code == 200:
                result = resp.json()
                print_success("Requisitos funcionais gerados e salvos com sucesso!")
                for req in result["content"]:
                    typer.echo(f"ID: {req['requirement_id']} | Prioridade: {req['priority']}\n  {req['description']}")
            else:
                print_error(f"Erro: {resp.json().get('detail', resp.text)}")
        elif opt == "8":
            revisar_requisitos_menu()
        elif opt == "0":
            break
        else:
            print_warning("Opção inválida!")

def revisar_requisitos_menu():
    while True:
        print_menu_title("Revisão de Requisitos Funcionais")
        print_menu_option("1", "Listar requisitos de uma história")
        print_menu_option("2", "Visualizar detalhes e revisão de um requisito")
        print_menu_option("3", "Editar requisito")
        print_menu_option("4", "Adicionar comentário/sugestão")
        print_menu_option("5", "Executar ação de revisão (aprovar, rejeitar, etc.)")
        print_menu_option("6", "Visualizar histórico de revisões do requisito")
        print_menu_option("0", "Voltar")
        opt = typer.prompt(">>> Opção : ")
        if opt == "1":
            hs_id = typer.prompt("ID da história de usuário")
            resp = requests.get(f"{API_URL}/stories/{hs_id}/requirements", headers=auth_headers())
            if resp.status_code == 200:
                for req in resp.json():
                    typer.echo(f"ID: {req['requirement_id']} | Prioridade: {req.get('priority', 'N/A')}\n  {req['description']}")
            else:
                print_error("Erro ao listar requisitos.")
        elif opt == "2":
            req_id = typer.prompt("ID do requisito")
            resp = requests.get(f"{API_URL}/requirements/{req_id}", headers=auth_headers())
            if resp.status_code == 200:
                req = resp.json()
                print_section_header("Detalhes do Requisito")
                typer.echo(f"ID: {req.get('requirement_id', 'N/A')}")
                typer.echo(f"Descrição: {req.get('description', 'N/A')}")
                typer.echo(f"Prioridade: {req.get('priority', 'N/A')}")
                # Status de revisão
                info = requests.get(f"{API_URL}/review/requirement/{req_id}/info", headers=auth_headers())
                if info.status_code == 200:
                    i = info.json()
                    typer.echo(f"Status: {i['current_status']}")
                    typer.echo(f"Total de comentários: {i['total_comments']}")
                    typer.echo(f"Revisões pendentes: {i['pending_reviews']}")
                    if i['last_review_date']:
                        typer.echo(f"Última revisão: {i['last_review_date']} por {i['reviewed_by']}")
                # Comentários
                comments = requests.get(f"{API_URL}/review/comments/requirement/{req_id}", headers=auth_headers())
                if comments.status_code == 200:
                    print_info("Comentários:")
                    for c in comments.json():
                        typer.echo(f"- {c['comment']} (Sugestão: {'Sim' if c['is_suggestion'] else 'Não'})")
                else:
                    print_info("Nenhum comentário.")
            else:
                print_error("Requisito não encontrado.")
        elif opt == "3":
            req_id = typer.prompt("ID do requisito a editar")
            description = typer.prompt("Nova descrição", default="")
            priority = typer.prompt("Nova prioridade (Alta/Média/Baixa)", default="")
            data = {}
            if description: data["description"] = description
            if priority: data["priority"] = priority
            resp = requests.put(f"{API_URL}/requirements/{req_id}", json=data, headers=auth_headers())
            if resp.status_code == 200:
                print_success("Requisito atualizado!")
            else:
                print_error(f"Erro: {resp.json().get('detail', resp.text)}")
        elif opt == "4":
            req_id = typer.prompt("ID do requisito")
            comment = typer.prompt("Comentário")
            is_suggestion = typer.confirm("É uma sugestão de melhoria?")
            suggested_changes = ""
            if is_suggestion:
                suggested_changes = typer.prompt("Sugestões específicas de mudanças")
            data = {
                "entity_type": "requirement",
                "entity_id": int(req_id),
                "comment": comment,
                "is_suggestion": is_suggestion,
                "suggested_changes": suggested_changes
            }
            resp = requests.post(f"{API_URL}/review/comments", json=data, headers=auth_headers())
            if resp.status_code == 200:
                print_success("Comentário adicionado com sucesso!")
            else:
                print_error(f"Erro: {resp.json().get('detail', resp.text)}")
        elif opt == "5":
            req_id = typer.prompt("ID do requisito")
            typer.echo("Ações disponíveis: 1-Aprovar, 2-Rejeitar, 3-Solicitar revisão, 4-Marcar como implementado")
            action_opt = typer.prompt("Escolha a ação")
            action_map = {
                "1": "approve",
                "2": "reject",
                "3": "request_revision",
                "4": "mark_implemented"
            }
            action = action_map.get(action_opt)
            if not action:
                print_warning("Ação inválida!")
                continue
            comment = typer.prompt("Comentário (opcional)", default="")
            reason = typer.prompt("Motivo (opcional)", default="")
            data = {
                "action": action,
                "comment": comment if comment else None,
                "reason": reason if reason else None
            }
            resp = requests.post(f"{API_URL}/review/requirement/{req_id}/action", json=data, headers=auth_headers())
            if resp.status_code == 200:
                print_success(f"Ação '{action}' executada com sucesso!")
            else:
                print_error(f"Erro: {resp.json().get('detail', resp.text)}")
        elif opt == "6":
            req_id = typer.prompt("ID do requisito")
            resp = requests.get(f"{API_URL}/products/requirements/{req_id}/revisions", headers=auth_headers())
            if resp.status_code == 200:
                revisions = resp.json()
                if revisions:
                    print_section_header(f"Histórico de revisões do requisito {req_id}")
                    for rev in revisions:
                        typer.echo(f"{print_field_label('Campo')} {print_field_value(rev['field_changed'])}")
                        typer.echo(f"{print_field_label('Antes')} {print_muted(str(rev['old_value']))}")
                        typer.echo(f"{print_field_label('Depois')} {print_highlight(str(rev['new_value']))}")
                        typer.echo(f"{print_field_label('Data')} {format_timestamp(rev['changed_at'])}")
                        typer.echo(f"{print_field_label('Motivo')} {print_accent(str(rev['change_reason']))}")
                        print_separator()
                else:
                    print_info("Nenhuma revisão encontrada para este requisito.")
            else:
                print_error("Erro ao obter histórico de revisões.")
        elif opt == "0":
            break
        else:
            print_warning("Opção inválida!")

# --- BACKLOGS ---
def backlogs_menu():
    while True:
        print_menu_title("Backlogs")
        print_menu_option("\t 1", "Listar backlogs de um produto")
        print_menu_option("\t 2", "Criar backlog para produto")
        print_menu_option("\t 3", "Visualizar backlog")
        print_menu_option("\t 4", "Editar backlog")
        print_menu_option("\t 5", "Remover backlog")
        print_menu_option("\t 6", "Gerar backlog automaticamente")
        print_menu_option("\t 7", "Preview de geração de backlog")
        print_menu_option("\t 8", "Ver itens aprovados")
        print_menu_option("\t 9", "Revisar backlogs gerados")
        print_menu_option("\t 0", "Voltar")
        opt = typer.prompt(">>> Opção : ")
        if opt == "1":
            pid = typer.prompt("ID do produto")
            resp = requests.get(f"{API_URL}/products/{pid}/backlogs", headers=auth_headers())
            if resp.status_code == 200:
                for b in resp.json():
                    typer.echo(f"{format_id(str(b['backlog_id']))} | {format_name(b['name'])} | {format_description(b['description'])}")
            else:
                print_error("Erro ao listar backlogs.")
        elif opt == "2":
            pid = typer.prompt("ID do produto")
            name = typer.prompt("Nome do backlog")
            description = typer.prompt("Descrição do backlog")
            version = typer.prompt("Versão do backlog")
            data = {"product_id": int(pid), "name": name, "description": description, "version": version}
            resp = requests.post(f"{API_URL}/products/{pid}/backlogs", json=data, headers=auth_headers())
            if resp.status_code == 200 or resp.status_code == 201:
                print_success(f"Backlog criado: {resp.json()['name']} (ID: {resp.json()['backlog_id']})")
            else:
                print_error(f"Erro: {resp.json().get('detail', resp.text)}")
        elif opt == "3":
            bid = typer.prompt("ID do backlog")
            resp = requests.get(f"{API_URL}/backlogs/{bid}", headers=auth_headers())
            if resp.status_code == 200:
                b = resp.json()
                print_section_header("Detalhes do Backlog")
                typer.echo(f"{format_id(str(b.get('backlog_id', 'N/A')))}")
                typer.echo(f"{format_name(b.get('name', 'N/A'))}")
                typer.echo(f"{format_description(b.get('description', 'N/A'))}")
                if 'version' in b:
                    typer.echo(f"{print_field_label('Versão')} {print_field_value(b['version'])}")
                if 'created_at' in b:
                    typer.echo(f"{print_field_label('Criado em')} {format_timestamp(b['created_at'])}")
                if 'updated_at' in b:
                    typer.echo(f"{print_field_label('Atualizado em')} {format_timestamp(b['updated_at'])}")
            else:
                print_error("Backlog não encontrado.")
        elif opt == "4":
            bid = typer.prompt("ID do backlog a editar")
            name = typer.prompt("Novo nome", default="")
            description = typer.prompt("Nova descrição", default="")
            version = typer.prompt("Nova versão", default="")
            data = {}
            if name: data["name"] = name
            if description: data["description"] = description
            if version: data["version"] = version
            resp = requests.put(f"{API_URL}/backlogs/{bid}", json=data, headers=auth_headers())
            if resp.status_code == 200:
                print_success("Backlog atualizado!")
            else:
                print_error(f"Erro: {resp.json().get('detail', resp.text)}")
        elif opt == "5":
            bid = typer.prompt("ID do backlog a remover")
            resp = requests.delete(f"{API_URL}/backlogs/{bid}", headers=auth_headers())
            if resp.status_code == 204:
                print_success("Backlog removido!")
            else:
                print_error(f"Erro: {resp.json().get('detail', resp.text)}")
        elif opt == "6":
            typer.echo("\n--- Geração Automática de Backlog ---")
            pid = typer.prompt("ID do produto")
            name = typer.prompt("Nome do backlog")
            description = typer.prompt("Descrição (opcional)", default="")
            
            # Verificar se há itens aprovados
            resp = requests.get(f"{API_URL}/backlog-generation/products/{pid}/approved-items", headers=auth_headers())
            if resp.status_code == 200:
                items_info = resp.json()
                print_info(f"Histórias aprovadas: {items_info['approved_stories']}")
                print_info(f"Requisitos aprovados: {items_info['approved_requirements']}")
                
                if not items_info['can_generate_backlog']:
                    print_warning("Não há itens aprovados suficientes para gerar um backlog.")
                    continue
            
            # Estratégias disponíveis
            resp = requests.get(f"{API_URL}/backlog-generation/strategies", headers=auth_headers())
            if resp.status_code == 200:
                strategies = resp.json()['strategies']
                print_info("\nEstratégias disponíveis:")
                for i, strategy in enumerate(strategies, 1):
                    print_info(f"{i} - {strategy['name']}: {strategy['description']}")
                
                strategy_choice = typer.prompt("Escolha a estratégia (1-5)", default="1")
                strategy_map = {
                    "1": "priority_based",
                    "2": "epic_based", 
                    "3": "story_only",
                    "4": "requirement_only",
                    "5": "mixed"
                }
                strategy = strategy_map.get(strategy_choice, "priority_based")
            
            # Gerar backlog
            data = {
                "product_id": int(pid),
                "name": name,
                "description": description if description else None,
                "strategy": strategy,
                "include_stories": True,
                "include_requirements": True,
                "min_priority": 3,
                "auto_prioritize": True
            }
            
            resp = requests.post(f"{API_URL}/backlog-generation/generate", json=data, headers=auth_headers())
            if resp.status_code == 200:
                result = resp.json()
                print_success(f"\nBacklog gerado com sucesso!")
                print_info(f"ID do backlog: {result['backlog_id']}")
                print_info(f"Total de itens: {result['total_items']}")
                print_info(f"Histórias: {result['stories_count']}")
                print_info(f"Requisitos: {result['requirements_count']}")
                print_info(f"Estratégia: {result['generation_strategy']}")
            else:
                print_error(f"Erro: {resp.json().get('detail', resp.text)}")
        
        elif opt == "7":
            typer.echo("\n--- Preview de Geração de Backlog ---")
            pid = typer.prompt("ID do produto")
            name = typer.prompt("Nome do backlog")
            description = typer.prompt("Descrição (opcional)", default="")
            
            # Estratégias disponíveis
            resp = requests.get(f"{API_URL}/backlog-generation/strategies", headers=auth_headers())
            if resp.status_code == 200:
                strategies = resp.json()['strategies']
                print_info("\nEstratégias disponíveis:")
                for i, strategy in enumerate(strategies, 1):
                    print_info(f"{i} - {strategy['name']}: {strategy['description']}")
                
                strategy_choice = typer.prompt("Escolha a estratégia (1-5)", default="1")
                strategy_map = {
                    "1": "priority_based",
                    "2": "epic_based", 
                    "3": "story_only",
                    "4": "requirement_only",
                    "5": "mixed"
                }
                strategy = strategy_map.get(strategy_choice, "priority_based")
            
            # Gerar preview
            data = {
                "product_id": int(pid),
                "name": name,
                "description": description if description else None,
                "strategy": strategy,
                "include_stories": True,
                "include_requirements": True,
                "min_priority": 3,
                "auto_prioritize": True
            }
            
            resp = requests.post(f"{API_URL}/backlog-generation/preview", json=data, headers=auth_headers())
            if resp.status_code == 200:
                preview = resp.json()
                print_success(f"\nPreview da geração:")
                print_info(f"Total estimado: {preview['estimated_items']} itens")
                print_info(f"Histórias estimadas: {preview['estimated_stories']}")
                print_info(f"Requisitos estimados: {preview['estimated_requirements']}")
                print_info(f"Estratégia: {preview['strategy']}")
                
                print_info("\nPrimeiros 10 itens que seriam incluídos:")
                for i, item in enumerate(preview['preview_items'], 1):
                    print_info(f"{i}. [{item['item_type'].upper()}] {item['title']}")
                    print_info(f"   Prioridade: {item['priority']} | Épico: {item['epic_title'] or 'N/A'}")
            else:
                print_error(f"Erro: {resp.json().get('detail', resp.text)}")
        
        elif opt == "8":
            print_info("\n--- Itens Aprovados ---")
            pid = typer.prompt("ID do produto")
            
            # Ver itens aprovados
            resp = requests.get(f"{API_URL}/backlog-generation/products/{pid}/approved-items", headers=auth_headers())
            if resp.status_code == 200:
                items_info = resp.json()
                print_info(f"Histórias aprovadas: {items_info['approved_stories']}")
                print_info(f"Requisitos aprovados: {items_info['approved_requirements']}")
                print_info(f"Total: {items_info['total_approved_items']}")
                print_info(f"Pode gerar backlog: {'Sim' if items_info['can_generate_backlog'] else 'Não'}")
            
            # Ver resumo por épicos
            resp = requests.get(f"{API_URL}/backlog-generation/products/{pid}/epics-summary", headers=auth_headers())
            if resp.status_code == 200:
                summary = resp.json()
                print_info(f"\nResumo por épicos:")
                print_info(f"Total de épicos: {summary['total_epics']}")
                print_info(f"Épicos com itens aprovados: {summary['epics_with_approved_items']}")
                
                for epic in summary['epics_summary']:
                    if epic['total_approved_items'] > 0:
                        print_info(f"\nÉpico: {epic['epic_title']} (ID: {epic['epic_id']})")
                        print_info(f"  Status: {epic['epic_status']}")
                        print_info(f"  Histórias aprovadas: {epic['approved_stories']}")
                        print_info(f"  Requisitos aprovados: {epic['approved_requirements']}")
                        print_info(f"  Total: {epic['total_approved_items']}")
            else:
                print_error(f"Erro: {resp.json().get('detail', resp.text)}")
        
        elif opt == "9":
            revisar_backlogs_menu()
        
        elif opt == "0":
            break
        else:
            print_warning("Opção inválida!")

# --- ITENS DE BACKLOG ---
def itens_backlog_menu():
    while True:
        print_menu_title("Itens de Backlog")
        print_menu_option("\t 1", "Listar itens de um backlog")
        print_menu_option("\t 2", "Criar item para backlog")
        print_menu_option("\t 3", "Visualizar item")
        print_menu_option("\t 4", "Editar item")
        print_menu_option("\t 5", "Remover item")
        print_menu_option("\t 0", "Voltar")
        opt = typer.prompt(">>> Opção : ")
        if opt == "1":
            bid = typer.prompt("ID do backlog")
            resp = requests.get(f"{API_URL}/backlogs/{bid}/items", headers=auth_headers())
            if resp.status_code == 200:
                for i in resp.json():
                    typer.echo(f"{format_id(str(i['item_id']))} | {format_name(i['title'])} | {format_description(i['description'])}")
            else:
                print_error("Erro ao listar itens.")
        elif opt == "2":
            bid = typer.prompt("ID do backlog")
            title = typer.prompt("Título do item")
            description = typer.prompt("Descrição do item")
            data = {"title": title, "description": description}
            resp = requests.post(f"{API_URL}/backlogs/{bid}/items", json=data, headers=auth_headers())
            if resp.status_code == 200 or resp.status_code == 201:
                print_success(f"Item criado: {resp.json()['title']} (ID: {resp.json()['item_id']})")
            else:
                print_error(f"Erro: {resp.json().get('detail', resp.text)}")
        elif opt == "3":
            iid = typer.prompt("ID do item")
            resp = requests.get(f"{API_URL}/backlog-items/{iid}", headers=auth_headers())
            if resp.status_code == 200:
                i = resp.json()
                print_section_header("Detalhes do Item")
                typer.echo(f"{format_id(str(i.get('item_id', 'N/A')))}")
                typer.echo(f"{format_name(i.get('title', 'N/A'))}")
                typer.echo(f"{format_description(i.get('description', 'N/A'))}")
                if 'status' in i:
                    typer.echo(f"{print_field_label('Status')} {format_status(i['status'])}")
                if 'created_at' in i:
                    typer.echo(f"{print_field_label('Criado em')} {format_timestamp(i['created_at'])}")
                if 'updated_at' in i:
                    typer.echo(f"{print_field_label('Atualizado em')} {format_timestamp(i['updated_at'])}")
            else:
                print_error("Item não encontrado.")
        elif opt == "4":
            iid = typer.prompt("ID do item a editar")
            title = typer.prompt("Novo título", default="")
            description = typer.prompt("Nova descrição", default="")
            data = {}
            if title: data["title"] = title
            if description: data["description"] = description
            resp = requests.put(f"{API_URL}/backlog-items/{iid}", json=data, headers=auth_headers())
            if resp.status_code == 200:
                print_success("Item atualizado!")
            else:
                print_error(f"Erro: {resp.json().get('detail', resp.text)}")
        elif opt == "5":
            iid = typer.prompt("ID do item a remover")
            resp = requests.delete(f"{API_URL}/backlog-items/{iid}", headers=auth_headers())
            if resp.status_code == 204:
                print_success("Item removido!")
            else:
                print_error(f"Erro: {resp.json().get('detail', resp.text)}")
        elif opt == "0":
            break
        else:
            print_warning("Opção inválida!")

# --- REVISÃO DE BACKLOGS ---
def revisar_backlogs_menu():
    while True:
        print_menu_title("Revisão de Backlogs")
        print_menu_option("1", "Listar backlogs de um produto")
        print_menu_option("2", "Visualizar detalhes e itens de um backlog")
        print_menu_option("3", "Adicionar comentário/sugestão")
        print_menu_option("4", "Executar ação de revisão (aprovar, rejeitar, etc.)")
        print_menu_option("5", "Visualizar histórico de revisões do backlog")
        print_menu_option("0", "Voltar")
        opt = typer.prompt(">>> Opção : ")
        if opt == "1":
            pid = typer.prompt("ID do produto")
            resp = requests.get(f"{API_URL}/products/{pid}/backlogs", headers=auth_headers())
            if resp.status_code == 200:
                for b in resp.json():
                    typer.echo(f"ID: {b['backlog_id']} | {b['name']}\n  {b['description']}")
            else:
                print_error("Erro ao listar backlogs.")
        elif opt == "2":
            bid = typer.prompt("ID do backlog")
            resp = requests.get(f"{API_URL}/backlogs/{bid}", headers=auth_headers())
            if resp.status_code == 200:
                b = resp.json()
                print_section_header("Detalhes do Backlog")
                typer.echo(f"ID: {b.get('backlog_id', 'N/A')}")
                typer.echo(f"Nome: {b.get('name', 'N/A')}")
                typer.echo(f"Descrição: {b.get('description', 'N/A')}")
                typer.echo(f"Versão: {b.get('version', 'N/A')}")
                # Listar itens do backlog
                items = requests.get(f"{API_URL}/backlogs/{bid}/items", headers=auth_headers())
                if items.status_code == 200:
                    print_info("Itens do backlog:")
                    for i in items.json():
                        typer.echo(f"- {i['title']} | {i['description']} | Status: {i.get('status', 'N/A')}")
                else:
                    print_info("Nenhum item encontrado.")
            else:
                print_error("Backlog não encontrado.")
        elif opt == "3":
            bid = typer.prompt("ID do backlog")
            comment = typer.prompt("Comentário")
            is_suggestion = typer.confirm("É uma sugestão de melhoria?")
            suggested_changes = ""
            if is_suggestion:
                suggested_changes = typer.prompt("Sugestões específicas de mudanças")
            data = {
                "entity_type": "backlog",
                "entity_id": int(bid),
                "comment": comment,
                "is_suggestion": is_suggestion,
                "suggested_changes": suggested_changes
            }
            resp = requests.post(f"{API_URL}/review/comments", json=data, headers=auth_headers())
            if resp.status_code == 200:
                print_success("Comentário adicionado com sucesso!")
            else:
                print_error(f"Erro: {resp.json().get('detail', resp.text)}")
        elif opt == "4":
            bid = typer.prompt("ID do backlog")
            typer.echo("Ações disponíveis: 1-Aprovar, 2-Rejeitar, 3-Solicitar revisão, 4-Marcar como implementado")
            action_opt = typer.prompt("Escolha a ação")
            action_map = {
                "1": "approve",
                "2": "reject",
                "3": "request_revision",
                "4": "mark_implemented"
            }
            action = action_map.get(action_opt)
            if not action:
                print_warning("Ação inválida!")
                continue
            comment = typer.prompt("Comentário (opcional)", default="")
            reason = typer.prompt("Motivo (opcional)", default="")
            data = {
                "action": action,
                "comment": comment if comment else None,
                "reason": reason if reason else None
            }
            resp = requests.post(f"{API_URL}/review/backlog/{bid}/action", json=data, headers=auth_headers())
            if resp.status_code == 200:
                print_success(f"Ação '{action}' executada com sucesso!")
            else:
                print_error(f"Erro: {resp.json().get('detail', resp.text)}")
        elif opt == "5":
            bid = typer.prompt("ID do backlog")
            resp = requests.get(f"{API_URL}/products/backlogs/{bid}/revisions", headers=auth_headers())
            if resp.status_code == 200:
                revisions = resp.json()
                if revisions:
                    print_section_header(f"Histórico de revisões do backlog {bid}")
                    for rev in revisions:
                        typer.echo(f"{print_field_label('Campo')} {print_field_value(rev['field_changed'])}")
                        typer.echo(f"{print_field_label('Antes')} {print_muted(str(rev['old_value']))}")
                        typer.echo(f"{print_field_label('Depois')} {print_highlight(str(rev['new_value']))}")
                        typer.echo(f"{print_field_label('Data')} {format_timestamp(rev['changed_at'])}")
                        typer.echo(f"{print_field_label('Motivo')} {print_accent(str(rev['change_reason']))}")
                        print_separator()
                else:
                    print_info("Nenhuma revisão encontrada para este backlog.")
            else:
                print_error("Erro ao obter histórico de revisões.")
        elif opt == "0":
            break
        else:
            print_warning("Opção inválida!")

# --- GERAÇÃO VIA LLM ---
def llm_menu():
    while True:
        print_menu_title("Geração via LLM")
        print_menu_option("\t 1", "Gerar épicos para um produto")
        print_menu_option("\t 2", "Gerar histórias de usuário")
        print_menu_option("\t 3", "Gerar requisitos")
        print_menu_option("\t 0", "Voltar")
        opt = typer.prompt(">>> Opção : ")
        if opt == "1":
            print_section_header("Geração de Épicos via LLM")
            product_id = typer.prompt("ID do produto para gerar épicos")
            product_info = typer.prompt("Informações do produto (JSON ou texto descritivo)")
            custom_prompt = typer.prompt("Prompt customizado (opcional)", default="")
            data = {
                "product_id": int(product_id),
                "productInfo": product_info,
                "userPromptAdjustment": custom_prompt if custom_prompt else None
            }
            resp = requests.post(f"{API_URL}/llm-project/generate-epics", json=data, headers=auth_headers())
            if resp.status_code == 200:
                result = resp.json()
                print_success("Épicos gerados e salvos com sucesso!")
                for epic in result["content"]:
                    typer.echo(f"ID: {epic['epic_id']} | {epic['title']}\n  {epic['description']}")
            else:
                print_error(f"Erro: {resp.json().get('detail', resp.text)}")
        
        elif opt == "2":
            print_section_header("Geração de Histórias de Usuário via LLM")
            product_id = typer.prompt("ID do produto para gerar histórias")
            epic_ids_str = typer.prompt("IDs dos épicos para gerar histórias (separe por vírgula)", default="")
            epic_ids = [int(e.strip()) for e in epic_ids_str.split(",") if e.strip()] if epic_ids_str else None
            product_info = typer.prompt("Informações do produto (JSON ou texto descritivo)")
            custom_prompt = typer.prompt("Prompt customizado (opcional)", default="")
            data = {
                "product_id": int(product_id),
                "epic_ids": epic_ids,
                "productInfo": product_info,
                "userPromptAdjustment": custom_prompt if custom_prompt else None
            }
            resp = requests.post(f"{API_URL}/llm-project/generate-user-stories", json=data, headers=auth_headers())
            if resp.status_code == 200:
                result = resp.json()
                print_success("Histórias de usuário geradas e salvas com sucesso!")
                for story in result["content"]:
                    typer.echo(f"ID: {story['user_story_id']} | {story['title']}\n  {story['description']}")
            else:
                print_error(f"Erro: {resp.json().get('detail', resp.text)}")
        
        elif opt == "3":
            print_section_header("Geração de Requisitos via LLM")
            stories_info = typer.prompt("Informações das histórias de usuário (JSON ou texto descritivo)")
            custom_prompt = typer.prompt("Prompt customizado (opcional)", default="")
            
            data = {
                "prompt": stories_info,
                "custom_prompt": custom_prompt if custom_prompt else None
            }
            
            resp = requests.post(f"{API_URL}/llm-project/generate-requirements", json=data, headers=auth_headers())
            if resp.status_code == 200:
                result = resp.json()
                print_success("Requisitos gerados com sucesso!")
                print_info(f"Resposta: {result['response']}")
                print_info(f"Tokens utilizados: {result.get('tokens_used', 'N/A')}")
            else:
                print_error(f"Erro: {resp.json().get('detail', resp.text)}")
        
        elif opt == "0":
            break
        else:
            print_warning("Opção inválida!")

@app.command()
def menu():
    while True:
        print_header("SISTEMA DE GERENCIAMENTO DE HISTÓRIAS")
        print_menu_option("\t 1", "Produtos")
        print_menu_option("\t 2", "Épicos")
        print_menu_option("\t 3", "Histórias de usuário")
        print_menu_option("\t 4", "Requisitos")
        print_menu_option("\t 5", "Backlogs")
        print_menu_option("\t 6", "Itens de backlog")
        print_menu_option("\t 7", "Geração via LLM")
        print_menu_option("\t 0", "Sair")
        opt = typer.prompt(">>> Opção : ")
        if opt == "1":
            produtos_menu()
        elif opt == "2":
            epicos_menu()
        elif opt == "3":
            historias_menu()
        elif opt == "4":
            requisitos_menu()
        elif opt == "5":
            backlogs_menu()
        elif opt == "6":
            itens_backlog_menu()
        elif opt == "7":
            llm_menu()
        elif opt == "0":
            print_info("Saindo...")
            sys.exit(0)
        else:
            print_error("Opção inválida!")

if __name__ == "__main__":
    app() 
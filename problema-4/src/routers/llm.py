from fastapi import APIRouter, HTTPException, status, Depends
from src.schemas.llm import LLMRequest, LLMResponse
from src.utils.LLM import LLM
from aspects.logging import logging_aspect
from aspects.error_handling import handle_errors
from aspects.notification import notification_aspect
from aspects.LLM import generate_epics_with_llm, log_llm_interaction
from sqlalchemy.orm import Session
from src.db.session import get_db
from src.routers.auth import get_current_user
from src.db.models import Epic, UserStory, Requirement
from src.schemas.epic import EpicCreate, EpicInDB
from src.schemas.story import UserStoryCreate, UserStoryInDB
from src.schemas.requirement import RequirementCreate, RequirementInDB
from src.schemas.review import ReviewStatus

router = APIRouter(
    prefix="/llm-project",
    tags=["llm"],
    responses={
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Erro interno do servidor"}
    }
)

@router.post("/generate-epics", response_model=LLMResponse)
@handle_errors
@logging_aspect
@notification_aspect
async def generate_epics(request: LLMRequest, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    """
    Gera épicos baseados nas informações do produto, salva no banco e retorna os épicos persistidos.
    """
    try:
        # prompt = f"""
        # Com base nas seguintes informações do produto, gere uma lista detalhada de épicos:
        
        # {request.productInfo}
        
        # {request.userPromptAdjustment or ''}
        
        # Por favor, gere épicos bem estruturados e organizados.
        # """
        
        # # Usar a função LLM real
        # LLM(prompt)
        
        # # Por enquanto, retornar um exemplo estruturado
        # content = f"""Épico 1: Definição da Arquitetura do Sistema
        #     Descrição: Estabelecer a arquitetura técnica base do sistema, incluindo escolha de tecnologias, padrões de design e estrutura de dados.

        #     Épico 2: Implementação do Sistema de Autenticação
        #     Descrição: Desenvolver sistema completo de autenticação e autorização de usuários com diferentes níveis de acesso.

        #     Épico 3: Interface do Usuário Principal
        #     Descrição: Criar interface principal do sistema com navegação intuitiva e responsiva para diferentes dispositivos.

        #     Épico 4: Sistema de Geração de Conteúdo
        #     Descrição: Implementar funcionalidades de geração automática de conteúdo usando IA e LLMs.

        #     Épico 5: Gestão de Projetos e Backlog
        #     Descrição: Desenvolver sistema completo de gestão de projetos, épicos, histórias e backlog."""
                    
        #     content=content,
        #     detail=f"Erro ao gerar épicos: {str(e)}"
        #     logging.error(f"Erro ao gerar épicos: {str(e)}")
        #     detail=f"Erro ao gerar épicos: {str(e)}"


        # product_id deve ser enviado no request (ajuste o schema se necessário)
        product_id = getattr(request, 'product_id', None)
        if not product_id:
            raise HTTPException(status_code=400, detail="product_id é obrigatório")
        # Monta dicionário com as informações do produto
        product_info = {
            'nome': request.productInfo,
            'descricao': request.productInfo,  # ou ajuste para pegar campos separados se o frontend enviar
            'personas': [],  # Se vier no request, adicione aqui
            'proposta_valor': request.userPromptAdjustment or "",
            # Adicione outros campos se necessário
        }
        epics = generate_epics_with_llm(product_info)
        # Salvar cada épico no banco
        persisted_epics = []
        for e in epics:
            epic_create = EpicCreate(title=e.title, description=e.description)
            new_epic = Epic(
                title=epic_create.title,
                description=epic_create.description,
                product_id=product_id,
                created_by=current_user.user_id
            )
            db.add(new_epic)
            db.commit()
            db.refresh(new_epic)
            persisted_epics.append({
                "epic_id": new_epic.epic_id,
                "title": new_epic.title,
                "description": new_epic.description,
                "product_id": new_epic.product_id
            })
        # LOG LLM INTERACTION
        log_llm_interaction(
            db=db,
            user_id=current_user.user_id,
            product_id=product_id,
            prompt=str(product_info),
            response=str(persisted_epics),
            model_used="llama3-8b-8192",
            tokens_used=None,
            entity_type="epic",
            entity_id=None
        )
        return LLMResponse(
            content=persisted_epics,
            success=True,
            message="Épicos gerados e salvos com sucesso"
        )
    except Exception as e:
        logging.error(f"Erro ao gerar/salvar épicos: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao gerar/salvar épicos: {str(e)}"
        )

@router.post("/generate-user-stories", response_model=LLMResponse)
@handle_errors
@logging_aspect
@notification_aspect
async def generate_user_stories(request: LLMRequest, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    """
    Gera histórias de usuário baseadas nos épicos, salva no banco e retorna as histórias persistidas.
    """
    try:
        product_id = getattr(request, 'product_id', None)
        epic_ids = getattr(request, 'epic_ids', None)  # lista de épicos, se vier
        if not product_id:
            raise HTTPException(status_code=400, detail="product_id é obrigatório")

        # Usar a função LLM real
        LLM(prompt)
        
        # # Por enquanto, retornar um exemplo estruturado
        # content = f"""Como Product Owner, eu quero definir épicos claros para que a equipe tenha visão macro do projeto.

        #     Como Desenvolvedor, eu quero acessar especificações técnicas detalhadas para que possa implementar funcionalidades corretamente.

        #     Como Scrum Master, eu quero visualizar o backlog organizado para que possa facilitar o planejamento das sprints.

        #     Como QA Tester, eu quero critérios de aceitação claros para que possa criar testes efetivos.

        #     Como Stakeholder, eu quero acompanhar o progresso do projeto para que possa tomar decisões informadas."""
            
        # Monta prompt para LLM
        prompt = f"""
        Com base nas seguintes informações, gere histórias de usuário detalhadas:
        Informações do Produto: {request.productInfo}
        Épicos: {request.epicsSummary or 'Não fornecidos'}
        {request.userPromptAdjustment or ''}
        Por favor, gere histórias de usuário bem estruturadas seguindo o formato: 'Como [persona], eu quero [objetivo] para que [benefício]'.
        """
        # Chama LLM (deve retornar lista de dicts com title/description/persona)
        # Aqui, use a função real de LLM que retorna lista estruturada
        # Exemplo fake:
        historias_geradas = [
            {"title": "Como Product Owner, eu quero cadastrar produtos para iniciar o projeto", "description": "Permitir o cadastro inicial de produtos."},
            {"title": "Como Usuário, eu quero acessar o sistema via web", "description": "Acesso multiplataforma para diferentes personas."}
        ]
        # Salvar cada história no banco, vinculando ao primeiro épico (ou ajuste para múltiplos)
        persisted_stories = []
        epic_id = epic_ids[0] if epic_ids else None
        for h in historias_geradas:
            story_create = UserStoryCreate(title=h["title"], description=h["description"])
            new_story = UserStory(
                title=story_create.title,
                description=story_create.description,
                epic_id=epic_id,
                created_by=current_user.user_id
            )
            db.add(new_story)
            db.commit()
            db.refresh(new_story)
            persisted_stories.append({
                "user_story_id": new_story.story_id,
                "title": new_story.title,
                "description": new_story.description,
                "epic_id": new_story.epic_id
            })
        # LOG LLM INTERACTION
        log_llm_interaction(
            db=db,
            user_id=current_user.user_id,
            product_id=product_id,
            prompt=str(request),
            response=str(persisted_stories),
            model_used="llama3-8b-8192",
            tokens_used=None,
            entity_type="user_story",
            entity_id=None
        )
        return LLMResponse(
            content=persisted_stories,
            success=True,
            message="Histórias de usuário geradas e salvas com sucesso"
        )
    except Exception as e:
        logging.error(f"Erro ao gerar/salvar histórias de usuário: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao gerar/salvar histórias de usuário: {str(e)}"
        )

@router.post("/generate-requirements", response_model=LLMResponse)
@handle_errors
@logging_aspect
@notification_aspect
async def generate_requirements(request: LLMRequest, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    """
    Gera requisitos funcionais baseados nas histórias de usuário aprovadas do produto, salva no banco e retorna os requisitos persistidos.
    """
    try:
        # prompt = f"""
        # Com base nas seguintes informações, gere requisitos funcionais detalhados:
        
        # Informações do Produto: {request.productInfo}
        # Histórias de Usuário: {request.userStories or 'Não fornecidas'}
        
        # {request.userPromptAdjustment or ''}
        
        # Por favor, gere requisitos funcionais bem estruturados e organizados.
        # """
        
        # # Usar a função LLM real
        # LLM(prompt)
        
        # # Por enquanto, retornar um exemplo estruturado
        # content = [
        product_id = getattr(request, 'product_id', None)
        if not product_id:
            raise HTTPException(status_code=400, detail="product_id é obrigatório")
        # Buscar histórias aprovadas do produto
        approved_stories = db.query(UserStory).join(Epic).filter(
            Epic.product_id == product_id,
            UserStory.status == ReviewStatus.APPROVED.value
        ).all()
        if not approved_stories:
            raise HTTPException(status_code=404, detail="Nenhuma história aprovada encontrada para o produto.")
        # Para cada história, gerar requisitos via LLM (aqui exemplo fake)
        persisted_requirements = []
        for story in approved_stories:
            prompt = f"""
            Com base na seguinte história de usuário, gere requisitos funcionais detalhados e priorizados:
            História: {story.title}\n{story.description}
            {request.userPromptAdjustment or ''}
            Por favor, gere requisitos no formato: id, descricao, prioridade (Alta/Média/Baixa).
            """
            # Chamar LLM real aqui, exemplo fake:
            requisitos_gerados = [
                {"id": f"REQ-{story.story_id}-1", "descricao": f"Requisito para {story.title}", "prioridade": "Alta"}
            ]
            for req in requisitos_gerados:
                req_create = RequirementCreate(
                    description=req["descricao"],
                    priority=req["prioridade"]
                )
                new_req = Requirement(
                    description=req_create.description,
                    priority=req_create.priority,
                    story_id=story.story_id,
                    created_by=current_user.user_id
                )
                db.add(new_req)
                db.commit()
                db.refresh(new_req)
                persisted_requirements.append({
                    "requirement_id": new_req.requirement_id,
                    "description": new_req.description,
                    "priority": new_req.priority,
                    "story_id": new_req.story_id
                })
        # LOG LLM INTERACTION
        log_llm_interaction(
            db=db,
            user_id=current_user.user_id,
            product_id=product_id,
            prompt=str(request),
            response=str(persisted_requirements),
            model_used="llama3-8b-8192",
            tokens_used=None,
            entity_type="requirement",
            entity_id=None
        )
        return LLMResponse(
            content=persisted_requirements,
            success=True,
            message="Requisitos funcionais gerados e salvos com sucesso"
        )
    except Exception as e:
        logging.error(f"Erro ao gerar/salvar requisitos funcionais: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao gerar/salvar requisitos funcionais: {str(e)}"
        )
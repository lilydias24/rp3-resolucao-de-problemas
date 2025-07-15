from fastapi import APIRouter, HTTPException, status, Depends, Body
from src.schemas.llm import LLMRequest, LLMResponse, GenerateEpicsRequest, GenerateUserStoriesRequest, GenerateRequirementsRequest
from src.utils.epics import Epic as EpicUtil
from aspects.LLM import generate_epics_with_llm, generate_user_stories_with_llm, generate_requirements_with_llm, log_llm_interaction
from sqlalchemy.orm import Session
from src.db.session import get_db
from src.routers.auth import get_current_user
from src.db.models import Epic, UserStory, Requirement, Product, User
from src.schemas.epic import EpicCreate
from src.schemas.story import UserStoryCreate
from src.schemas.requirement import RequirementCreate
import logging

router = APIRouter(
    prefix="/llm-project",
    tags=["llm"],
    responses={
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Erro interno do servidor"}
    }
)

@router.post("/generate-epics", response_model=LLMResponse)
async def generate_epics(request: GenerateEpicsRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Gera épicos baseados nas informações do produto, salva no banco e retorna os épicos persistidos.
    """
    try:
        product = db.query(Product).filter(Product.product_id == request.product_id).first()
        if not product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produto não encontrado")

        product_info = {
            'nome': product.name,
            'descricao': product.description,
            'personas': product.personas,
            'proposta_valor': product.value_proposition,
        }

        epics_generated = generate_epics_with_llm(product_info=product_info)

        persisted_epics = []
        for epic_util in epics_generated:
            epic_create = EpicCreate(title=epic_util.title, description=epic_util.description)
            new_epic = Epic(
                **epic_create.model_dump(),
                product_id=request.product_id,
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

        log_llm_interaction(
            db=db,
            user_id=current_user.user_id,
            product_id=request.product_id,
            prompt=str(product_info),
            response=str(persisted_epics),
            model_used="llama3-8b-8192",
            entity_type="epic",
        )

        return LLMResponse(
            content=persisted_epics,
            success=True,
            message="Épicos gerados e salvos com sucesso!"
        )
    except Exception as e:
        logging.error(f"Erro ao gerar/salvar épicos: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao gerar/salvar épicos: {str(e)}"
        )


@router.post("/generate-user-stories", response_model=LLMResponse)
async def generate_user_stories(request: GenerateUserStoriesRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Gera histórias de usuário baseadas nos épicos, salva no banco e retorna as histórias persistidas.
    """
    try:
        product = db.query(Product).filter(Product.product_id == request.product_id).first()
        if not product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produto não encontrado")

        epics = db.query(Epic).filter(Epic.product_id == request.product_id).all()
        if not epics:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nenhum épico encontrado para este produto.")
            
        epics_summary = "\n".join([f"- {e.title}: {e.description}" for e in epics])

        user_stories_generated = generate_user_stories_with_llm(epics=epics_summary, custom_prompt=request.userPromptAdjustment)

        persisted_stories = []
        for story_util in user_stories_generated:
            # Assumindo que a LLM retorna um título que pode ser dividido em "como, quero, para"
            parts = story_util.title.split(',')
            if len(parts) >= 3:
                as_a = parts[0].replace("Como ", "").strip()
                i_want = parts[1].replace(" quero ", "").strip()
                so_that = parts[2].replace(" para que ", "").strip()
            else:
                as_a = "Usuário"
                i_want = story_util.title
                so_that = story_util.description

            story_create = UserStoryCreate(
                epic_id=epics[0].epic_id, # Simplificação: associar ao primeiro épico
                as_a=as_a,
                i_want=i_want,
                so_that=so_that,
                acceptance_criteria=[story_util.description] if hasattr(story_util, 'description') and story_util.description else None,
            )
            new_story = UserStory(
                **story_create.model_dump(),
                created_by=current_user.user_id
            )
            db.add(new_story)
            db.commit()
            db.refresh(new_story)
            persisted_stories.append({
                "story_id": new_story.story_id,
                "epic_id": new_story.epic_id,
                "as_a": new_story.as_a,
                "i_want": new_story.i_want,
                "so_that": new_story.so_that,
                "acceptance_criteria": new_story.acceptance_criteria,
                "priority": new_story.priority,
                "status": new_story.status,
                "created_by": new_story.created_by,
                "created_at": new_story.created_at
            })

        return LLMResponse(
            content=persisted_stories,
            success=True,
            message="Histórias de usuário geradas com sucesso!"
        )

    except Exception as e:
        logging.error(f"Erro ao gerar/salvar histórias de usuário: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao gerar/salvar histórias de usuário: {str(e)}"
        )


@router.post("/generate-requirements", response_model=LLMResponse)
async def generate_requirements(request: GenerateRequirementsRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Gera requisitos funcionais baseados nas histórias de usuário aprovadas.
    """
    try:
        story = db.query(UserStory).filter(UserStory.story_id == request.story_id).first()
        if not story:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="História de usuário não encontrada")

        # Construir título e descrição da história a partir dos campos disponíveis
        story_title = f"Como {story.as_a}, quero {story.i_want}, para que {story.so_that}"
        story_description = story.acceptance_criteria[0] if story.acceptance_criteria else ""
        
        requirements_generated = generate_requirements_with_llm(story_title=story_title, story_description=story_description)
        
        persisted_requirements = []
        for req_util in requirements_generated:
            req_create = RequirementCreate(
                story_id=request.story_id,
                description=req_util.description,
                priority=3 # Prioridade padrão
            )
            new_req = Requirement(
                **req_create.model_dump(),
                created_by=current_user.user_id
            )
            db.add(new_req)
            db.commit()
            db.refresh(new_req)
            persisted_requirements.append({
                "requirement_id": new_req.requirement_id,
                "story_id": new_req.story_id,
                "description": new_req.description,
                "priority": new_req.priority,
                "status": new_req.status,
                "created_by": new_req.created_by,
                "created_at": new_req.created_at
            })
            
        return LLMResponse(
            content=persisted_requirements,
            success=True,
            message="Requisitos gerados com sucesso!"
        )
    except Exception as e:
        logging.error(f"Erro ao gerar/salvar requisitos: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao gerar/salvar requisitos: {str(e)}"
        )
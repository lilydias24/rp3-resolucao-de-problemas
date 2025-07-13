from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from src.db.models import Product, User, Epic, UserStory, Requirement, Backlog, BacklogItem
from src.schemas.product import ProductCreate, ProductInDB
from src.db.session import get_db
from src.routers.auth import get_current_user
from aspects.logging import logging_aspect
from aspects.error_handling import handle_errors
from aspects.notification import notification_aspect
from aspects.authorization import require_admin
from aspects.revision_tracking import track_revisions, get_revision_history
from src.schemas.epic import EpicCreate, EpicInDB
from src.schemas.story import UserStoryCreate, UserStoryInDB
from src.schemas.requirement import RequirementCreate, RequirementInDB
from src.schemas.backlog import BacklogCreate, BacklogInDB, BacklogItemCreate, BacklogItemInDB

"""
Define as rotas relacionadas a produtos na API FastAPI.
Inclui endpoints para criação, listagem e manipulação de produtos.
"""

router = APIRouter(
    prefix="/products",
    tags=["products"],
    responses={
        status.HTTP_403_FORBIDDEN: {"description": "Acesso negado"},
        status.HTTP_404_NOT_FOUND: {"description": "Produto não encontrado"}
    }
)

@handle_errors
@logging_aspect
@notification_aspect
# @require_admin  
def business_create_product(product_data: ProductCreate, db: Session, current_user: User):
    """
    Função de negócio para criar um novo produto.
    Verifica duplicidade e realiza a criação no banco de dados.
    Args:
        product_data (ProductCreate): Dados do produto.
        db (Session): Sessão do banco de dados.
        current_user (User): Usuário autenticado.
    Returns:
        Product: Produto criado.
    """
    # Verifica se o produto já existe
    existing_product = db.query(Product).filter(
        Product.name == product_data.name,
        Product.created_by == current_user.user_id
    ).first()
    
    if existing_product:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Você já tem um produto com este nome"
        )

    # Criação do produto
    new_product = Product(
        **product_data.model_dump(exclude_unset=True),  # Pega apenas os campos fornecidos
        created_by=current_user.user_id
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product

@router.post(
    "/",
    response_model=ProductInDB,
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {
            "description": "Produto criado com sucesso",
            "content": {
                "application/json": {
                    "example": {
                        "product_id": 1,
                        "name": "Meu Produto",
                        "description": "Descrição do produto",
                        "platforms": ["web", "mobile"],
                        "created_by": 123,
                        "created_at": "2023-11-21T10:00:00Z"
                    }
                }
            }
        },
        status.HTTP_400_BAD_REQUEST: {
            "description": "Dados inválidos ou produto já existe"
        }
    }
)
def create_product(
    product_data: ProductCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Endpoint para criar um novo produto.
    Recebe os dados do produto e retorna o produto criado.
    """
    return business_create_product(product_data, db, current_user)

@router.post("/{product_id}/epics", response_model=EpicInDB)
@handle_errors
@logging_aspect
@notification_aspect
def create_epic(product_id: int, epic: EpicCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Cria um novo épico para um produto específico.
    """
    new_epic = Epic(**epic.dict(), product_id=product_id)
    db.add(new_epic)
    db.commit()
    db.refresh(new_epic)
    return new_epic

@router.get("/{product_id}/epics", response_model=List[EpicInDB])
@handle_errors
@logging_aspect
def list_epics(product_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Lista todos os épicos de um produto.
    """
    return db.query(Epic).filter(Epic.product_id == product_id).all()

@router.put("/epics/{epic_id}", response_model=EpicInDB)
@handle_errors
@track_revisions("epic")
@logging_aspect
@notification_aspect
def update_epic(epic_id: int, epic: EpicCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Atualiza um épico existente.
    """
    db_epic = db.query(Epic).filter(Epic.epic_id == epic_id).first()
    if not db_epic:
        raise HTTPException(status_code=404, detail="Épico não encontrado")
    for key, value in epic.dict(exclude_unset=True).items():
        setattr(db_epic, key, value)
    db.commit()
    db.refresh(db_epic)
    return db_epic

# --- REVISION HISTORY ---
@router.get("/epics/{epic_id}/revisions")
@handle_errors
@logging_aspect
def get_epic_revisions(epic_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Obtém o histórico de revisões de um épico.
    """
    revisions = get_revision_history(db, "epic", epic_id)
    return revisions

@router.get("/stories/{story_id}/revisions")
@handle_errors
@logging_aspect
def get_story_revisions(story_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Obtém o histórico de revisões de uma história de usuário.
    """
    revisions = get_revision_history(db, "user_story", story_id)
    return revisions

@router.get("/requirements/{requirement_id}/revisions")
@handle_errors
@logging_aspect
def get_requirement_revisions(requirement_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Obtém o histórico de revisões de um requisito.
    """
    revisions = get_revision_history(db, "requirement", requirement_id)
    return revisions

# --- USER STORIES ---
@router.post("/{epic_id}/stories", response_model=UserStoryInDB)
@handle_errors
@logging_aspect
@notification_aspect
def create_story(epic_id: int, story: UserStoryCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Cria uma nova história de usuário para um épico.
    """
    new_story = UserStory(**story.dict(), epic_id=epic_id, created_by=current_user.user_id)
    db.add(new_story)
    db.commit()
    db.refresh(new_story)
    return new_story

@router.get("/{epic_id}/stories", response_model=List[UserStoryInDB])
@handle_errors
@logging_aspect
def list_stories(epic_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Lista todas as histórias de usuário de um épico.
    """
    return db.query(UserStory).filter(UserStory.epic_id == epic_id).all()

@router.get("/stories/{story_id}", response_model=UserStoryInDB)
@handle_errors
@logging_aspect
def get_story(story_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Busca uma história de usuário pelo seu ID.
    """
    story = db.query(UserStory).filter(UserStory.story_id == story_id).first()
    if not story:
        raise HTTPException(status_code=404, detail="História não encontrada")
    return story

@router.put("/stories/{story_id}", response_model=UserStoryInDB)
@handle_errors
@track_revisions("user_story")
@logging_aspect
@notification_aspect
def update_story(story_id: int, story: UserStoryCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Atualiza uma história de usuário existente.
    """
    db_story = db.query(UserStory).filter(UserStory.story_id == story_id).first()
    if not db_story:
        raise HTTPException(status_code=404, detail="História não encontrada")
    for key, value in story.dict(exclude_unset=True).items():
        setattr(db_story, key, value)
    db.commit()
    db.refresh(db_story)
    return db_story

@router.delete("/stories/{story_id}", status_code=204)
@handle_errors
@logging_aspect
@notification_aspect
def delete_story(story_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Remove uma história de usuário pelo seu ID.
    """
    db_story = db.query(UserStory).filter(UserStory.story_id == story_id).first()
    if not db_story:
        raise HTTPException(status_code=404, detail="História não encontrada")
    db.delete(db_story)
    db.commit()
    return None

# --- REQUIREMENTS ---
@router.post("/stories/{story_id}/requirements", response_model=RequirementInDB)
@handle_errors
@logging_aspect
@notification_aspect
def create_requirement(story_id: int, req: RequirementCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Cria um novo requisito para uma história de usuário.
    """
    new_req = Requirement(**req.dict(), story_id=story_id, created_by=current_user.user_id)
    db.add(new_req)
    db.commit()
    db.refresh(new_req)
    return new_req

@router.get("/stories/{story_id}/requirements", response_model=List[RequirementInDB])
@handle_errors
@logging_aspect
def list_requirements(story_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Lista todos os requisitos de uma história de usuário.
    """
    return db.query(Requirement).filter(Requirement.story_id == story_id).all()

@router.get("/requirements/{requirement_id}", response_model=RequirementInDB)
@handle_errors
@logging_aspect
def get_requirement(requirement_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Busca um requisito pelo seu ID.
    """
    req = db.query(Requirement).filter(Requirement.requirement_id == requirement_id).first()
    if not req:
        raise HTTPException(status_code=404, detail="Requisito não encontrado")
    return req

@router.put("/requirements/{requirement_id}", response_model=RequirementInDB)
@handle_errors
@track_revisions("requirement")
@logging_aspect
@notification_aspect
def update_requirement(requirement_id: int, req: RequirementCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Atualiza um requisito existente.
    """
    db_req = db.query(Requirement).filter(Requirement.requirement_id == requirement_id).first()
    if not db_req:
        raise HTTPException(status_code=404, detail="Requisito não encontrado")
    for key, value in req.dict(exclude_unset=True).items():
        setattr(db_req, key, value)
    db.commit()
    db.refresh(db_req)
    return db_req

@router.delete("/requirements/{requirement_id}", status_code=204)
@handle_errors
@logging_aspect
@notification_aspect
def delete_requirement(requirement_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Remove um requisito pelo seu ID.
    """
    db_req = db.query(Requirement).filter(Requirement.requirement_id == requirement_id).first()
    if not db_req:
        raise HTTPException(status_code=404, detail="Requisito não encontrado")
    db.delete(db_req)
    db.commit()
    return None

# --- BACKLOG ---
@router.post("/{product_id}/backlogs", response_model=BacklogInDB)
@handle_errors
@logging_aspect
@notification_aspect
def create_backlog(product_id: int, backlog: BacklogCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Cria um novo backlog para um produto.
    """
    new_backlog = Backlog(**backlog.dict(), product_id=product_id, created_by=current_user.user_id)
    db.add(new_backlog)
    db.commit()
    db.refresh(new_backlog)
    return new_backlog

@router.get("/{product_id}/backlogs", response_model=List[BacklogInDB])
@handle_errors
@logging_aspect
def list_backlogs(product_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Lista todos os backlogs de um produto.
    """
    return db.query(Backlog).filter(Backlog.product_id == product_id).all()

@router.get("/backlogs/{backlog_id}", response_model=BacklogInDB)
@handle_errors
@logging_aspect
def get_backlog(backlog_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Busca um backlog pelo seu ID.
    """
    backlog = db.query(Backlog).filter(Backlog.backlog_id == backlog_id).first()
    if not backlog:
        raise HTTPException(status_code=404, detail="Backlog não encontrado")
    return backlog

@router.put("/backlogs/{backlog_id}", response_model=BacklogInDB)
@handle_errors
@logging_aspect
@notification_aspect
def update_backlog(backlog_id: int, backlog: BacklogCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Atualiza um backlog existente.
    """
    db_backlog = db.query(Backlog).filter(Backlog.backlog_id == backlog_id).first()
    if not db_backlog:
        raise HTTPException(status_code=404, detail="Backlog não encontrado")
    for key, value in backlog.dict(exclude_unset=True).items():
        setattr(db_backlog, key, value)
    db.commit()
    db.refresh(db_backlog)
    return db_backlog

@router.delete("/backlogs/{backlog_id}", status_code=204)
@handle_errors
@logging_aspect
@notification_aspect
def delete_backlog(backlog_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Remove um backlog pelo seu ID.
    """
    db_backlog = db.query(Backlog).filter(Backlog.backlog_id == backlog_id).first()
    if not db_backlog:
        raise HTTPException(status_code=404, detail="Backlog não encontrado")
    db.delete(db_backlog)
    db.commit()
    return None

# --- BACKLOG ITEMS ---
@router.post("/backlogs/{backlog_id}/items", response_model=BacklogItemInDB)
@handle_errors
@logging_aspect
@notification_aspect
def create_backlog_item(backlog_id: int, item: BacklogItemCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Cria um novo item em um backlog.
    """
    new_item = BacklogItem(**item.dict(), backlog_id=backlog_id)
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item

@router.get("/backlogs/{backlog_id}/items", response_model=List[BacklogItemInDB])
@handle_errors
@logging_aspect
def list_backlog_items(backlog_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Lista todos os itens de um backlog.
    """
    return db.query(BacklogItem).filter(BacklogItem.backlog_id == backlog_id).all()

@router.get("/backlog-items/{item_id}", response_model=BacklogItemInDB)
@handle_errors
@logging_aspect
def get_backlog_item(item_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Busca um item do backlog pelo seu ID.
    """
    item = db.query(BacklogItem).filter(BacklogItem.item_id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item do backlog não encontrado")
    return item

@router.put("/backlog-items/{item_id}", response_model=BacklogItemInDB)
@handle_errors
@logging_aspect
@notification_aspect
def update_backlog_item(item_id: int, item: BacklogItemCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Atualiza um item do backlog existente.
    """
    db_item = db.query(BacklogItem).filter(BacklogItem.item_id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item do backlog não encontrado")
    for key, value in item.dict(exclude_unset=True).items():
        setattr(db_item, key, value)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.delete("/backlog-items/{item_id}", status_code=204)
@handle_errors
@logging_aspect
@notification_aspect
def delete_backlog_item(item_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Remove um item do backlog pelo seu ID.
    """
    db_item = db.query(BacklogItem).filter(BacklogItem.item_id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item do backlog não encontrado")
    db.delete(db_item)
    db.commit()
    return None

# TODO: Implementar endpoints para épicos, histórias, requisitos, backlog, etc. no futuro.
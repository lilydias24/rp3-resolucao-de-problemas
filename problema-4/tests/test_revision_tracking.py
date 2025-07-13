"""
Testes para o sistema de rastreamento de revisões.
Verifica se as mudanças em épicos, histórias e requisitos são registradas automaticamente.
"""

import pytest
from sqlalchemy.orm import Session
from src.db.models import User, Epic, UserStory, Requirement, RevisionHistory
from src.schemas.epic import EpicCreate
from src.schemas.story import UserStoryCreate
from src.schemas.requirement import RequirementCreate
from aspects.revision_tracking import track_revisions, get_revision_history, record_changes
from datetime import datetime

@pytest.fixture
def admin_user(db_session):
    """Cria um usuário administrador para os testes."""
    user = User(
        email="admin@test.com",
        password_hash="hashed_password",
        name="Admin User",
        role="admin"
    )
    db_session.add(user)
    db_session.commit()
    return user

@pytest.fixture
def test_epic(db_session, admin_user):
    """Cria um épico de teste."""
    epic = Epic(
        product_id=1,
        title="Épico Teste",
        description="Descrição do épico teste",
        created_by=admin_user.user_id
    )
    db_session.add(epic)
    db_session.commit()
    return epic

@pytest.fixture
def test_story(db_session, admin_user, test_epic):
    """Cria uma história de usuário de teste."""
    story = UserStory(
        epic_id=test_epic.epic_id,
        as_a="Usuário",
        i_want="fazer algo",
        so_that="possa alcançar um objetivo",
        created_by=admin_user.user_id
    )
    db_session.add(story)
    db_session.commit()
    return story

@pytest.fixture
def test_requirement(db_session, admin_user, test_story):
    """Cria um requisito de teste."""
    requirement = Requirement(
        story_id=test_story.story_id,
        description="Requisito teste",
        created_by=admin_user.user_id
    )
    db_session.add(requirement)
    db_session.commit()
    return requirement

def test_track_epic_revisions(db_session, admin_user, test_epic):
    """Testa se as mudanças em épicos são rastreadas."""
    
    @track_revisions("epic")
    def update_epic(epic_id: int, new_title: str, db: Session, current_user: User):
        epic = db.query(Epic).filter(Epic.epic_id == epic_id).first()
        epic.title = new_title
        db.commit()
        return epic
    
    # Fazer uma mudança
    update_epic(test_epic.epic_id, "Novo Título", db_session, admin_user)
    
    # Verificar se a revisão foi registrada
    revisions = get_revision_history(db_session, "epic", test_epic.epic_id)
    assert len(revisions) > 0
    
    # Verificar se a mudança específica foi registrada
    title_revision = next((r for r in revisions if r.field_changed == "title"), None)
    assert title_revision is not None
    assert title_revision.old_value == "Épico Teste"
    assert title_revision.new_value == "Novo Título"
    assert title_revision.changed_by == admin_user.user_id

def test_track_story_revisions(db_session, admin_user, test_story):
    """Testa se as mudanças em histórias são rastreadas."""
    
    @track_revisions("user_story")
    def update_story(story_id: int, new_as_a: str, db: Session, current_user: User):
        story = db.query(UserStory).filter(UserStory.story_id == story_id).first()
        story.as_a = new_as_a
        db.commit()
        return story
    
    # Fazer uma mudança
    update_story(test_story.story_id, "Novo Usuário", db_session, admin_user)
    
    # Verificar se a revisão foi registrada
    revisions = get_revision_history(db_session, "user_story", test_story.story_id)
    assert len(revisions) > 0
    
    # Verificar se a mudança específica foi registrada
    as_a_revision = next((r for r in revisions if r.field_changed == "as_a"), None)
    assert as_a_revision is not None
    assert as_a_revision.old_value == "Usuário"
    assert as_a_revision.new_value == "Novo Usuário"

def test_track_requirement_revisions(db_session, admin_user, test_requirement):
    """Testa se as mudanças em requisitos são rastreadas."""
    
    @track_revisions("requirement")
    def update_requirement(req_id: int, new_description: str, db: Session, current_user: User):
        req = db.query(Requirement).filter(Requirement.requirement_id == req_id).first()
        req.description = new_description
        db.commit()
        return req
    
    # Fazer uma mudança
    update_requirement(test_requirement.requirement_id, "Nova Descrição", db_session, admin_user)
    
    # Verificar se a revisão foi registrada
    revisions = get_revision_history(db_session, "requirement", test_requirement.requirement_id)
    assert len(revisions) > 0
    
    # Verificar se a mudança específica foi registrada
    desc_revision = next((r for r in revisions if r.field_changed == "description"), None)
    assert desc_revision is not None
    assert desc_revision.old_value == "Requisito teste"
    assert desc_revision.new_value == "Nova Descrição"

def test_record_changes_function(db_session, admin_user):
    """Testa a função record_changes diretamente."""
    old_state = {"title": "Título Antigo", "description": "Descrição Antiga"}
    new_state = {"title": "Título Novo", "description": "Descrição Nova"}
    
    record_changes(db_session, "epic", 1, old_state, new_state, admin_user.user_id, "Teste manual")
    
    # Verificar se as revisões foram registradas
    revisions = db_session.query(RevisionHistory).filter(
        RevisionHistory.entity_type == "epic",
        RevisionHistory.entity_id == 1
    ).all()
    
    assert len(revisions) == 2  # title e description
    
    title_revision = next((r for r in revisions if r.field_changed == "title"), None)
    assert title_revision is not None
    assert title_revision.old_value == "Título Antigo"
    assert title_revision.new_value == "Título Novo"
    assert title_revision.change_reason == "Teste manual"

def test_get_revision_history_empty(db_session):
    """Testa obter histórico de revisões quando não há mudanças."""
    revisions = get_revision_history(db_session, "epic", 999)
    assert len(revisions) == 0

def test_multiple_changes_tracking(db_session, admin_user, test_epic):
    """Testa rastreamento de múltiplas mudanças."""
    
    @track_revisions("epic")
    def update_epic_multiple(epic_id: int, new_title: str, new_description: str, db: Session, current_user: User):
        epic = db.query(Epic).filter(Epic.epic_id == epic_id).first()
        epic.title = new_title
        epic.description = new_description
        db.commit()
        return epic
    
    # Fazer múltiplas mudanças
    update_epic_multiple(test_epic.epic_id, "Título Final", "Descrição Final", db_session, admin_user)
    
    # Verificar se todas as mudanças foram registradas
    revisions = get_revision_history(db_session, "epic", test_epic.epic_id)
    assert len(revisions) >= 2  # title e description
    
    # Verificar se há revisões para ambos os campos
    title_revisions = [r for r in revisions if r.field_changed == "title"]
    desc_revisions = [r for r in revisions if r.field_changed == "description"]
    
    assert len(title_revisions) > 0
    assert len(desc_revisions) > 0 
"""
Testes para o sistema de geração automática de backlog.
Testa a geração de backlog a partir de histórias e requisitos aprovados.
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.db.base import Base
from src.db.models import User, Product, Epic, UserStory, Requirement
from main import app
from src.routers.auth import create_access_token
from src.schemas.review import ReviewStatus
from datetime import datetime

# Configuração do banco de dados de teste (PostgreSQL real)
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:root@localhost:5432/problema4_tests"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides = {}

@pytest.fixture
def client():
    Base.metadata.create_all(bind=engine)
    with TestClient(app) as c:
        yield c
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def db_session():
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()

@pytest.fixture
def test_user(db_session):
    user = User(
        email="test@example.com",
        password_hash="hashed_password",
        name="Test User"
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user

@pytest.fixture
def test_product(db_session, test_user):
    product = Product(
        name="Test Product",
        description="Test Description",
        value_proposition="Test Value",
        created_by=test_user.user_id
    )
    db_session.add(product)
    db_session.commit()
    db_session.refresh(product)
    return product

@pytest.fixture
def test_epic(db_session, test_user, test_product):
    epic = Epic(
        title="Test Epic",
        description="Test Description",
        status="approved",
        product_id=test_product.product_id,
        created_by=test_user.user_id
    )
    db_session.add(epic)
    db_session.commit()
    db_session.refresh(epic)
    return epic

@pytest.fixture
def test_stories(db_session, test_user, test_epic):
    stories = []
    for i in range(3):
        story = UserStory(
            epic_id=test_epic.epic_id,
            as_a=f"User {i}",
            i_want=f"feature {i}",
            so_that=f"benefit {i}",
            priority=5 - i,  # Prioridades diferentes
            status=ReviewStatus.APPROVED.value,
            created_by=test_user.user_id
        )
        db_session.add(story)
        stories.append(story)
    
    db_session.commit()
    for story in stories:
        db_session.refresh(story)
    return stories

@pytest.fixture
def test_requirements(db_session, test_user, test_stories):
    requirements = []
    for i, story in enumerate(test_stories):
        req = Requirement(
            story_id=story.story_id,
            description=f"Requirement {i}",
            technical_details=f"Technical details {i}",
            priority=4 - i,
            status=ReviewStatus.APPROVED.value,
            created_by=test_user.user_id
        )
        db_session.add(req)
        requirements.append(req)
    
    db_session.commit()
    for req in requirements:
        db_session.refresh(req)
    return requirements

@pytest.fixture
def auth_headers(test_user):
    token = create_access_token(data={"sub": test_user.email})
    return {"Authorization": f"Bearer {token}"}

class TestBacklogGeneration:
    """Testes para geração automática de backlog"""
    
    def test_get_generation_strategies(self, client, auth_headers):
        """Testa obtenção das estratégias de geração"""
        response = client.get("/backlog-generation/strategies", headers=auth_headers)
        assert response.status_code == 200
        
        data = response.json()
        assert "strategies" in data
        assert len(data["strategies"]) == 5
        
        strategy_values = [s["value"] for s in data["strategies"]]
        assert "priority_based" in strategy_values
        assert "epic_based" in strategy_values
        assert "story_only" in strategy_values
        assert "requirement_only" in strategy_values
        assert "mixed" in strategy_values
    
    def test_get_approved_items_count(self, client, auth_headers, test_product, test_stories, test_requirements):
        """Testa contagem de itens aprovados"""
        response = client.get(f"/backlog-generation/products/{test_product.product_id}/approved-items", headers=auth_headers)
        assert response.status_code == 200
        
        data = response.json()
        assert data["product_id"] == test_product.product_id
        assert data["approved_stories"] == 3
        assert data["approved_requirements"] == 3
        assert data["total_approved_items"] == 6
        assert data["can_generate_backlog"] == True
    
    def test_get_epics_summary(self, client, auth_headers, test_product, test_epic, test_stories, test_requirements):
        """Testa resumo de épicos"""
        response = client.get(f"/backlog-generation/products/{test_product.product_id}/epics-summary", headers=auth_headers)
        assert response.status_code == 200
        
        data = response.json()
        assert data["product_id"] == test_product.product_id
        assert data["total_epics"] == 1
        assert data["epics_with_approved_items"] == 1
        
        epic_summary = data["epics_summary"][0]
        assert epic_summary["epic_id"] == test_epic.epic_id
        assert epic_summary["epic_title"] == test_epic.title
        assert epic_summary["approved_stories"] == 3
        assert epic_summary["approved_requirements"] == 3
        assert epic_summary["total_approved_items"] == 6
    
    def test_preview_backlog_generation(self, client, auth_headers, test_product, test_stories, test_requirements):
        """Testa preview da geração de backlog"""
        request_data = {
            "product_id": test_product.product_id,
            "name": "Test Backlog",
            "description": "Test Description",
            "strategy": "priority_based",
            "include_stories": True,
            "include_requirements": True,
            "min_priority": 3,
            "auto_prioritize": True
        }
        
        response = client.post("/backlog-generation/preview", json=request_data, headers=auth_headers)
        assert response.status_code == 200
        
        data = response.json()
        assert data["estimated_items"] == 6
        assert data["estimated_stories"] == 3
        assert data["estimated_requirements"] == 3
        assert data["strategy"] == "priority_based"
        assert len(data["preview_items"]) == 6  # Todos os itens no preview
    
    def test_generate_backlog_priority_based(self, client, auth_headers, test_product, test_stories, test_requirements):
        """Testa geração de backlog com estratégia baseada em prioridade"""
        request_data = {
            "product_id": test_product.product_id,
            "name": "Test Backlog",
            "description": "Test Description",
            "strategy": "priority_based",
            "include_stories": True,
            "include_requirements": True,
            "min_priority": 3,
            "auto_prioritize": True
        }
        
        response = client.post("/backlog-generation/generate", json=request_data, headers=auth_headers)
        assert response.status_code == 200
        
        data = response.json()
        assert data["backlog_name"] == "Test Backlog"
        assert data["total_items"] == 6
        assert data["stories_count"] == 3
        assert data["requirements_count"] == 3
        assert data["generation_strategy"] == "priority_based"
        assert "summary" in data
    
    def test_generate_backlog_story_only(self, client, auth_headers, test_product, test_stories, test_requirements):
        """Testa geração de backlog apenas com histórias"""
        request_data = {
            "product_id": test_product.product_id,
            "name": "Stories Only Backlog",
            "description": "Only stories",
            "strategy": "story_only",
            "include_stories": True,
            "include_requirements": False,
            "min_priority": 3,
            "auto_prioritize": True
        }
        
        response = client.post("/backlog-generation/generate", json=request_data, headers=auth_headers)
        assert response.status_code == 200
        
        data = response.json()
        assert data["total_items"] == 3
        assert data["stories_count"] == 3
        assert data["requirements_count"] == 0
        assert data["generation_strategy"] == "story_only"
    
    def test_generate_backlog_requirement_only(self, client, auth_headers, test_product, test_stories, test_requirements):
        """Testa geração de backlog apenas com requisitos"""
        request_data = {
            "product_id": test_product.product_id,
            "name": "Requirements Only Backlog",
            "description": "Only requirements",
            "strategy": "requirement_only",
            "include_stories": False,
            "include_requirements": True,
            "min_priority": 3,
            "auto_prioritize": True
        }
        
        response = client.post("/backlog-generation/generate", json=request_data, headers=auth_headers)
        assert response.status_code == 200
        
        data = response.json()
        assert data["total_items"] == 3
        assert data["stories_count"] == 0
        assert data["requirements_count"] == 3
        assert data["generation_strategy"] == "requirement_only"
    
    def test_generate_backlog_with_max_items(self, client, auth_headers, test_product, test_stories, test_requirements):
        """Testa geração de backlog com limite de itens"""
        request_data = {
            "product_id": test_product.product_id,
            "name": "Limited Backlog",
            "description": "Limited items",
            "strategy": "priority_based",
            "include_stories": True,
            "include_requirements": True,
            "min_priority": 3,
            "max_items": 3,
            "auto_prioritize": True
        }
        
        response = client.post("/backlog-generation/generate", json=request_data, headers=auth_headers)
        assert response.status_code == 200
        
        data = response.json()
        assert data["total_items"] == 3  # Limitado a 3 itens
        assert len(data["items"]) == 3
    
    def test_generate_backlog_with_min_priority(self, client, auth_headers, test_product, test_stories, test_requirements):
        """Testa geração de backlog com prioridade mínima"""
        request_data = {
            "product_id": test_product.product_id,
            "name": "High Priority Backlog",
            "description": "High priority items only",
            "strategy": "priority_based",
            "include_stories": True,
            "include_requirements": True,
            "min_priority": 4,  # Apenas prioridade 4 e 5
            "auto_prioritize": True
        }
        
        response = client.post("/backlog-generation/generate", json=request_data, headers=auth_headers)
        assert response.status_code == 200
        
        data = response.json()
        # Deve incluir apenas itens com prioridade 4 e 5
        for item in data["items"]:
            assert item["priority"] >= 4
    
    def test_generate_quick_backlog(self, client, auth_headers, test_product, test_stories, test_requirements):
        """Testa geração rápida de backlog"""
        response = client.post(
            f"/backlog-generation/generate/quick?product_id={test_product.product_id}&name=Quick Backlog&description=Quick generation",
            headers=auth_headers
        )
        assert response.status_code == 200
        
        data = response.json()
        assert data["backlog_name"] == "Quick Backlog"
        assert data["total_items"] == 6
        assert data["generation_strategy"] == "priority_based"
    
    def test_generate_backlog_no_approved_items(self, client, auth_headers, test_product):
        """Testa geração de backlog sem itens aprovados"""
        request_data = {
            "product_id": test_product.product_id,
            "name": "Empty Backlog",
            "description": "No approved items",
            "strategy": "priority_based",
            "include_stories": True,
            "include_requirements": True,
            "min_priority": 3,
            "auto_prioritize": True
        }
        
        response = client.post("/backlog-generation/generate", json=request_data, headers=auth_headers)
        assert response.status_code == 400
        assert "Nenhuma história de usuário ou requisito aprovado encontrado" in response.json()["detail"]
    
    def test_generate_backlog_invalid_product(self, client, auth_headers, test_stories, test_requirements):
        """Testa geração de backlog com produto inválido"""
        request_data = {
            "product_id": 99999,  # Produto inexistente
            "name": "Invalid Backlog",
            "description": "Invalid product",
            "strategy": "priority_based",
            "include_stories": True,
            "include_requirements": True,
            "min_priority": 3,
            "auto_prioritize": True
        }
        
        response = client.post("/backlog-generation/generate", json=request_data, headers=auth_headers)
        assert response.status_code == 400
        assert "não encontrado" in response.json()["detail"]
    
    def test_backlog_items_ordering(self, client, auth_headers, test_product, test_stories, test_requirements):
        """Testa se os itens do backlog estão ordenados corretamente por prioridade"""
        request_data = {
            "product_id": test_product.product_id,
            "name": "Ordered Backlog",
            "description": "Test ordering",
            "strategy": "priority_based",
            "include_stories": True,
            "include_requirements": True,
            "min_priority": 1,
            "auto_prioritize": True
        }
        
        response = client.post("/backlog-generation/generate", json=request_data, headers=auth_headers)
        assert response.status_code == 200
        
        data = response.json()
        items = data["items"]
        
        # Verificar se está ordenado por prioridade (maior primeiro)
        priorities = [item["priority"] for item in items]
        assert priorities == sorted(priorities, reverse=True)
    
    def test_backlog_generation_with_options(self, client, auth_headers, test_product, test_stories, test_requirements):
        """Testa geração de backlog com opções personalizadas"""
        request_data = {
            "product_id": test_product.product_id,
            "name": "Custom Backlog",
            "description": "Custom options",
            "strategy": "priority_based",
            "include_stories": True,
            "include_requirements": True,
            "min_priority": 3,
            "auto_prioritize": True
        }
        
        options_data = {
            "story_weight": 2.0,
            "requirement_weight": 1.0,
            "priority_multiplier": 2.0,
            "recent_bonus": 0.5,
            "complexity_factor": True
        }
        
        response = client.post(
            "/backlog-generation/generate", 
            json={"request": request_data, "options": options_data}, 
            headers=auth_headers
        )
        assert response.status_code == 200
        
        data = response.json()
        assert data["generation_options"]["story_weight"] == 2.0
        assert data["generation_options"]["requirement_weight"] == 1.0
        assert data["generation_options"]["priority_multiplier"] == 2.0 
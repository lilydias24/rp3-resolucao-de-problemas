"""
Testes para o sistema de revisão/sugestão.
Testa comentários, ações de revisão e gerenciamento de status.
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.db.base import Base
from src.db.models import User, Epic, UserStory, Requirement, ReviewComment, ReviewStatusHistory
from main import app
from src.routers.auth import create_access_token
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
def test_epic(db_session, test_user):
    epic = Epic(
        title="Test Epic",
        description="Test Description",
        status="draft",
        product_id=1,
        created_by=test_user.user_id
    )
    db_session.add(epic)
    db_session.commit()
    db_session.refresh(epic)
    return epic

@pytest.fixture
def auth_headers(test_user):
    token = create_access_token(data={"sub": test_user.email})
    return {"Authorization": f"Bearer {token}"}

class TestReviewSystem:
    """Testes para o sistema de revisão"""
    
    def test_create_review_comment(self, client, auth_headers, test_epic):
        """Testa criação de comentário de revisão"""
        comment_data = {
            "entity_type": "epic",
            "entity_id": test_epic.epic_id,
            "comment": "Este é um comentário de revisão",
            "is_suggestion": False,
            "suggested_changes": None
        }
        
        response = client.post("/review/comments", json=comment_data, headers=auth_headers)
        assert response.status_code == 200
        
        data = response.json()
        assert data["comment"] == "Este é um comentário de revisão"
        assert data["entity_type"] == "epic"
        assert data["entity_id"] == test_epic.epic_id
        assert data["is_suggestion"] == False
    
    def test_create_suggestion_comment(self, client, auth_headers, test_epic):
        """Testa criação de comentário com sugestão"""
        comment_data = {
            "entity_type": "epic",
            "entity_id": test_epic.epic_id,
            "comment": "Sugestão de melhoria",
            "is_suggestion": True,
            "suggested_changes": "Adicionar mais detalhes na descrição"
        }
        
        response = client.post("/review/comments", json=comment_data, headers=auth_headers)
        assert response.status_code == 200
        
        data = response.json()
        assert data["is_suggestion"] == True
        assert data["suggested_changes"] == "Adicionar mais detalhes na descrição"
    
    def test_get_review_comments(self, client, auth_headers, test_epic, db_session):
        """Testa listagem de comentários de revisão"""
        # Criar comentários de teste
        comment1 = ReviewComment(
            entity_type="epic",
            entity_id=test_epic.epic_id,
            comment="Comentário 1",
            created_by=1
        )
        comment2 = ReviewComment(
            entity_type="epic",
            entity_id=test_epic.epic_id,
            comment="Comentário 2",
            created_by=1
        )
        db_session.add_all([comment1, comment2])
        db_session.commit()
        
        response = client.get(f"/review/comments/epic/{test_epic.epic_id}", headers=auth_headers)
        assert response.status_code == 200
        
        data = response.json()
        assert len(data) == 2
        assert data[0]["comment"] == "Comentário 2"  # Ordem decrescente por data
    
    def test_approve_epic(self, client, auth_headers, test_epic):
        """Testa aprovação de épico"""
        action_data = {
            "action": "approve",
            "comment": "Aprovado após revisão",
            "reason": "Atende aos critérios estabelecidos"
        }
        
        response = client.post(f"/review/epic/{test_epic.epic_id}/action", json=action_data, headers=auth_headers)
        assert response.status_code == 200
        
        data = response.json()
        assert data["new_status"] == "approved"
        assert "Aprovado após revisão" in data["message"]
    
    def test_reject_epic(self, client, auth_headers, test_epic):
        """Testa rejeição de épico"""
        action_data = {
            "action": "reject",
            "comment": "Não atende aos requisitos",
            "reason": "Falta de detalhamento técnico"
        }
        
        response = client.post(f"/review/epic/{test_epic.epic_id}/action", json=action_data, headers=auth_headers)
        assert response.status_code == 200
        
        data = response.json()
        assert data["new_status"] == "rejected"
    
    def test_request_revision(self, client, auth_headers, test_epic):
        """Testa solicitação de revisão"""
        action_data = {
            "action": "request_revision",
            "comment": "Precisa de mais detalhes",
            "reason": "Descrição muito vaga"
        }
        
        response = client.post(f"/review/epic/{test_epic.epic_id}/action", json=action_data, headers=auth_headers)
        assert response.status_code == 200
        
        data = response.json()
        assert data["new_status"] == "needs_revision"
    
    def test_mark_implemented(self, client, auth_headers, test_epic):
        """Testa marcação como implementado"""
        action_data = {
            "action": "mark_implemented",
            "comment": "Implementação concluída",
            "reason": "Funcionalidade desenvolvida e testada"
        }
        
        response = client.post(f"/review/epic/{test_epic.epic_id}/action", json=action_data, headers=auth_headers)
        assert response.status_code == 200
        
        data = response.json()
        assert data["new_status"] == "implemented"
    
    def test_get_review_info(self, client, auth_headers, test_epic, db_session):
        """Testa obtenção de informações de revisão"""
        # Criar comentários e histórico
        comment = ReviewComment(
            entity_type="epic",
            entity_id=test_epic.epic_id,
            comment="Test comment",
            is_suggestion=True,
            created_by=1
        )
        history = ReviewStatusHistory(
            entity_type="epic",
            entity_id=test_epic.epic_id,
            old_status="draft",
            new_status="in_review",
            changed_by=1,
            reason="Submetido para revisão"
        )
        db_session.add_all([comment, history])
        db_session.commit()
        
        response = client.get(f"/review/epic/{test_epic.epic_id}/info", headers=auth_headers)
        assert response.status_code == 200
        
        data = response.json()
        assert data["current_status"] == "draft"
        assert data["total_comments"] == 1
        assert data["pending_reviews"] == 1
    
    def test_get_review_summary(self, client, auth_headers, test_epic, db_session):
        """Testa obtenção de resumo de revisão"""
        # Criar dados de teste
        comment = ReviewComment(
            entity_type="epic",
            entity_id=test_epic.epic_id,
            comment="Test comment",
            created_by=1
        )
        history = ReviewStatusHistory(
            entity_type="epic",
            entity_id=test_epic.epic_id,
            old_status="draft",
            new_status="in_review",
            changed_by=1,
            reason="Test reason"
        )
        db_session.add_all([comment, history])
        db_session.commit()
        
        response = client.get(f"/review/epic/{test_epic.epic_id}/summary", headers=auth_headers)
        assert response.status_code == 200
        
        data = response.json()
        assert "entity_info" in data
        assert "comments" in data
        assert "status_history" in data
        assert len(data["comments"]) == 1
        assert len(data["status_history"]) == 1
    
    def test_delete_review_comment(self, client, auth_headers, test_epic, db_session):
        """Testa remoção de comentário de revisão"""
        # Criar comentário
        comment = ReviewComment(
            entity_type="epic",
            entity_id=test_epic.epic_id,
            comment="Comment to delete",
            created_by=1
        )
        db_session.add(comment)
        db_session.commit()
        
        response = client.delete(f"/review/comments/{comment.comment_id}", headers=auth_headers)
        assert response.status_code == 204
        
        # Verificar se foi removido
        remaining_comments = db_session.query(ReviewComment).filter(
            ReviewComment.entity_type == "epic",
            ReviewComment.entity_id == test_epic.epic_id
        ).count()
        assert remaining_comments == 0
    
    def test_invalid_entity_type(self, client, auth_headers):
        """Testa erro com tipo de entidade inválido"""
        comment_data = {
            "entity_type": "invalid_type",
            "entity_id": 1,
            "comment": "Test comment",
            "is_suggestion": False
        }
        
        response = client.post("/review/comments", json=comment_data, headers=auth_headers)
        assert response.status_code == 400
    
    def test_entity_not_found(self, client, auth_headers):
        """Testa erro com entidade não encontrada"""
        comment_data = {
            "entity_type": "epic",
            "entity_id": 99999,
            "comment": "Test comment",
            "is_suggestion": False
        }
        
        response = client.post("/review/comments", json=comment_data, headers=auth_headers)
        assert response.status_code == 404
    
    def test_invalid_action(self, client, auth_headers, test_epic):
        """Testa erro com ação inválida"""
        action_data = {
            "action": "invalid_action",
            "comment": "Test comment"
        }
        
        response = client.post(f"/review/epic/{test_epic.epic_id}/action", json=action_data, headers=auth_headers)
        assert response.status_code == 400 
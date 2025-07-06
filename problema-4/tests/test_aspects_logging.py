"""
Testes automatizados para o aspecto de logging (log_operations) aplicado à criação de produtos.
Garante que operações importantes são registradas corretamente nos logs.
"""
import pytest
from unittest.mock import patch
from src.routers.product import create_product
from src.schemas.product import ProductCreate
from src.db.models import User
from sqlalchemy.orm import Session

@pytest.fixture
def fake_user():
    """
    Fixture que retorna um usuário admin fake para os testes.
    """
    user = User(user_id=1, email="test@example.com", name="Test User", password_hash="hash", is_active=True)
    user.role = 'admin'
    return user

@pytest.fixture
def fake_db():
    """
    Fixture que retorna um banco de dados fake para os testes.
    """
    class DummyDB(Session):
        def query(self, *args, **kwargs): return self
        def filter(self, *args, **kwargs): return self
        def first(self): return None
        def add(self, obj): pass
        def commit(self): pass
        def refresh(self, obj): pass
    return DummyDB()

def test_logging_aspect_called(fake_db, fake_user):
    """
    Garante que o aspecto de logging é chamado ao criar um produto.
    """
    product_data = ProductCreate(
        name="Produto Teste",
        description="desc",
        valueProposition="prop",
        platforms=["web"]
    )
    with patch("src.aspects.logging.logger.info") as mock_log:
        create_product(product_data, db=fake_db, current_user=fake_user)
        assert mock_log.called, "O aspecto de logging não foi chamado!"
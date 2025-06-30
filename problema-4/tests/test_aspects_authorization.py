import pytest
from fastapi import HTTPException
from src.routers.product import create_product
from src.schemas.product import ProductCreate
from src.db.models import User
from sqlalchemy.orm import Session

@pytest.fixture
def fake_db():
    class DummyDB(Session):
        def query(self, *args, **kwargs): return self
        def filter(self, *args, **kwargs): return self
        def first(self): return None
        def add(self, obj): pass
        def commit(self): pass
        def refresh(self, obj): pass
    return DummyDB()

@pytest.fixture
def product_data():
    return ProductCreate(
        name="Produto Teste",
        description="desc",
        valueProposition="prop",
        platforms=["web"]
    )

def test_authorization_allows_admin(fake_db, product_data):
    user = User(user_id=1, email="admin@example.com", name="Admin", password_hash="hash", is_active=True)
    user.role = 'admin'
    # Não deve levantar exceção
    create_product(product_data, db=fake_db, current_user=user)

def test_authorization_denies_non_admin(fake_db, product_data):
    user = User(user_id=2, email="user@example.com", name="User", password_hash="hash", is_active=True)
    user.role = 'user'
    with pytest.raises(HTTPException) as excinfo:
        create_product(product_data, db=fake_db, current_user=user)
    assert excinfo.value.status_code == 403
    assert "acesso negado" in str(excinfo.value.detail).lower()

def test_authorization_denies_no_user(fake_db, product_data):
    with pytest.raises(HTTPException) as excinfo:
        create_product(product_data, db=fake_db, current_user=None)
    assert excinfo.value.status_code == 403
    assert "acesso negado" in str(excinfo.value.detail).lower() 
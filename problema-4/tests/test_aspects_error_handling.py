# tests/test_aspects_error_handling.py
import pytest
from fastapi import HTTPException
from src.routers.product import create_product
from src.schemas.product import ProductCreate
from src.db.models import User
from sqlalchemy.orm import Session

class DummyDB(Session):
    def query(self, *args, **kwargs): return self
    def filter(self, *args, **kwargs): return self
    def first(self): return True  # Simula produto já existente

@pytest.fixture
def fake_user():
    user = User(user_id=1, email="test@example.com", name="Test User", password_hash="hash", is_active=True)
    user.role = 'admin'
    return user

def test_error_handling_aspect(fake_user):
    product_data = ProductCreate(
        name="Produto Teste",
        description="desc",
        valueProposition="prop",
        platforms=["web"]
    )
    db = DummyDB()
    with pytest.raises(HTTPException) as excinfo:
        create_product(product_data, db=db, current_user=fake_user)
    assert excinfo.value.status_code == 400
    assert "produto com este nome" in str(excinfo.value.detail).lower()
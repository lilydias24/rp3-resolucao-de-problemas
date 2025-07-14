"""
Testes automatizados para o aspecto de tratamento de erros (handle_errors) aplicado à criação de produtos.
Garante que exceções de negócio sejam convertidas corretamente em HTTPException.
"""
import pytest
from fastapi import HTTPException
from src.routers.product import create_product
from src.schemas.product import ProductCreate
from src.db.models import User, Product

@pytest.fixture
def admin_user():
    user = User(user_id=1, email="test@example.com", name="Test User", password_hash="hash", is_active=True)
    user.role = 'admin'
    return user

def test_error_handling_aspect(db_session, admin_user):
    product_data = ProductCreate(
        name="Produto Teste",
        description="desc",
        value_proposition="prop",
        platforms=["web"]
    )
    # Insere produto real para simular duplicidade
    existing_product = Product(
        name=product_data.name,
        description=product_data.description,
        value_proposition=product_data.value_proposition,
        platforms=product_data.platforms,
        created_by=admin_user.user_id
    )
    db_session.add(admin_user)
    db_session.add(existing_product)
    db_session.commit()
    with pytest.raises(HTTPException) as excinfo:
        create_product(product_data, db=db_session, current_user=admin_user)
    assert excinfo.value.status_code == 400
    assert "produto com este nome" in str(excinfo.value.detail).lower()
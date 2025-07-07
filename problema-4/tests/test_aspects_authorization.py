"""
Testes automatizados para o aspecto de autorização (require_role) aplicado à criação de produtos.
Garante que apenas usuários com papel 'admin' possam criar produtos.
"""
import pytest
from fastapi import HTTPException
from src.routers.product import create_product
from src.schemas.product import ProductCreate
from src.db.models import User

@pytest.fixture
def product_data():
    """
    Fixture que retorna dados de produto válidos para os testes.
    """
    return ProductCreate(
        name="Produto Teste",
        description="desc",
        valueProposition="prop",
        platforms=["web"]
    )

def test_authorization_allows_admin(db_session, product_data):
    """
    Garante que um usuário com papel 'admin' pode criar produtos (não levanta exceção).
    """
    user = User(user_id=1, email="admin@example.com", name="Admin", password_hash="hash", is_active=True)
    user.role = 'admin'
    db_session.add(user)
    db_session.commit()
    create_product(product_data, db=db_session, current_user=user)

def test_authorization_denies_non_admin(db_session, product_data):
    """
    Garante que um usuário sem papel 'admin' recebe HTTP 403 ao tentar criar produto.
    """
    user = User(user_id=2, email="user@example.com", name="User", password_hash="hash", is_active=True)
    user.role = 'user'
    db_session.add(user)
    db_session.commit()
    with pytest.raises(HTTPException) as excinfo:
        create_product(product_data, db=db_session, current_user=user)
    assert excinfo.value.status_code == 403
    assert "acesso negado" in str(excinfo.value.detail).lower()

def test_authorization_denies_no_user(db_session, product_data):
    """
    Garante que a ausência de usuário autenticado resulta em HTTP 403 ao criar produto.
    """
    with pytest.raises(HTTPException) as excinfo:
        create_product(product_data, db=db_session, current_user=None)
    assert excinfo.value.status_code == 403
    assert "acesso negado" in str(excinfo.value.detail).lower() 
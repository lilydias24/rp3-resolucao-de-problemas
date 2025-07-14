"""
Testes automatizados para as rotas e lógica de produtos da API.
Inclui testes de autenticação, validação e regras de negócio para criação de produtos.
"""
import pytest
from fastapi.testclient import TestClient

# Helper para obter o token de autenticação
def get_auth_token(client: TestClient) -> str:
    """
    Cria um usuário e faz login para obter um token de acesso.
    Args:
        client (TestClient): Cliente de teste FastAPI.
    Returns:
        str: Token JWT de autenticação.
    """
    user_data = {
        "email": "product_test_user@example.com",
        "name": "Product Test User",
        "password": "password123"
    }
    # Garante que o usuário exista
    client.post("/auth/register", json=user_data)
    
    # Faz login para obter o token
    login_data = {"username": user_data["email"], "password": user_data["password"]}
    response = client.post("/auth/login", data=login_data)
    return response.json()["access_token"]

def test_create_product_success(client: TestClient):
    """
    Testa a criação bem-sucedida de um produto com autenticação.
    """
    token = get_auth_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    product_data = {
        "name": "Meu Primeiro Produto",
        "description": "Uma descrição detalhada.",
        "value_proposition": "Resolver um problema importante.",
        "platforms": ["web", "mobile"]
    }
    response = client.post("/products", headers=headers, json=product_data)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == product_data["name"]
    assert "product_id" in data

def test_create_product_no_auth(client: TestClient):
    """
    Testa a falha ao tentar criar um produto sem autenticação.
    """
    product_data = {"name": "Produto Sem Auth", "description": "..."}
    response = client.post("/products", json=product_data)
    assert response.status_code == 401
    assert response.json()["detail"] in ["Não autenticado", "Not authenticated", "Credenciais inválidas"]

def test_create_product_duplicate_name(client: TestClient):
    """
    Testa a falha ao criar um produto com um nome que já existe para o mesmo usuário.
    """
    token = get_auth_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    product_data = {
        "name": "Produto Duplicado Teste",
        "description": "..."
    }
    # Primeira criação (deve funcionar)
    response1 = client.post("/products", headers=headers, json=product_data)
    assert response1.status_code == 201
    
    # Segunda criação (deve falhar)
    response2 = client.post("/products", headers=headers, json=product_data)
    assert response2.status_code == 400
    assert "Você já tem um produto com este nome" in response2.json()["detail"]

def test_create_product_invalid_data(client: TestClient):
    """
    Testa a falha ao criar um produto com dados inválidos (nome sem espaço).
    """
    token = get_auth_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    product_data = {"name": "ProdutoInvalido", "description": "..."}
    response = client.post("/products", headers=headers, json=product_data)
    assert response.status_code == 422  # Erro de validação do Pydantic 

def test_create_product(client):
    """
    Testa a criação de um novo produto via API.
    """
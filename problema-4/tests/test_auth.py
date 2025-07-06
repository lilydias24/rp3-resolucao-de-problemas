import pytest
from fastapi.testclient import TestClient

# Dados de teste para o usuário
USER_DATA = {
    "email": "test@example.com",
    "name": "Test User",
    "password": "password123"
}

def test_register_user_success(client: TestClient):
    """
    Testa o registro bem-sucedido de um novo usuário.
    """
    response = client.post("/auth/register", json=USER_DATA)
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == USER_DATA["email"]
    assert "user_id" in data

def test_register_user_duplicate_email(client: TestClient):
    """
    Testa a falha ao registrar um usuário com um e-mail que já existe.
    """
    # A primeira tentativa (no teste anterior) deve ter funcionado
    response = client.post("/auth/register", json=USER_DATA)
    assert response.status_code == 400
    assert "Email já cadastrado" in response.json()["detail"]

def test_login_success(client: TestClient):
    """
    Testa o login bem-sucedido de um usuário.
    """
    login_data = {
        "username": USER_DATA["email"],
        "password": USER_DATA["password"]
    }
    response = client.post("/auth/login", data=login_data)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_invalid_password(client: TestClient):
    """
    Testa a falha de login com uma senha incorreta.
    """
    login_data = {
        "username": USER_DATA["email"],
        "password": "wrongpassword"
    }
    response = client.post("/auth/login", data=login_data)
    assert response.status_code == 401
    assert "Credenciais inválidas" in response.json()["detail"]

def test_login_nonexistent_user(client: TestClient):
    """
    Testa a falha de login com um usuário que não existe.
    """
    login_data = {
        "username": "nouser@example.com",
        "password": "anypassword"
    }
    response = client.post("/auth/login", data=login_data)
    assert response.status_code == 401
    assert "Credenciais inválidas" in response.json()["detail"] 
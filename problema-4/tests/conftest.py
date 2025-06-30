import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from main import app
from src.db.base import Base
from src.db.session import get_db

# Configuração do banco de dados de teste (em memória)
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Cria as tabelas no banco de dados de teste
Base.metadata.create_all(bind=engine)

def override_get_db():
    """
    Dependência que substitui a original para usar o banco de dados de teste.
    """
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

# Aplica a substituição da dependência na aplicação
app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="module")
def client():
    """
    Fixture do Pytest que fornece um cliente de teste para a API.
    """
    with TestClient(app) as c:
        yield c 
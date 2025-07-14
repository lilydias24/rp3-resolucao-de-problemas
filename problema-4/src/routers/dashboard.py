from fastapi import APIRouter, Depends
from src.db.session import get_db
from src.db.models import Product, Epic, UserStory, Requirement
from sqlalchemy.orm import Session

router = APIRouter(prefix="/dashboard", tags=["dashboard"])

@router.get("/metrics")
def get_metrics(db: Session = Depends(get_db)):
    """
    Retorna métricas agregadas para o dashboard.
    """
    return {
        "totalProducts": db.query(Product).count(),
        "totalEpics": db.query(Epic).count(),
        "totalStories": db.query(UserStory).count(),
        "totalRequirements": db.query(Requirement).count(),
        "pendingReviews": db.query(UserStory).filter(UserStory.status == "draft").count(),
        "completedThisWeek": 0  # Implemente lógica real se desejar
    }

@router.get("/recent-products")
def get_recent_products(db: Session = Depends(get_db)):
    """
    Retorna os produtos mais recentes.
    """
    products = db.query(Product).order_by(Product.created_at.desc()).limit(5).all()
    return [
        {
            "id": p.product_id,
            "name": p.name,
            "description": p.description,
            "status": "active",  # Ajuste conforme sua lógica
            "epicsCount": len(p.epics),
            "storiesCount": sum(len(e.stories) for e in p.epics),
            "requirementsCount": 0,  # Implemente se desejar
            "lastActivity": str(p.updated_at or p.created_at),
            "progress": 50,  # Implemente lógica real
        }
        for p in products
    ]

@router.get("/recent-activities")
def get_recent_activities():
    """
    Retorna atividades recentes (mock, expanda conforme sua lógica).
    """
    return [
        {
            "id": "1",
            "type": "story_approved",
            "description": "5 histórias de usuário foram aprovadas",
            "timestamp": "há 30 minutos",
            "productName": "E-commerce Platform",
        },
        # ...adicione mais atividades reais
    ]

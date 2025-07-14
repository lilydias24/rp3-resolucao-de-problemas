"""
Aspecto para rastreamento automático de revisões de entidades.
Registra automaticamente mudanças em épicos, histórias de usuário e requisitos
na tabela revision_history.
"""

import logging
from functools import wraps
from sqlalchemy.orm import Session
from typing import Dict, Any, Optional
from src.db.models import RevisionHistory

logger = logging.getLogger(__name__)

def track_revisions(entity_type: str):
    """
    Aspecto para rastrear revisões de entidades.
    
    Args:
        entity_type (str): Tipo da entidade ('epic', 'user_story', 'requirement')
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Extrair a sessão do banco e o usuário atual dos argumentos
            db: Optional[Session] = None
            current_user = None
            entity_id = None
            
            # Procurar por db e current_user nos argumentos
            for arg in args:
                if isinstance(arg, Session):
                    db = arg
                elif hasattr(arg, 'user_id'):  # Assumindo que current_user tem user_id
                    current_user = arg
            
            # Procurar nos kwargs também
            if 'db' in kwargs:
                db = kwargs['db']
            if 'current_user' in kwargs:
                current_user = kwargs['current_user']
            
            # Extrair entity_id dos argumentos (pode estar em diferentes posições)
            for arg in args:
                if isinstance(arg, int):
                    entity_id = arg
                    break
            
            # Se não encontrou nos args, procurar nos kwargs
            if entity_id is None:
                for key, value in kwargs.items():
                    if key.endswith('_id') and isinstance(value, int):
                        entity_id = value
                        break
            
            # Se não conseguiu extrair informações necessárias, executar sem tracking
            if not db or not current_user or entity_id is None:
                logger.warning(f"Não foi possível extrair informações para tracking de revisão em {func.__name__}")
                return func(*args, **kwargs)
            
            # Obter o estado atual da entidade antes da mudança
            old_state = get_entity_state(db, entity_type, entity_id)
            
            # Executar a função original
            result = func(*args, **kwargs)
            
            # Obter o novo estado da entidade
            new_state = get_entity_state(db, entity_type, entity_id)
            
            # Registrar mudanças
            if old_state and new_state:
                record_changes(db, entity_type, entity_id, old_state, new_state, current_user.user_id)
            
            return result
        return wrapper
    return decorator

def get_entity_state(db: Session, entity_type: str, entity_id: int) -> Optional[Dict[str, Any]]:
    """
    Obtém o estado atual de uma entidade.
    
    Args:
        db (Session): Sessão do banco de dados
        entity_type (str): Tipo da entidade
        entity_id (int): ID da entidade
        
    Returns:
        Dict com os campos da entidade ou None se não encontrada
    """
    try:
        if entity_type == 'epic':
            from src.db.models import Epic
            entity = db.query(Epic).filter(Epic.epic_id == entity_id).first()
        elif entity_type == 'user_story':
            from src.db.models import UserStory
            entity = db.query(UserStory).filter(UserStory.story_id == entity_id).first()
        elif entity_type == 'requirement':
            from src.db.models import Requirement
            entity = db.query(Requirement).filter(Requirement.requirement_id == entity_id).first()
        else:
            logger.warning(f"Tipo de entidade não suportado: {entity_type}")
            return None
        
        if entity:
            # Converter para dict, excluindo campos internos
            state = {}
            for column in entity.__table__.columns:
                if column.name not in ['created_at', 'updated_at']:
                    value = getattr(entity, column.name)
                    state[column.name] = str(value) if value is not None else None
            return state
        
        return None
    except Exception as e:
        logger.error(f"Erro ao obter estado da entidade {entity_type} {entity_id}: {e}")
        return None

def record_changes(db: Session, entity_type: str, entity_id: int, 
                  old_state: Dict[str, Any], new_state: Dict[str, Any], 
                  changed_by: int, change_reason: str = "Edição via sistema"):
    """
    Registra mudanças na tabela revision_history.
    
    Args:
        db (Session): Sessão do banco de dados
        entity_type (str): Tipo da entidade
        entity_id (int): ID da entidade
        old_state (Dict): Estado anterior
        new_state (Dict): Estado novo
        changed_by (int): ID do usuário que fez a mudança
        change_reason (str): Motivo da mudança
    """
    try:
        # Comparar campos e registrar mudanças
        for field in old_state.keys():
            if field in new_state:
                old_value = old_state[field]
                new_value = new_state[field]
                
                # Se o valor mudou, registrar a mudança
                if old_value != new_value:
                    revision = RevisionHistory(
                        entity_type=entity_type,
                        entity_id=entity_id,
                        field_changed=field,
                        old_value=old_value,
                        new_value=new_value,
                        changed_by=changed_by,
                        change_reason=change_reason
                    )
                    db.add(revision)
        
        # Registrar mudanças em campos que existem apenas no novo estado
        for field in new_state.keys():
            if field not in old_state:
                revision = RevisionHistory(
                    entity_type=entity_type,
                    entity_id=entity_id,
                    field_changed=field,
                    old_value=None,
                    new_value=new_state[field],
                    changed_by=changed_by,
                    change_reason=change_reason
                )
                db.add(revision)
        
        db.commit()
        logger.info(f"Revisões registradas para {entity_type} {entity_id}")
        
    except Exception as e:
        logger.error(f"Erro ao registrar revisões para {entity_type} {entity_id}: {e}")
        db.rollback()

def get_revision_history(db: Session, entity_type: str, entity_id: int) -> list:
    """
    Obtém o histórico de revisões de uma entidade.
    
    Args:
        db (Session): Sessão do banco de dados
        entity_type (str): Tipo da entidade
        entity_id (int): ID da entidade
        
    Returns:
        Lista de revisões ordenadas por data
    """
    try:
        revisions = db.query(RevisionHistory).filter(
            RevisionHistory.entity_type == entity_type,
            RevisionHistory.entity_id == entity_id
        ).order_by(RevisionHistory.changed_at.desc()).all()
        
        return revisions
    except Exception as e:
        logger.error(f"Erro ao obter histórico de revisões para {entity_type} {entity_id}: {e}")
        return [] 
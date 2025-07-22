from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, ForeignKey, Boolean, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy import CheckConstraint
from .base import Base
from sqlalchemy.dialects.postgresql import ARRAY

"""
Define os modelos ORM do sistema para o SQLAlchemy.
Cada classe representa uma tabela do banco de dados.
"""

class User(Base):
    """
    Modelo ORM para usuários do sistema.
    Campos principais: user_id, email, password_hash, name, is_active, created_at, last_login, role.
    Relacionamentos: products (produtos criados pelo usuário).
    """
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    name = Column(String(100), nullable=False)
    is_active = Column(Boolean, default=True)
    role = Column(String(50), default='user')
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    last_login = Column(TIMESTAMP(timezone=True))
    
    products = relationship("Product", back_populates="owner")

class Product(Base):
    """
    Modelo ORM para produtos cadastrados no sistema.
    Campos principais: product_id, name, description, value_proposition, platforms, created_by, created_at, updated_at.
    Relacionamentos: owner (usuário criador), epics, personas.
    """
    __tablename__ = 'products'

    product_id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    value_proposition = Column(Text)
    platforms = Column(JSON)   # Ex: ['web', 'mobile']
    personas = Column(ARRAY(String), nullable=True)
    created_by = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True))
    
    owner = relationship("User", back_populates="products")
    epics = relationship("Epic", back_populates="product")
    personas_rel = relationship("Persona", back_populates="product")

class Persona(Base):
    """
    Modelo ORM para personas associadas a produtos.
    Campos principais: persona_id, product_id, name, description, characteristics.
    Relacionamentos: product, stories.
    """
    __tablename__ = 'personas'

    persona_id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('products.product_id'), nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    characteristics = Column(JSON)  # Para PostgreSQL (ou use Text em outros DBs)
    
    product = relationship("Product", back_populates="personas_rel")
    stories = relationship("UserStory", back_populates="persona")

class Epic(Base):
    """
    Modelo ORM para épicos (grandes funcionalidades) de um produto.
    Campos principais: epic_id, product_id, title, description, status, created_by, created_at, updated_at.
    Relacionamentos: product, stories.
    """
    __tablename__ = 'epics'

    epic_id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('products.product_id'), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    status = Column(String(50), server_default='draft')  # draft, in_review, approved, rejected, needs_revision, implemented
    created_by = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True))
    
    product = relationship("Product", back_populates="epics")
    stories = relationship("UserStory", back_populates="epic")

class UserStory(Base):
    """
    Modelo ORM para histórias de usuário.
    Campos principais: story_id, epic_id, persona_id, as_a, i_want, so_that, acceptance_criteria, priority, status, generated_by_llm, llm_prompt_used, created_by, created_at, updated_at.
    Relacionamentos: epic, persona, requirements.
    """
    __tablename__ = 'user_stories'

    story_id = Column(Integer, primary_key=True)
    epic_id = Column(Integer, ForeignKey('epics.epic_id'), nullable=False)
    persona_id = Column(Integer, ForeignKey('personas.persona_id'))
    as_a = Column(Text, nullable=False)
    i_want = Column(Text, nullable=False)
    so_that = Column(Text, nullable=False)
    acceptance_criteria = Column(JSON)
    priority = Column(Integer)
    status = Column(String(50), server_default='draft')
    generated_by_llm = Column(Boolean, default=False)
    llm_prompt_used = Column(Text)
    created_by = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True))
    
    epic = relationship("Epic", back_populates="stories")
    persona = relationship("Persona", back_populates="stories")
    requirements = relationship("Requirement", back_populates="story")

    __table_args__ = (
        CheckConstraint(
            "status IN ('draft', 'in_review', 'approved', 'rejected', 'needs_revision', 'implemented')",
            name='check_status'
        ),
        CheckConstraint(
            "priority BETWEEN 1 AND 5",
            name='check_priority'
        )
    )

class Requirement(Base):
    """
    Modelo ORM para requisitos associados a histórias de usuário.
    Campos principais: requirement_id, story_id, description, technical_details, priority, status, created_by, created_at, updated_at.
    Relacionamentos: story.
    """
    __tablename__ = 'requirements'

    requirement_id = Column(Integer, primary_key=True)
    story_id = Column(Integer, ForeignKey('user_stories.story_id'), nullable=False)
    description = Column(Text, nullable=False)
    technical_details = Column(Text)
    priority = Column(Integer)
    status = Column(String(50), server_default='draft')
    created_by = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True))
    
    story = relationship("UserStory", back_populates="requirements")

class Backlog(Base):
    """
    Modelo ORM para backlogs de produto.
    Campos principais: backlog_id, product_id, name, description, version, created_by, created_at, updated_at.
    Relacionamentos: items (itens do backlog).
    """
    __tablename__ = 'backlogs'

    backlog_id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('products.product_id'), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    version = Column(String(50))
    created_by = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True))
    
    items = relationship("BacklogItem", back_populates="backlog")

class BacklogItem(Base):
    """
    Modelo ORM para itens do backlog.
    Campos principais: item_id, backlog_id, story_id, requirement_id, position, sprint_planned.
    Relacionamentos: backlog, story, requirement.
    """
    __tablename__ = 'backlog_items'

    item_id = Column(Integer, primary_key=True)
    backlog_id = Column(Integer, ForeignKey('backlogs.backlog_id'), nullable=False)
    story_id = Column(Integer, ForeignKey('user_stories.story_id'))
    requirement_id = Column(Integer, ForeignKey('requirements.requirement_id'))
    position = Column(Integer, nullable=False)
    sprint_planned = Column(String(100))
    
    # Relacionamentos
    backlog = relationship("Backlog", back_populates="items")
    story = relationship("UserStory")
    requirement = relationship("Requirement")
    
    # Constraint para garantir que tenha pelo menos uma referência
    __table_args__ = (
        CheckConstraint(
            'story_id IS NOT NULL OR requirement_id IS NOT NULL',
            name='check_reference'
        ),
    )

class RevisionHistory(Base):
    """
    Modelo ORM para histórico de revisões de entidades.
    Campos principais: revision_id, entity_type, entity_id, field_changed, old_value, new_value, changed_by, change_reason, changed_at.
    """
    __tablename__ = 'revision_history'

    revision_id = Column(Integer, primary_key=True)
    entity_type = Column(String(50), nullable=False)  # 'epic', 'user_story', etc.
    entity_id = Column(Integer, nullable=False)
    field_changed = Column(String(100), nullable=False)
    old_value = Column(Text)
    new_value = Column(Text)
    changed_by = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    change_reason = Column(Text)
    changed_at = Column(TIMESTAMP(timezone=True), server_default=func.now())

class LLMInteraction(Base):
    """
    Modelo ORM para interações com LLMs (Large Language Models).
    Campos principais: interaction_id, user_id, product_id, prompt, response, model_used, tokens_used, entity_type, entity_id, created_at.
    """
    __tablename__ = 'llm_interactions'

    interaction_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    product_id = Column(Integer, ForeignKey('products.product_id'))
    prompt = Column(Text, nullable=False)
    response = Column(Text, nullable=False)
    model_used = Column(String(100), nullable=False)
    tokens_used = Column(Integer)
    entity_type = Column(String(50))  # 'epic', 'user_story', etc.
    entity_id = Column(Integer)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())

class SystemLog(Base):
    """
    Modelo ORM para logs do sistema.
    Campos principais: log_id, action, user_id, details, level, created_at.
    """
    __tablename__ = 'system_logs'
    
    log_id = Column(Integer, primary_key=True)
    action = Column(String(100), nullable=False)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    details = Column(Text)
    level = Column(String(20))  # INFO, WARNING, ERROR
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())

class ReviewComment(Base):
    """
    Modelo ORM para comentários de revisão em entidades.
    Campos principais: comment_id, entity_type, entity_id, comment, is_suggestion, created_by, created_at.
    """
    __tablename__ = 'review_comments'
    
    comment_id = Column(Integer, primary_key=True)
    entity_type = Column(String(50), nullable=False)  # 'epic', 'user_story', 'requirement'
    entity_id = Column(Integer, nullable=False)
    comment = Column(Text, nullable=False)
    is_suggestion = Column(Boolean, default=False)
    suggested_changes = Column(Text)
    created_by = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True))
    
    # Relacionamento com usuário
    user = relationship("User")

class ReviewStatusHistory(Base):
    """
    Modelo ORM para histórico de mudanças de status de revisão.
    Campos principais: history_id, entity_type, entity_id, old_status, new_status, changed_by, reason, changed_at.
    """
    __tablename__ = 'review_status_history'
    
    history_id = Column(Integer, primary_key=True)
    entity_type = Column(String(50), nullable=False)  # 'epic', 'user_story', 'requirement'
    entity_id = Column(Integer, nullable=False)
    old_status = Column(String(50))
    new_status = Column(String(50), nullable=False)
    changed_by = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    reason = Column(Text)
    changed_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    
    # Relacionamento com usuário
    user = relationship("User")
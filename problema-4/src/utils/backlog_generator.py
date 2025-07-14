"""
Serviço para geração automática de backlog a partir de histórias e requisitos aprovados.
"""
from sqlalchemy.orm import Session
from sqlalchemy import and_, desc, func
from typing import List, Dict, Any, Tuple
from datetime import datetime, timedelta
from src.db.models import Product, Epic, UserStory, Requirement, Backlog, BacklogItem
from src.schemas.backlog_generation import (
    BacklogGenerationRequest, BacklogGenerationOptions, GenerationStrategy,
    BacklogItemInfo, BacklogGenerationResponse, BacklogGenerationPreview
)
from src.schemas.review import ReviewStatus
import logging

logger = logging.getLogger(__name__)

class BacklogGenerator:
    """Serviço para geração automática de backlog"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def generate_backlog(self, request: BacklogGenerationRequest, options: BacklogGenerationOptions = None) -> BacklogGenerationResponse:
        """
        Gera um backlog automaticamente baseado nos parâmetros fornecidos.
        """
        if options is None:
            options = BacklogGenerationOptions()
        
        # Validar se o produto existe
        product = self.db.query(Product).filter(Product.product_id == request.product_id).first()
        if not product:
            raise ValueError(f"Produto com ID {request.product_id} não encontrado")
        
        # Buscar itens aprovados
        approved_items = self._get_approved_items(request)
        
        if not approved_items['stories'] and not approved_items['requirements']:
            raise ValueError("Nenhuma história de usuário ou requisito aprovado encontrado")
        
        # Aplicar estratégia de geração
        prioritized_items = self._apply_generation_strategy(
            approved_items, request, options
        )
        
        # Limitar número de itens se especificado
        if request.max_items:
            prioritized_items = prioritized_items[:request.max_items]
        
        # Criar o backlog
        backlog = self._create_backlog(request, product)
        
        # Criar itens do backlog
        backlog_items = self._create_backlog_items(backlog.backlog_id, prioritized_items, request)
        
        # Preparar resposta
        return self._prepare_response(backlog, backlog_items, request, options)
    
    def preview_generation(self, request: BacklogGenerationRequest, options: BacklogGenerationOptions = None) -> BacklogGenerationPreview:
        """
        Gera um preview da geração sem criar o backlog.
        """
        if options is None:
            options = BacklogGenerationOptions()
        
        # Buscar itens aprovados
        approved_items = self._get_approved_items(request)
        
        # Aplicar estratégia de geração
        prioritized_items = self._apply_generation_strategy(
            approved_items, request, options
        )
        
        # Limitar para preview (primeiros 10 itens)
        preview_items = prioritized_items[:10]
        
        return BacklogGenerationPreview(
            estimated_items=len(prioritized_items),
            estimated_stories=len([item for item in prioritized_items if item['type'] == 'story']),
            estimated_requirements=len([item for item in prioritized_items if item['type'] == 'requirement']),
            preview_items=[self._create_item_info(item, idx + 1) for idx, item in enumerate(preview_items)],
            strategy=request.strategy,
            options=options
        )
    
    def _get_approved_items(self, request: BacklogGenerationRequest) -> Dict[str, List]:
        """
        Busca histórias de usuário e requisitos aprovados.
        """
        items = {'stories': [], 'requirements': []}
        
        if request.include_stories:
            stories_query = self.db.query(UserStory).join(Epic).filter(
                and_(
                    Epic.product_id == request.product_id,
                    UserStory.status == ReviewStatus.APPROVED.value
                )
            )
            
            if request.min_priority:
                stories_query = stories_query.filter(UserStory.priority >= request.min_priority)
            
            items['stories'] = stories_query.all()
        
        if request.include_requirements:
            requirements_query = self.db.query(Requirement).join(UserStory).join(Epic).filter(
                and_(
                    Epic.product_id == request.product_id,
                    Requirement.status == ReviewStatus.APPROVED.value
                )
            )
            
            if request.min_priority:
                requirements_query = requirements_query.filter(Requirement.priority >= request.min_priority)
            
            items['requirements'] = requirements_query.all()
        
        return items
    
    def _apply_generation_strategy(self, approved_items: Dict[str, List], request: BacklogGenerationRequest, options: BacklogGenerationOptions) -> List[Dict]:
        """
        Aplica a estratégia de geração para priorizar e organizar os itens.
        """
        all_items = []
        
        # Converter histórias para formato padrão
        for story in approved_items['stories']:
            all_items.append({
                'type': 'story',
                'id': story.story_id,
                'title': f"{story.as_a} - {story.i_want}",
                'description': story.so_that,
                'priority': story.priority or 3,
                'epic_id': story.epic_id,
                'epic_title': story.epic.title if story.epic else None,
                'created_at': story.created_at,
                'weight': options.story_weight,
                'acceptance_criteria': story.acceptance_criteria
            })
        
        # Converter requisitos para formato padrão
        for req in approved_items['requirements']:
            all_items.append({
                'type': 'requirement',
                'id': req.requirement_id,
                'title': req.description[:100] + "..." if len(req.description) > 100 else req.description,
                'description': req.description,
                'priority': req.priority or 3,
                'epic_id': req.story.epic_id if req.story else None,
                'epic_title': req.story.epic.title if req.story and req.story.epic else None,
                'created_at': req.created_at,
                'weight': options.requirement_weight,
                'technical_details': req.technical_details
            })
        
        # Aplicar estratégia específica
        if request.strategy == GenerationStrategy.PRIORITY_BASED:
            return self._priority_based_strategy(all_items, options)
        elif request.strategy == GenerationStrategy.EPIC_BASED:
            return self._epic_based_strategy(all_items, request.group_by_epic)
        elif request.strategy == GenerationStrategy.STORY_ONLY:
            return [item for item in all_items if item['type'] == 'story']
        elif request.strategy == GenerationStrategy.REQUIREMENT_ONLY:
            return [item for item in all_items if item['type'] == 'requirement']
        elif request.strategy == GenerationStrategy.MIXED:
            return self._mixed_strategy(all_items, options)
        else:
            return all_items
    
    def _priority_based_strategy(self, items: List[Dict], options: BacklogGenerationOptions) -> List[Dict]:
        """
        Estratégia baseada em prioridade com fatores adicionais.
        """
        for item in items:
            # Calcular score baseado em prioridade
            score = item['priority'] * options.priority_multiplier * item['weight']
            
            # Bônus para itens recentes
            if options.recent_bonus > 0:
                days_old = (datetime.utcnow() - item['created_at']).days
                if days_old <= 7:  # Itens da última semana
                    score += options.recent_bonus
            
            # Fator de complexidade (baseado no tamanho da descrição)
            if options.complexity_factor:
                complexity = min(len(item['description']) / 100, 2.0)  # Máximo 2x
                score *= complexity
            
            item['score'] = score
        
        # Ordenar por score (maior primeiro)
        return sorted(items, key=lambda x: x['score'], reverse=True)
    
    def _epic_based_strategy(self, items: List[Dict], group_by_epic: bool) -> List[Dict]:
        """
        Estratégia baseada em épicos.
        """
        if not group_by_epic:
            # Ordenar por épico e depois por prioridade
            return sorted(items, key=lambda x: (x['epic_id'] or 0, x['priority']), reverse=True)
        
        # Agrupar por épico e ordenar épicos por prioridade média
        epic_groups = {}
        for item in items:
            epic_id = item['epic_id'] or 0
            if epic_id not in epic_groups:
                epic_groups[epic_id] = []
            epic_groups[epic_id].append(item)
        
        # Calcular prioridade média de cada épico
        epic_priorities = {}
        for epic_id, epic_items in epic_groups.items():
            avg_priority = sum(item['priority'] for item in epic_items) / len(epic_items)
            epic_priorities[epic_id] = avg_priority
        
        # Ordenar épicos por prioridade média
        sorted_epics = sorted(epic_priorities.items(), key=lambda x: x[1], reverse=True)
        
        # Montar lista final ordenada por épico
        result = []
        for epic_id, _ in sorted_epics:
            epic_items = sorted(epic_groups[epic_id], key=lambda x: x['priority'], reverse=True)
            result.extend(epic_items)
        
        return result
    
    def _mixed_strategy(self, items: List[Dict], options: BacklogGenerationOptions) -> List[Dict]:
        """
        Estratégia mista que alterna entre histórias e requisitos.
        """
        stories = [item for item in items if item['type'] == 'story']
        requirements = [item for item in items if item['type'] == 'requirement']
        
        # Ordenar cada tipo por prioridade
        stories = sorted(stories, key=lambda x: x['priority'], reverse=True)
        requirements = sorted(requirements, key=lambda x: x['priority'], reverse=True)
        
        # Intercalar histórias e requisitos
        result = []
        max_len = max(len(stories), len(requirements))
        
        for i in range(max_len):
            if i < len(stories):
                result.append(stories[i])
            if i < len(requirements):
                result.append(requirements[i])
        
        return result
    
    def _create_backlog(self, request: BacklogGenerationRequest, product: Product) -> Backlog:
        """
        Cria o backlog no banco de dados.
        """
        backlog = Backlog(
            product_id=request.product_id,
            name=request.name,
            description=request.description or f"Backlog gerado automaticamente para {product.name}",
            version=request.version or "1.0",
            created_by=product.created_by
        )
        
        self.db.add(backlog)
        self.db.commit()
        self.db.refresh(backlog)
        
        return backlog
    
    def _create_backlog_items(self, backlog_id: int, items: List[Dict], request: BacklogGenerationRequest) -> List[BacklogItem]:
        """
        Cria os itens do backlog no banco de dados.
        """
        backlog_items = []
        
        for position, item in enumerate(items, 1):
            backlog_item = BacklogItem(
                backlog_id=backlog_id,
                story_id=item['id'] if item['type'] == 'story' else None,
                requirement_id=item['id'] if item['type'] == 'requirement' else None,
                position=position
            )
            
            self.db.add(backlog_item)
            backlog_items.append(backlog_item)
        
        self.db.commit()
        
        # Refresh para obter os IDs gerados
        for item in backlog_items:
            self.db.refresh(item)
        
        return backlog_items
    
    def _create_item_info(self, item: Dict, position: int) -> BacklogItemInfo:
        """
        Cria informações de item para a resposta.
        """
        return BacklogItemInfo(
            item_id=item['id'],
            item_type=item['type'],
            title=item['title'],
            description=item['description'],
            priority=item['priority'],
            epic_title=item['epic_title'],
            estimated_effort=self._estimate_effort(item),
            business_value=self._calculate_business_value(item),
            position=position
        )
    
    def _estimate_effort(self, item: Dict) -> str:
        """
        Estima o esforço baseado na complexidade do item.
        """
        description_length = len(item['description'])
        
        if item['type'] == 'story':
            if description_length < 100:
                return "1-2 pontos"
            elif description_length < 300:
                return "3-5 pontos"
            else:
                return "8-13 pontos"
        else:  # requirement
            if description_length < 150:
                return "1-2 pontos"
            elif description_length < 400:
                return "3-5 pontos"
            else:
                return "8-13 pontos"
    
    def _calculate_business_value(self, item: Dict) -> int:
        """
        Calcula o valor de negócio baseado na prioridade e tipo.
        """
        base_value = item['priority'] * 10
        
        if item['type'] == 'story':
            return base_value * 2  # Histórias têm mais valor de negócio
        else:
            return base_value
    
    def _prepare_response(self, backlog: Backlog, backlog_items: List[BacklogItem], request: BacklogGenerationRequest, options: BacklogGenerationOptions) -> BacklogGenerationResponse:
        """
        Prepara a resposta da geração.
        """
        stories_count = len([item for item in backlog_items if item.story_id is not None])
        requirements_count = len([item for item in backlog_items if item.requirement_id is not None])
        
        # Buscar informações detalhadas dos itens
        items_info = []
        for item in backlog_items:
            if item.story_id:
                story = self.db.query(UserStory).filter(UserStory.story_id == item.story_id).first()
                if story:
                    items_info.append(self._create_item_info({
                        'id': story.story_id,
                        'type': 'story',
                        'title': f"{story.as_a} - {story.i_want}",
                        'description': story.so_that,
                        'priority': story.priority or 3,
                        'epic_title': story.epic.title if story.epic else None
                    }, item.position))
            elif item.requirement_id:
                req = self.db.query(Requirement).filter(Requirement.requirement_id == item.requirement_id).first()
                if req:
                    items_info.append(self._create_item_info({
                        'id': req.requirement_id,
                        'type': 'requirement',
                        'title': req.description[:100] + "..." if len(req.description) > 100 else req.description,
                        'description': req.description,
                        'priority': req.priority or 3,
                        'epic_title': req.story.epic.title if req.story and req.story.epic else None
                    }, item.position))
        
        summary = {
            'total_effort_estimated': f"{len(items_info) * 3}-{len(items_info) * 8} pontos",
            'high_priority_items': len([item for item in items_info if item.priority >= 4]),
            'medium_priority_items': len([item for item in items_info if 2 <= item.priority <= 3]),
            'low_priority_items': len([item for item in items_info if item.priority <= 1]),
            'epics_covered': len(set(item.epic_title for item in items_info if item.epic_title))
        }
        
        return BacklogGenerationResponse(
            backlog_id=backlog.backlog_id,
            backlog_name=backlog.name,
            total_items=len(items_info),
            stories_count=stories_count,
            requirements_count=requirements_count,
            generation_strategy=request.strategy,
            generation_options=options,
            items=items_info,
            summary=summary,
            created_at=backlog.created_at
        ) 
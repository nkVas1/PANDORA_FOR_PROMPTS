import json
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from app.db.models import Prompt, Tag, Project, ProcessEntry, Task
from app.models.schemas import (
    PromptCreate, PromptUpdate, TagCreate, AutoTagResult,
    ProjectCreate, ProjectUpdate, ProcessEntry as ProcessEntrySchema,
    TaskEntry
)
from app.utils.auto_tagger import AutoTagger

auto_tagger = AutoTagger()


class PromptService:
    """Сервис для работы с промптами"""
    
    @staticmethod
    def create_prompt(db: Session, prompt: PromptCreate) -> Prompt:
        """Создать новый промпт"""
        db_prompt = Prompt(
            title=prompt.title,
            content=prompt.content,
            description=prompt.description,
            category=prompt.category.value,
            version=prompt.version
        )
        
        # Добавляем теги
        if prompt.tag_ids:
            tags = db.query(Tag).filter(Tag.id.in_(prompt.tag_ids)).all()
            db_prompt.tags = tags
        
        db.add(db_prompt)
        db.commit()
        db.refresh(db_prompt)
        return db_prompt
    
    @staticmethod
    def get_prompt(db: Session, prompt_id: int) -> Optional[Prompt]:
        """Получить промпт по ID"""
        return db.query(Prompt).filter(Prompt.id == prompt_id).first()
    
    @staticmethod
    def get_all_prompts(db: Session, skip: int = 0, limit: int = 100) -> List[Prompt]:
        """Получить все промпты с пагинацией"""
        return db.query(Prompt).offset(skip).limit(limit).all()
    
    @staticmethod
    def search_prompts(
        db: Session,
        query: str,
        category: Optional[str] = None,
        tags: Optional[List[str]] = None,
        skip: int = 0,
        limit: int = 100
    ) -> tuple[int, List[Prompt]]:
        """Поиск промптов"""
        q = db.query(Prompt)
        
        # Поиск по заголовку и содержимому
        if query:
            q = q.filter(or_(
                Prompt.title.ilike(f"%{query}%"),
                Prompt.content.ilike(f"%{query}%"),
                Prompt.description.ilike(f"%{query}%")
            ))
        
        # Фильтр по категории
        if category:
            q = q.filter(Prompt.category == category)
        
        # Фильтр по тегам
        if tags:
            q = q.join(Prompt.tags).filter(Tag.name.in_(tags)).distinct()
        
        total = q.count()
        results = q.offset(skip).limit(limit).all()
        
        return total, results
    
    @staticmethod
    def update_prompt(db: Session, prompt_id: int, prompt_update: PromptUpdate) -> Optional[Prompt]:
        """Обновить промпт"""
        db_prompt = db.query(Prompt).filter(Prompt.id == prompt_id).first()
        if not db_prompt:
            return None
        
        update_data = prompt_update.dict(exclude_unset=True)
        tag_ids = update_data.pop('tag_ids', None)
        
        for field, value in update_data.items():
            if value is not None:
                setattr(db_prompt, field, value)
        
        if tag_ids is not None:
            tags = db.query(Tag).filter(Tag.id.in_(tag_ids)).all()
            db_prompt.tags = tags
        
        db.add(db_prompt)
        db.commit()
        db.refresh(db_prompt)
        return db_prompt
    
    @staticmethod
    def delete_prompt(db: Session, prompt_id: int) -> bool:
        """Удалить промпт"""
        db_prompt = db.query(Prompt).filter(Prompt.id == prompt_id).first()
        if not db_prompt:
            return False
        
        db.delete(db_prompt)
        db.commit()
        return True
    
    @staticmethod
    def increment_usage(db: Session, prompt_id: int):
        """Увеличить счётчик использования"""
        db_prompt = db.query(Prompt).filter(Prompt.id == prompt_id).first()
        if db_prompt:
            db_prompt.usage_count += 1
            db.commit()


class TagService:
    """Сервис для работы с тегами"""
    
    @staticmethod
    def create_tag(db: Session, tag: TagCreate) -> Tag:
        """Создать новый тег"""
        db_tag = Tag(name=tag.name, color=tag.color)
        db.add(db_tag)
        db.commit()
        db.refresh(db_tag)
        return db_tag
    
    @staticmethod
    def get_all_tags(db: Session) -> List[Tag]:
        """Получить все теги"""
        return db.query(Tag).order_by(Tag.usage_count.desc()).all()
    
    @staticmethod
    def get_tag(db: Session, tag_id: int) -> Optional[Tag]:
        """Получить тег по ID"""
        return db.query(Tag).filter(Tag.id == tag_id).first()
    
    @staticmethod
    def get_tag_by_name(db: Session, tag_name: str) -> Optional[Tag]:
        """Получить тег по имени"""
        return db.query(Tag).filter(Tag.name.ilike(tag_name)).first()
    
    @staticmethod
    def delete_tag(db: Session, tag_id: int) -> bool:
        """Удалить тег"""
        db_tag = db.query(Tag).filter(Tag.id == tag_id).first()
        if not db_tag:
            return False
        
        db.delete(db_tag)
        db.commit()
        return True


class AutoTaggingService:
    """Сервис для автоматического тегирования"""
    
    @staticmethod
    def auto_tag_prompt(db: Session, prompt_id: int) -> AutoTagResult:
        """Автоматически тегировать промпт"""
        db_prompt = db.query(Prompt).filter(Prompt.id == prompt_id).first()
        if not db_prompt:
            return None
        
        # Получаем предложенные теги и категорию
        suggested = auto_tagger.tag_prompt(db_prompt.title, db_prompt.content)
        
        result = AutoTagResult(
            prompt_id=prompt_id,
            suggested_tags=suggested['tags'],
            category_suggestion=suggested['category'],
            category_confidence=suggested['category_confidence']
        )
        
        return result


class ProjectService:
    """Сервис для работы с проектами"""
    
    @staticmethod
    def create_project(db: Session, project: ProjectCreate) -> Project:
        """Создать новый проект"""
        db_project = Project(
            name=project.name,
            description=project.description,
            status=project.status
        )
        db.add(db_project)
        db.commit()
        db.refresh(db_project)
        return db_project
    
    @staticmethod
    def get_project(db: Session, project_id: int) -> Optional[Project]:
        """Получить проект по ID"""
        return db.query(Project).filter(Project.id == project_id).first()
    
    @staticmethod
    def get_all_projects(db: Session) -> List[Project]:
        """Получить все проекты"""
        return db.query(Project).order_by(Project.updated_at.desc()).all()
    
    @staticmethod
    def update_project(db: Session, project_id: int, project_update: ProjectUpdate) -> Optional[Project]:
        """Обновить проект"""
        db_project = db.query(Project).filter(Project.id == project_id).first()
        if not db_project:
            return None
        
        update_data = project_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_project, field, value)
        
        db.add(db_project)
        db.commit()
        db.refresh(db_project)
        return db_project
    
    @staticmethod
    def delete_project(db: Session, project_id: int) -> bool:
        """Удалить проект"""
        db_project = db.query(Project).filter(Project.id == project_id).first()
        if not db_project:
            return False
        
        db.delete(db_project)
        db.commit()
        return True
    
    @staticmethod
    def add_process_entry(db: Session, project_id: int, entry: str) -> ProcessEntry:
        """Добавить запись в процесс"""
        db_entry = ProcessEntry(project_id=project_id, entry=entry)
        db.add(db_entry)
        db.commit()
        db.refresh(db_entry)
        return db_entry
    
    @staticmethod
    def add_task(db: Session, project_id: int, task: TaskEntry) -> Task:
        """Добавить задачу к проекту"""
        db_task = Task(
            project_id=project_id,
            title=task.title,
            description=task.description,
            status=task.status,
            priority=task.priority,
            due_date=task.due_date
        )
        db.add(db_task)
        db.commit()
        db.refresh(db_task)
        return db_task
    
    @staticmethod
    def update_task(db: Session, task_id: int, task_update: dict) -> Optional[Task]:
        """Обновить задачу"""
        db_task = db.query(Task).filter(Task.id == task_id).first()
        if not db_task:
            return None
        
        for field, value in task_update.items():
            if value is not None:
                setattr(db_task, field, value)
        
        db.add(db_task)
        db.commit()
        db.refresh(db_task)
        return db_task

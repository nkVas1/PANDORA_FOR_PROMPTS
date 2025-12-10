from sqlalchemy import Column, Integer, String, Text, DateTime, Float, Table, ForeignKey, Boolean
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()

# Association table для промптов и тегов
prompt_tags = Table(
    'prompt_tags',
    Base.metadata,
    Column('prompt_id', Integer, ForeignKey('prompts.id', ondelete='CASCADE')),
    Column('tag_id', Integer, ForeignKey('tags.id', ondelete='CASCADE'))
)


class Tag(Base):
    """Модель тега"""
    __tablename__ = "tags"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, index=True, nullable=False)
    color = Column(String(7), default="#3B82F6")
    usage_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    prompts = relationship(
        "Prompt",
        secondary=prompt_tags,
        back_populates="tags"
    )


class Prompt(Base):
    """Модель промпта с расширенными метаданными"""
    __tablename__ = "prompts"
    
    id = Column(Integer, primary_key=True)
    title = Column(String(255), index=True, nullable=False)
    content = Column(Text, nullable=False)
    description = Column(Text)
    category = Column(String(50), index=True, default="custom")
    subcategory = Column(String(50), index=True)  # Подкатегория для иерархии
    emoji = Column(String(10))  # Эмодзи для категории
    version = Column(String(20), default="1.0")
    difficulty = Column(String(50), default="intermediate")  # beginner, intermediate, advanced
    context_window = Column(String(50))  # small, medium, large
    models = Column(Text)  # JSON array: ["gpt-4", "claude-3"]
    use_cases = Column(Text)  # JSON array: ["use_case_1", "use_case_2"]
    examples = Column(Text)  # JSON array: ["example1.md", "example2.md"]
    changelog = Column(Text)  # История изменений (версионирование)
    rating = Column(Float, default=0.0)  # Рейтинг от 0 до 5
    usage_count = Column(Integer, default=0)
    author = Column(String(255))  # Автор промта
    author_url = Column(String(500))  # URL автора (GitHub profile и т.д.)
    imported_from = Column(String(255))  # Источник импорта
    keywords = Column(Text)  # JSON array: ["keyword1", "keyword2"] для поиска
    is_featured = Column(Boolean, default=False)
    is_experimental = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    tags = relationship(
        "Tag",
        secondary=prompt_tags,
        back_populates="prompts",
        cascade="save-update"
    )


class Project(Base):
    """Модель проекта"""
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    status = Column(String(50), default="active")  # active, paused, completed
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    process_entries = relationship("ProcessEntry", back_populates="project", cascade="all, delete-orphan")
    tasks = relationship("Task", back_populates="project", cascade="all, delete-orphan")


class ProcessEntry(Base):
    """Модель записи процесса разработки"""
    __tablename__ = "process_entries"
    
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('projects.id', ondelete='CASCADE'), nullable=False)
    entry = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    
    project = relationship("Project", back_populates="process_entries")


class Task(Base):
    """Модель задачи проекта"""
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('projects.id', ondelete='CASCADE'), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    status = Column(String(50), default="todo")  # todo, in_progress, done
    priority = Column(String(50), default="medium")  # low, medium, high
    due_date = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    project = relationship("Project", back_populates="tasks")

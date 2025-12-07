from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
from enum import Enum


class CategoryEnum(str, Enum):
    """Категории промптов"""
    DEVELOPMENT = "development"
    WRITING = "writing"
    ANALYSIS = "analysis"
    DESIGN = "design"
    MARKETING = "marketing"
    DATA = "data"
    IMPORT = "import"
    PROJECT = "project"
    CUSTOM = "custom"


class TagBase(BaseModel):
    """Базовая схема для тега"""
    name: str = Field(..., min_length=1, max_length=50)
    color: Optional[str] = Field(default="#3B82F6", description="Цвет тега в hex")


class TagCreate(TagBase):
    pass


class Tag(TagBase):
    id: int
    usage_count: int = 0
    
    class Config:
        from_attributes = True


class PromptBase(BaseModel):
    """Базовая схема для промпта"""
    title: str = Field(..., min_length=1, max_length=255)
    content: str = Field(..., min_length=1)
    description: Optional[str] = None
    category: CategoryEnum = CategoryEnum.CUSTOM
    version: str = "1.0"


class PromptCreate(PromptBase):
    tag_ids: Optional[List[int]] = []


class PromptUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    description: Optional[str] = None
    category: Optional[CategoryEnum] = None
    version: Optional[str] = None
    tag_ids: Optional[List[int]] = None


class Prompt(PromptBase):
    id: int
    tags: List[Tag] = []
    usage_count: int = 0
    created_at: datetime
    updated_at: datetime
    imported_from: Optional[str] = None
    
    class Config:
        from_attributes = True


class ProjectBase(BaseModel):
    """Базовая схема для проекта"""
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    status: str = Field(default="active", description="active, paused, completed")


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None


class ProcessEntry(BaseModel):
    """Запись процесса разработки"""
    date: datetime
    entry: str
    project_id: int


class TaskEntry(BaseModel):
    """Запись задачи"""
    task_id: Optional[int] = None
    title: str
    description: Optional[str] = None
    status: str = Field(default="todo", description="todo, in_progress, done")
    priority: str = Field(default="medium", description="low, medium, high")
    project_id: int
    due_date: Optional[datetime] = None


class Project(ProjectBase):
    id: int
    created_at: datetime
    updated_at: datetime
    process_entries: List[ProcessEntry] = []
    tasks: List[TaskEntry] = []
    
    class Config:
        from_attributes = True


class PromptBulkImport(BaseModel):
    """Схема для массовой загрузки промптов"""
    import_source: str = Field(..., description="Источник импорта (e.g., 'awesome-prompts', 'agent-library')")
    prompts: List[PromptCreate] = Field(..., min_items=1)


class AutoTagResult(BaseModel):
    """Результат автотегирования"""
    prompt_id: int
    suggested_tags: List[dict] = Field(..., description="Список тегов с уверенностью [{'name': 'tag', 'confidence': 0.95}]")
    category_suggestion: Optional[str] = None
    category_confidence: float = 0.0


class SearchQuery(BaseModel):
    """Запрос поиска"""
    q: str = Field(..., min_length=1)
    category: Optional[CategoryEnum] = None
    tags: Optional[List[str]] = []
    limit: int = Field(default=20, le=100)
    offset: int = Field(default=0, ge=0)


class SearchResult(BaseModel):
    """Результат поиска"""
    total: int
    results: List[Prompt]

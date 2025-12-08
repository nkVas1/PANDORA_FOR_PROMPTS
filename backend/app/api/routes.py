from fastapi import APIRouter, Depends, HTTPException, Query, File, UploadFile
from sqlalchemy.orm import Session
from typing import List
import json
from app.db import get_db
from app.models import schemas
from app.services.database import (
    PromptService, TagService, ProjectService, AutoTaggingService
)
from app.services.autotagging import AutoTaggingService as ATS
from app.services.file_service import FileService
from app.services.keyword_analyzer import analyzer as keyword_analyzer
from app.utils.importer import PromptImporter

router = APIRouter(prefix="/api", tags=["prompts"])


# ================ PROMPTS ENDPOINTS ================

@router.post("/prompts", response_model=schemas.Prompt)
def create_prompt(prompt: schemas.PromptCreate, db: Session = Depends(get_db)):
    """Создать новый промпт"""
    return PromptService.create_prompt(db, prompt)


@router.get("/prompts", response_model=List[schemas.Prompt])
def list_prompts(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, le=1000),
    db: Session = Depends(get_db)
):
    """Получить список всех промптов"""
    return PromptService.get_all_prompts(db, skip, limit)


@router.get("/prompts/search")
def search_prompts(
    q: str = Query(..., min_length=1),
    category: str = Query(None),
    tags: List[str] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, le=1000),
    db: Session = Depends(get_db)
):
    """Поиск промптов"""
    total, results = PromptService.search_prompts(
        db, q, category, tags, skip, limit
    )
    return {
        "total": total,
        "results": results,
        "skip": skip,
        "limit": limit
    }


@router.get("/prompts/{prompt_id}", response_model=schemas.Prompt)
def get_prompt(prompt_id: int, db: Session = Depends(get_db)):
    """Получить промпт по ID"""
    db_prompt = PromptService.get_prompt(db, prompt_id)
    if not db_prompt:
        raise HTTPException(status_code=404, detail="Prompt not found")
    return db_prompt


@router.put("/prompts/{prompt_id}", response_model=schemas.Prompt)
def update_prompt(
    prompt_id: int,
    prompt_update: schemas.PromptUpdate,
    db: Session = Depends(get_db)
):
    """Обновить промпт"""
    db_prompt = PromptService.update_prompt(db, prompt_id, prompt_update)
    if not db_prompt:
        raise HTTPException(status_code=404, detail="Prompt not found")
    return db_prompt


@router.delete("/prompts/{prompt_id}")
def delete_prompt(prompt_id: int, db: Session = Depends(get_db)):
    """Удалить промпт"""
    if not PromptService.delete_prompt(db, prompt_id):
        raise HTTPException(status_code=404, detail="Prompt not found")
    return {"message": "Prompt deleted successfully"}


@router.post("/prompts/{prompt_id}/use")
def use_prompt(prompt_id: int, db: Session = Depends(get_db)):
    """Увеличить счётчик использования промпта"""
    db_prompt = PromptService.get_prompt(db, prompt_id)
    if not db_prompt:
        raise HTTPException(status_code=404, detail="Prompt not found")
    PromptService.increment_usage(db, prompt_id)
    return {"message": "Usage count incremented"}


# ================ TAGS ENDPOINTS ================

@router.post("/tags", response_model=schemas.Tag)
def create_tag(tag: schemas.TagCreate, db: Session = Depends(get_db)):
    """Создать новый тег"""
    existing = TagService.get_tag_by_name(db, tag.name)
    if existing:
        raise HTTPException(status_code=400, detail="Tag already exists")
    return TagService.create_tag(db, tag)


@router.get("/tags", response_model=List[schemas.Tag])
def list_tags(db: Session = Depends(get_db)):
    """Получить все теги"""
    return TagService.get_all_tags(db)


@router.delete("/tags/{tag_id}")
def delete_tag(tag_id: int, db: Session = Depends(get_db)):
    """Удалить тег"""
    if not TagService.delete_tag(db, tag_id):
        raise HTTPException(status_code=404, detail="Tag not found")
    return {"message": "Tag deleted successfully"}


# ================ AUTO-TAGGING ENDPOINTS ================

@router.post("/prompts/analyze")
def analyze_prompt_for_creation(data: dict):
    """
    Анализирует промпт перед созданием для предложения тегов, категории и ключевых слов
    
    Expected input:
    {
        "title": "Prompt Title",
        "content": "Prompt content",
        "category": "development" (optional)
    }
    """
    title = data.get("title", "")
    content = data.get("content", "")
    category = data.get("category")
    
    if not title or not content:
        raise HTTPException(status_code=400, detail="Title and content are required")
    
    # Анализируем с помощью KeywordAnalyzer
    analysis_result = keyword_analyzer.analyze(title, content, category)
    
    return {
        "suggested_tags": analysis_result.get("suggested_tags", []),
        "keywords": analysis_result.get("keywords", []),
        "suggested_category": analysis_result.get("suggested_category"),
        "suggested_difficulty": analysis_result.get("suggested_difficulty"),
        "confidence": analysis_result.get("confidence", 0.0),
        "tag_count": analysis_result.get("tag_count", 0)
    }


@router.post("/prompts/{prompt_id}/auto-tag", response_model=schemas.AutoTagResult)
def auto_tag_prompt(prompt_id: int, db: Session = Depends(get_db)):
    """Автоматически тегировать промпт"""
    result = AutoTaggingService.auto_tag_prompt(db, prompt_id)
    if not result:
        raise HTTPException(status_code=404, detail="Prompt not found")
    return result


# ================ IMPORT ENDPOINTS ================

@router.post("/import/json")
def import_from_json(
    file: UploadFile = File(...),
    source_name: str = Query("import"),
    db: Session = Depends(get_db)
):
    """Импортировать промпты из JSON файла"""
    try:
        content = file.file.read().decode('utf-8')
        data = json.loads(content)
        
        # Сохраняем временный файл
        import tempfile
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as tmp:
            json.dump(data, tmp)
            tmp_path = tmp.name
        
        # Импортируем
        prompts_data = PromptImporter.import_from_json(tmp_path, source_name)
        imported = []
        
        for prompt_data in prompts_data:
            prompt_data.imported_from = source_name
            db_prompt = PromptService.create_prompt(db, prompt_data)
            imported.append(db_prompt)
        
        return {
            "message": f"Successfully imported {len(imported)} prompts",
            "imported_count": len(imported),
            "prompts": imported
        }
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON file")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/import/batch")
def import_bulk_prompts(
    bulk_import: schemas.PromptBulkImport,
    db: Session = Depends(get_db)
):
    """Массовый импорт промптов"""
    imported = []
    
    for prompt_data in bulk_import.prompts:
        prompt_data.imported_from = bulk_import.import_source
        db_prompt = PromptService.create_prompt(db, prompt_data)
        imported.append(db_prompt)
    
    return {
        "message": f"Successfully imported {len(imported)} prompts",
        "imported_count": len(imported),
        "prompts": imported
    }


# ================ PROJECTS ENDPOINTS ================

@router.post("/projects", response_model=schemas.Project)
def create_project(project: schemas.ProjectCreate, db: Session = Depends(get_db)):
    """Создать новый проект"""
    return ProjectService.create_project(db, project)


@router.get("/projects", response_model=List[schemas.Project])
def list_projects(db: Session = Depends(get_db)):
    """Получить все проекты"""
    return ProjectService.get_all_projects(db)


@router.get("/projects/{project_id}", response_model=schemas.Project)
def get_project(project_id: int, db: Session = Depends(get_db)):
    """Получить проект по ID"""
    db_project = ProjectService.get_project(db, project_id)
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")
    return db_project


@router.put("/projects/{project_id}", response_model=schemas.Project)
def update_project(
    project_id: int,
    project_update: schemas.ProjectUpdate,
    db: Session = Depends(get_db)
):
    """Обновить проект"""
    db_project = ProjectService.update_project(db, project_id, project_update)
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")
    return db_project


@router.delete("/projects/{project_id}")
def delete_project(project_id: int, db: Session = Depends(get_db)):
    """Удалить проект"""
    if not ProjectService.delete_project(db, project_id):
        raise HTTPException(status_code=404, detail="Project not found")
    return {"message": "Project deleted successfully"}


@router.post("/projects/{project_id}/process")
def add_process_entry(
    project_id: int,
    entry: str = Query(..., min_length=1),
    db: Session = Depends(get_db)
):
    """Добавить запись в процесс разработки"""
    db_project = ProjectService.get_project(db, project_id)
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    process_entry = ProjectService.add_process_entry(db, project_id, entry)
    return process_entry


@router.post("/projects/{project_id}/tasks")
def add_task(
    project_id: int,
    task: schemas.TaskEntry,
    db: Session = Depends(get_db)
):
    """Добавить задачу к проекту"""
    db_project = ProjectService.get_project(db, project_id)
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    task.project_id = project_id
    db_task = ProjectService.add_task(db, project_id, task)
    return db_task


@router.put("/tasks/{task_id}")
def update_task(task_id: int, task_update: dict, db: Session = Depends(get_db)):
    """Обновить задачу"""
    db_task = ProjectService.update_task(db, task_id, task_update)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task


# ================ STATISTICS ENDPOINTS ================

@router.get("/stats")
def get_statistics(db: Session = Depends(get_db)):
    """Получить статистику приложения"""
    from sqlalchemy import func
    from app.db.models import Prompt, Tag, Project
    
    from sqlalchemy import func
    
    total_prompts = db.query(func.count(Prompt.id)).scalar()
    total_tags = db.query(func.count(Tag.id)).scalar()
    total_projects = db.query(func.count(Project.id)).scalar()
    total_categories = db.query(func.count(Prompt.category.distinct())).scalar()
    
    # Самые используемые промпты
    top_prompts = db.query(Prompt).order_by(Prompt.usage_count.desc()).limit(5).all()
    
    return {
        "total_prompts": total_prompts or 0,
        "total_tags": total_tags or 0,
        "total_projects": total_projects or 0,
        "total_categories": total_categories or 0,
        "top_prompts": top_prompts
    }


@router.get("/stats")
def get_stats(db: Session = Depends(get_db)):
    """Получить статистику"""
    from sqlalchemy import func
    from app.db.models import Prompt, Tag, Project
    
    total_prompts = db.query(func.count(Prompt.id)).scalar() or 0
    total_tags = db.query(func.count(Tag.id)).scalar() or 0
    total_projects = db.query(func.count(Project.id)).scalar() or 0
    total_categories = db.query(func.count(Prompt.category.distinct())).scalar() or 0
    
    return {
        "total_prompts": total_prompts,
        "total_tags": total_tags,
        "total_projects": total_projects,
        "total_categories": total_categories
    }


# ================ AUTO-TAGGING ENDPOINTS ================

@router.post("/prompts/{prompt_id}/auto-tag")
def auto_tag_prompt(prompt_id: int, db: Session = Depends(get_db)):
    """Auto-tag a prompt based on its content"""
    prompt = PromptService.get_prompt(db, prompt_id)
    if not prompt:
        raise HTTPException(status_code=404, detail="Prompt not found")
    
    # Extract tags
    tags = ATS.extract_tags(prompt.content, prompt.title, limit=5)
    category = ATS.categorize_prompt(prompt.content, prompt.title)
    keywords = ATS.extract_keywords(prompt.content, limit=10)
    
    return {
        "prompt_id": prompt_id,
        "suggested_tags": tags,
        "suggested_category": category,
        "keywords": keywords
    }


@router.post("/prompts/extract-keywords")
def extract_keywords(data: dict):
    """Extract keywords from text for highlighting"""
    content = data.get("content", "")
    keywords = ATS.extract_keywords(content, limit=15)
    highlighted = ATS.highlight_keywords(content, keywords)
    
    return {
        "keywords": keywords,
        "highlighted_content": highlighted
    }


# ================ FILE SERVICE ENDPOINTS ================

@router.post("/prompts/{prompt_id}/export-txt")
def export_prompt_txt(prompt_id: int, db: Session = Depends(get_db)):
    """Export prompt as TXT file"""
    prompt = PromptService.get_prompt(db, prompt_id)
    if not prompt:
        raise HTTPException(status_code=404, detail="Prompt not found")
    
    # Get tags
    tag_names = [tag.name for tag in prompt.tags]
    
    # Save file
    file_path = FileService.save_prompt_as_txt(
        prompt_id, prompt.title, prompt.content, 
        prompt.category, tag_names
    )
    
    return {
        "message": "Prompt exported successfully",
        "file_path": file_path
    }


@router.post("/projects/{project_id}/create-structure")
def create_project_structure(project_id: int, db: Session = Depends(get_db)):
    """Create directory structure for a project"""
    project = ProjectService.get_project(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    structure = FileService.create_project_structure(project_id, project.name)
    
    return {
        "message": "Project structure created",
        "structure": structure
    }


@router.put("/projects/{project_id}/tasks")
def update_project_tasks(project_id: int, data: dict, db: Session = Depends(get_db)):
    """Update project tasks file"""
    project = ProjectService.get_project(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    content = data.get("content", "")
    file_path = FileService.update_project_file(project_id, project.name, "tasks", content)
    
    return {
        "message": "Tasks updated successfully",
        "file_path": file_path
    }


@router.put("/projects/{project_id}/process")
def update_project_process(project_id: int, data: dict, db: Session = Depends(get_db)):
    """Update project process file"""
    project = ProjectService.get_project(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    content = data.get("content", "")
    file_path = FileService.update_project_file(project_id, project.name, "process", content)
    
    return {
        "message": "Process updated successfully",
        "file_path": file_path
    }


@router.get("/projects/{project_id}/tasks")
def get_project_tasks(project_id: int, db: Session = Depends(get_db)):
    """Get project tasks file content"""
    project = ProjectService.get_project(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    content = FileService.read_project_file(project_id, project.name, "tasks")
    
    return {
        "project_id": project_id,
        "content": content or ""
    }


@router.get("/projects/{project_id}/process")
def get_project_process(project_id: int, db: Session = Depends(get_db)):
    """Get project process file content"""
    project = ProjectService.get_project(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    content = FileService.read_project_file(project_id, project.name, "process")
    
    return {
        "project_id": project_id,
        "content": content or ""
    }


@router.get("/prompts/by-category/{category}")
def get_prompts_by_category(category: str, db: Session = Depends(get_db)):
    """Get all prompts in a specific category"""
    prompts = db.query(PromptService.Prompt).filter(
        PromptService.Prompt.category == category
    ).all()
    
    return {
        "category": category,
        "prompts": prompts,
        "count": len(prompts)
    }


@router.get("/prompts/categories")
def get_all_categories(db: Session = Depends(get_db)):
    """Get list of all prompt categories"""
    from sqlalchemy import distinct
    from app.db.models import Prompt
    
    categories = db.query(distinct(Prompt.category)).all()
    category_list = [cat[0] for cat in categories if cat[0]]
    
    return {
        "categories": category_list,
        "count": len(category_list)
    }

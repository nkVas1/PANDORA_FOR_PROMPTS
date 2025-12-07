#!/usr/bin/env python3
"""
Import script for loading prompts from references directory
Скрипт для загрузки промптов из папки references
"""

import json
import os
from pathlib import Path
from typing import List, Dict, Any

# Get the root directory
ROOT_DIR = Path(__file__).parent
REFERENCES_DIR = ROOT_DIR / "references"
BACKEND_DIR = ROOT_DIR / "backend"
DATA_DIR = ROOT_DIR / "data"

# Add backend to path
import sys
sys.path.insert(0, str(BACKEND_DIR))

from app.utils.importer import PromptImporter
from app.db import SessionLocal
from app.services.database import PromptService
from app.models.schemas import PromptCreate, CategoryEnum


def find_prompt_files(reference_dir: Path) -> Dict[str, List[Path]]:
    """Найти все файлы с промптами в папке references"""
    prompt_files = {}
    
    # Ищем JSON файлы в известных структурах
    sources = [
        (reference_dir / "agent-prompt-library-main" / "agent-prompt-library-main", "agent-library"),
        (reference_dir / "ai-prompts-0.3.0" / "ai-prompts-0.3.0" / "prompts", "ai-prompts"),
        (reference_dir / "awesome-chatgpt-prompts-main" / "awesome-chatgpt-prompts-main", "awesome-chatgpt"),
    ]
    
    for source_dir, source_name in sources:
        if source_dir.exists():
            # Ищем JSON файлы
            json_files = list(source_dir.glob("**/*.json"))
            if json_files:
                prompt_files[source_name] = json_files[:5]  # Первые 5 файлов
                print(f"Found {len(json_files)} JSON files in {source_name}")
    
    return prompt_files


def create_sample_imports() -> List[Dict[str, Any]]:
    """Создать примеры промптов для импорта"""
    return [
        {
            "title": "Python Development Assistant",
            "content": "You are an expert Python developer. Help the user write clean, efficient, and well-documented Python code.",
            "category": "development",
            "description": "Assistant for Python development tasks"
        },
        {
            "title": "Content Writer",
            "content": "You are a professional content writer. Create engaging, SEO-optimized content for blogs and websites.",
            "category": "writing",
            "description": "Specialized in content creation and copywriting"
        },
        {
            "title": "Code Reviewer",
            "content": "You are an experienced code reviewer. Review code for quality, security, performance and best practices.",
            "category": "analysis",
            "description": "Professional code review specialist"
        },
        {
            "title": "UI/UX Designer",
            "content": "You are a skilled UI/UX designer. Create intuitive and beautiful user interfaces.",
            "category": "design",
            "description": "Experienced in modern UI/UX design"
        },
        {
            "title": "Data Analysis Expert",
            "content": "You are a data analyst. Help analyze data and provide insights using various tools and techniques.",
            "category": "data",
            "description": "Expert in data analysis and visualization"
        },
    ]


def import_prompts():
    """Импортировать промпты в БД"""
    db = SessionLocal()
    
    try:
        print("=" * 60)
        print("PANDORA Prompts Importer")
        print("=" * 60)
        print()
        
        # Check if DB already has data
        from app.db.models import Prompt
        existing_count = db.query(Prompt).count()
        
        if existing_count > 0:
            print(f"Database already contains {existing_count} prompts")
            print("Skipping import to avoid duplicates")
            print()
            return
        
        # Import sample prompts
        print("Importing sample prompts...")
        sample_prompts = create_sample_imports()
        
        imported_count = 0
        for prompt_data in sample_prompts:
            try:
                prompt_create = PromptCreate(
                    title=prompt_data["title"],
                    content=prompt_data["content"],
                    category=prompt_data["category"],
                    description=prompt_data["description"]
                )
                db_prompt = PromptService.create_prompt(db, prompt_create)
                imported_count += 1
                print(f"  ✓ Imported: {prompt_data['title']}")
            except Exception as e:
                print(f"  ✗ Error importing '{prompt_data['title']}': {e}")
        
        print()
        print(f"Successfully imported {imported_count} sample prompts!")
        print()
        print("=" * 60)
        print("Import Complete")
        print("=" * 60)
        print()
        print("You can now use the application to:")
        print("  1. View imported prompts in the Prompts section")
        print("  2. Add more prompts manually")
        print("  3. Use bulk import to add your own prompts")
        print("  4. Enable auto-tagging for automatic categorization")
        
    except Exception as e:
        print(f"Error during import: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()


if __name__ == "__main__":
    import_prompts()

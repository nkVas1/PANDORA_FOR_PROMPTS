import json
from pathlib import Path
from typing import List
from app.config import settings
from app.models.schemas import PromptCreate, CategoryEnum


class PromptImporter:
    """Импортер промптов из различных источников"""
    
    @staticmethod
    def import_from_json(file_path: str, source_name: str) -> List[PromptCreate]:
        """Импортировать промпты из JSON файла"""
        prompts = []
        
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if isinstance(data, list):
            for item in data:
                prompt = PromptImporter._parse_prompt(item, source_name)
                if prompt:
                    prompts.append(prompt)
        elif isinstance(data, dict):
            if 'prompts' in data:
                for item in data['prompts']:
                    prompt = PromptImporter._parse_prompt(item, source_name)
                    if prompt:
                        prompts.append(prompt)
            elif 'agents' in data:
                for item in data['agents']:
                    prompt = PromptImporter._parse_agent(item, source_name)
                    if prompt:
                        prompts.append(prompt)
        
        return prompts
    
    @staticmethod
    def _parse_prompt(item: dict, source_name: str) -> PromptCreate:
        """Парсирует одиночный промпт из JSON"""
        try:
            title = item.get('title') or item.get('name') or item.get('prompt', '')[:50]
            content = item.get('content') or item.get('prompt') or ''
            
            if not title or not content:
                return None
            
            category = item.get('category', 'import')
            if category not in [c.value for c in CategoryEnum]:
                category = 'import'
            
            return PromptCreate(
                title=title,
                content=content,
                description=item.get('description', ''),
                category=category,
                version=item.get('version', '1.0')
            )
        except Exception:
            return None
    
    @staticmethod
    def _parse_agent(item: dict, source_name: str) -> PromptCreate:
        """Парсирует агента из JSON (для agent-library)"""
        try:
            return PromptCreate(
                title=item.get('name', ''),
                content=item.get('description', ''),
                description=f"Agent: {item.get('id', '')}",
                category='import',
                version='1.0'
            )
        except Exception:
            return None

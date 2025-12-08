# -*- coding: utf-8 -*-
"""
Сервис для импорта всех промптов из папки references.
Автоматически категоризирует и правильно структурирует данные.
Рекурсивно собирает ВСЕ .md файлы из всех подпапок.
"""

import json
import os
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from datetime import datetime

class ReferencesImporter:
    """Импортер промптов из папок references"""
    
    # Маппинг папок на категории
    FOLDER_TO_CATEGORY = {
        # Agent Prompt Library
        "backend-api": "development",
        "frontend-developer": "development",
        "code-review": "review",
        "debugging": "development",
        "refactoring": "development",
        "testing-specialist": "development",
        "technical-writer": "writing",
        "security-analyst": "analysis",
        "infrastructure": "devops",
        "react-native": "development",
        
        # Структура для других источников
        "development": "development",
        "writing": "writing",
        "analysis": "analysis",
        "business": "business",
        "creative": "creative",
        "marketing": "marketing",
        "design": "design",
        "research": "research",
        "translation": "translation",
        "education": "education",
        "devops": "devops",
        "review": "review",
        
        # Дополнительные паттерны
        "code": "development",
        "python": "development",
        "javascript": "development",
        "web": "development",
        "api": "development",
        "database": "development",
        "testing": "development",
        "documentation": "writing",
        "tutorial": "education",
    }
    
    CATEGORY_DESCRIPTIONS = {
        "development": "Разработка и программирование",
        "review": "Проверка кода и качество",
        "writing": "Написание текстов и документация",
        "analysis": "Анализ и аналитика",
        "business": "Бизнес и менеджмент",
        "creative": "Творческие задачи",
        "marketing": "Маркетинг и продвижение",
        "design": "Дизайн и визуалика",
        "research": "Исследования",
        "translation": "Переводы и локализация",
        "education": "Образование и обучение",
        "devops": "DevOps и развертывание",
    }
    
    @staticmethod
    def find_references_dir() -> Optional[Path]:
        """Находит директорию references"""
        import sys
        
        # Для exe используем папку exe, для разработки - идем вверх
        if getattr(sys, 'frozen', False):
            current = Path(sys.executable).parent.parent
        else:
            current = Path(__file__).parent.parent.parent
        
        # Ищем references идя вверх по иерархии
        for _ in range(5):  # Максимум 5 уровней вверх
            references_dir = current / "references"
            if references_dir.exists():
                return references_dir
            current = current.parent
            if current == current.parent:  # Достигли корня
                break
        
        return None
    
    @staticmethod
    def extract_title_from_content(content: str, file_path: Path) -> str:
        """Извлекает заголовок из содержимого файла"""
        lines = content.split('\n')
        
        # Ищем первый заголовок (# или ##)
        for line in lines[:10]:
            if line.strip().startswith('#'):
                title = line.lstrip('#').strip()
                if title:
                    return title
        
        # Если заголовка нет, используем имя файла
        title = file_path.stem.replace('_', ' ').replace('-', ' ').title()
        return title if title != 'Readme' else f"{file_path.parent.name} - README"
    
    @staticmethod
    def categorize_by_path(file_path: Path, parent_name: str) -> str:
        """Определяет категорию по пути и названию папки"""
        folder_name = parent_name.lower().replace('_', '-').replace(' ', '-')
        
        # Проверяем папку файла
        for folder in file_path.parts:
            folder_lower = folder.lower().replace('_', '-')
            if folder_lower in ReferencesImporter.FOLDER_TO_CATEGORY:
                return ReferencesImporter.FOLDER_TO_CATEGORY[folder_lower]
        
        # Проверяем родительскую папку
        if folder_name in ReferencesImporter.FOLDER_TO_CATEGORY:
            return ReferencesImporter.FOLDER_TO_CATEGORY[folder_name]
        
        # Умная категоризация по названию
        folder_lower = folder_name.lower()
        
        if any(x in folder_lower for x in ['code', 'dev', 'python', 'javascript', 'java', 'backend', 'frontend', 'api', 'web', 'database']):
            return 'development'
        if any(x in folder_lower for x in ['devops', 'deploy', 'docker', 'kubernetes', 'ci', 'infra']):
            return 'devops'
        if any(x in folder_lower for x in ['write', 'blog', 'article', 'content', 'documentation', 'document']):
            return 'writing'
        if any(x in folder_lower for x in ['analysis', 'research', 'analytic']):
            return 'analysis'
        if any(x in folder_lower for x in ['business', 'strategy', 'planning']):
            return 'business'
        if any(x in folder_lower for x in ['design', 'ui', 'ux']):
            return 'design'
        if any(x in folder_lower for x in ['creative', 'brainstorm', 'idea']):
            return 'creative'
        if any(x in folder_lower for x in ['marketing']):
            return 'marketing'
        if any(x in folder_lower for x in ['learn', 'education', 'tutorial']):
            return 'education'
        if any(x in folder_lower for x in ['review', 'code-review']):
            return 'review'
        if any(x in folder_lower for x in ['translate', 'translation']):
            return 'translation'
        
        return 'development'  # По умолчанию
    
    @staticmethod
    def is_likely_prompt(file_path: Path, content: str) -> bool:
        """
        Определяет, является ли файл реальным промптом, а не документацией.
        
        Критерии фильтрации:
        - Не документационные файлы (README, CHANGELOG, LICENSE, CONTRIBUTING)
        - Содержит признаки промпта (instructions, task, prompt keywords)
        - Разумный размер контента (не слишком большой как документация)
        - Содержит вопросительные или повелительные конструкции
        """
        
        # Исключаем явные документационные файлы
        excluded_names = {
            'readme', 'changelog', 'license', 'contributing', 'authors',
            'installation', 'setup', 'quickstart', 'getting-started',
            'index', 'toc', 'table-of-contents', 'glossary'
        }
        
        file_name_lower = file_path.stem.lower().replace('_', '-')
        if file_name_lower in excluded_names:
            print(f"[IMPORT FILTER] Excluding by filename: {file_path.name}")
            return False
        
        # Исключаем очень большие файлы (скорее всего документация, а не промпт)
        if len(content) > 10000:  # > 10KB - скорее всего документация
            print(f"[IMPORT FILTER] Excluding large file (>10KB): {file_path.name} (size={len(content)})")
            return False
        
        # Признаки документации (много заголовков, little content)
        lines = content.split('\n')
        header_count = sum(1 for line in lines if line.strip().startswith('#'))
        total_lines = len([l for l in lines if l.strip()])
        
        # Если много заголовков относительно контента - это документация
        if total_lines > 0 and header_count / total_lines > 0.3:
            print(f"[IMPORT FILTER] Excluding by header density: {file_path.name} (headers={header_count}, lines={total_lines})")
            return False
        
        # Ищем признаки промпта в содержимом
        content_lower = content.lower()
        
        prompt_keywords = {
            'prompt', 'task', 'instruction', 'instructions', 'system',
            'assistant', 'user', 'role', 'you are', 'act as', 'write a',
            'generate', 'create', 'design', 'explain', 'describe',
            'list', 'analyze', 'suggest', 'recommend', 'summarize',
            'translate', 'convert', 'format', 'rewrite', 'improve',
            'question:', 'q:', 'request:', 'example:', 'example,',
            '?', # Содержит вопросы
        }
        
        # Проверяем есть ли хоть один признак промпта
        prompt_score = sum(1 for kw in prompt_keywords if kw in content_lower)
        
        # Исключаем пустые или очень маленькие файлы (< 50 символов)
        if len(content.strip()) < 50:
            print(f"[IMPORT FILTER] Excluding tiny file (<50 chars): {file_path.name}")
            return False
        
        # Если нет явных признаков промпта и много документации - это не промпт
        if prompt_score == 0 and header_count > 2:
            print(f"[IMPORT FILTER] Excluding: no prompt keywords and many headers: {file_path.name}")
            return False
        
        # Если имеет минимум один признак промпта - считаем его промптом
        if prompt_score > 0:
            return True
        
        # По умолчанию включаем, если это не явная документация
        # По умолчанию включаем, если это не явная документация
        return not (file_name_lower in excluded_names)
    
    @staticmethod
    def collect_all_md_files(root_dir: Path, source_name: str) -> List[Dict]:
        """Рекурсивно собирает ВСЕ .md файлы из папки и подпапок"""
        prompts = []
        
        if not root_dir.exists():
            return prompts
        
        try:
            # Собираем ВСЕ .md файлы рекурсивно
            md_files = list(root_dir.glob('**/*.md'))
            filtered_count = 0
            
            for file_path in md_files:
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                    
                    if not content.strip():
                        continue
                    
                    # Фильтруем по признакам промпта
                    if not ReferencesImporter.is_likely_prompt(file_path, content):
                        filtered_count += 1
                        continue
                    
                    title = ReferencesImporter.extract_title_from_content(content, file_path)
                    category = ReferencesImporter.categorize_by_path(file_path, source_name)
                    
                    # Определяем относительный путь для source_id
                    rel_path = file_path.relative_to(root_dir.parent)
                    
                    prompts.append({
                        'title': title[:255],
                        'content': content,
                        'description': f"From {source_name}",
                        'category': category,
                        'tags': [],
                        'imported_from': source_name,
                        'source_id': str(rel_path),
                    })
                except Exception as e:
                    print(f"[IMPORT ERROR] Failed to read {file_path}: {e}")
                    continue
            
            total_files = len(md_files)
            if filtered_count > 0:
                print(f"[IMPORT] Found {total_files} .md files in {root_dir.name} (filtered {filtered_count} non-prompts, kept {len(prompts)})")
            else:
                print(f"[IMPORT] Found {len(prompts)} .md files in {root_dir.name}")
        
        except Exception as e:
            print(f"[IMPORT ERROR] Error scanning {root_dir}: {e}")
        
        return prompts
    
    @staticmethod
    def import_all_references() -> Tuple[List[Dict], Dict[str, int]]:
        """Импортирует ВСЕ промпты из папки references"""
        references_dir = ReferencesImporter.find_references_dir()
        
        if not references_dir:
            print("[IMPORT] References directory not found!")
            return [], {}
        
        all_prompts = []
        stats = {}
        
        print(f"[IMPORT] Starting import from {references_dir}")
        print(f"[IMPORT] Scanning for ALL .md files recursively...")
        
        # Итерируем по всем папкам в references
        try:
            for item in references_dir.iterdir():
                if not item.is_dir():
                    continue
                
                source_name = item.name
                print(f"\n[IMPORT] Processing {source_name}...")
                
                # Проверяем разные структуры (с -main суффиксом или без)
                search_paths = [
                    item / item.name,  # Папка -main/-main структура
                    item / f"{item.name[:-5]}" if item.name.endswith('-main') else None,  # Без -main
                    item,  # Сама папка
                ]
                
                for search_path in search_paths:
                    if search_path is None or not search_path.exists():
                        continue
                    
                    # Для agent-prompt-library используем специальную обработку agents.json
                    if 'agent-prompt-library' in source_name.lower():
                        agents_json = search_path / "agents.json"
                        if agents_json.exists():
                            try:
                                with open(agents_json, 'r', encoding='utf-8') as f:
                                    data = json.load(f)
                                
                                for agent in data.get('agents', []):
                                    prompt_path = search_path / agent.get('path', '')
                                    if prompt_path.exists():
                                        with open(prompt_path, 'r', encoding='utf-8', errors='ignore') as f:
                                            content = f.read()
                                        
                                        all_prompts.append({
                                            'title': agent.get('name', agent.get('id', 'Unknown'))[:255],
                                            'content': content,
                                            'description': agent.get('description', ''),
                                            'category': ReferencesImporter.FOLDER_TO_CATEGORY.get(
                                                agent.get('category', 'development'), 'development'
                                            ),
                                            'tags': agent.get('tags', []),
                                            'imported_from': source_name,
                                            'source_id': agent.get('id', ''),
                                        })
                            except Exception as e:
                                print(f"[IMPORT ERROR] Failed to parse agents.json: {e}")
                    
                    # Собираем все .md файлы
                    prompts = ReferencesImporter.collect_all_md_files(search_path, source_name)
                    if prompts:
                        all_prompts.extend(prompts)
                        stats[source_name] = len(prompts)
                        print(f"[IMPORT] {source_name}: {len(prompts)} prompts collected")
                        break
        
        except Exception as e:
            print(f"[IMPORT ERROR] Error scanning references: {e}")
        
        print(f"\n[IMPORT] Total imported: {len(all_prompts)} prompts")
        return all_prompts, stats

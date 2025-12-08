#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Сервис для автоматического анализа и тегирования промптов.
Анализирует контент, выделяет ключевые слова и автоматически предлагает теги.
"""

import re
from typing import List, Dict, Optional, Tuple
from collections import Counter
import json


class KeywordAnalyzer:
    """Анализирует контент для выделения ключевых слов и автотегирования"""
    
    # Словарь ключевых слов с их связанными тегами и категориями
    KEYWORD_MAPPINGS = {
        # Development & Backend
        "api": {"tags": ["API", "Backend", "Integration"], "category": "development", "difficulty": "intermediate"},
        "rest": {"tags": ["REST", "API", "Backend"], "category": "development", "difficulty": "beginner"},
        "graphql": {"tags": ["GraphQL", "API", "Backend"], "category": "development", "difficulty": "advanced"},
        "database": {"tags": ["Database", "SQL", "Data"], "category": "development", "difficulty": "intermediate"},
        "sql": {"tags": ["SQL", "Database", "Data"], "category": "data", "difficulty": "intermediate"},
        "nosql": {"tags": ["NoSQL", "Database", "Data"], "category": "data", "difficulty": "intermediate"},
        "microservices": {"tags": ["Microservices", "Architecture", "DevOps"], "category": "devops", "difficulty": "advanced"},
        "docker": {"tags": ["Docker", "DevOps", "Containers"], "category": "devops", "difficulty": "intermediate"},
        "kubernetes": {"tags": ["Kubernetes", "DevOps", "Orchestration"], "category": "devops", "difficulty": "advanced"},
        "ci/cd": {"tags": ["CI/CD", "DevOps", "Automation"], "category": "devops", "difficulty": "intermediate"},
        "testing": {"tags": ["Testing", "QA", "Validation"], "category": "development", "difficulty": "intermediate"},
        "unit test": {"tags": ["Testing", "Unit Tests"], "category": "development", "difficulty": "beginner"},
        "integration test": {"tags": ["Testing", "Integration Tests"], "category": "development", "difficulty": "intermediate"},
        "framework": {"tags": ["Framework", "Library"], "category": "development", "difficulty": "intermediate"},
        "library": {"tags": ["Library", "Package"], "category": "development", "difficulty": "beginner"},
        "npm": {"tags": ["NPM", "Package Manager", "JavaScript"], "category": "development", "difficulty": "beginner"},
        "pip": {"tags": ["PIP", "Package Manager", "Python"], "category": "development", "difficulty": "beginner"},
        
        # Frontend & UI/UX
        "frontend": {"tags": ["Frontend", "UI"], "category": "design", "difficulty": "intermediate"},
        "react": {"tags": ["React", "JavaScript", "Frontend"], "category": "development", "difficulty": "intermediate"},
        "vue": {"tags": ["Vue", "JavaScript", "Frontend"], "category": "development", "difficulty": "intermediate"},
        "angular": {"tags": ["Angular", "JavaScript", "Frontend"], "category": "development", "difficulty": "advanced"},
        "typescript": {"tags": ["TypeScript", "JavaScript"], "category": "development", "difficulty": "intermediate"},
        "css": {"tags": ["CSS", "Styling", "Frontend"], "category": "design", "difficulty": "beginner"},
        "html": {"tags": ["HTML", "Markup", "Frontend"], "category": "development", "difficulty": "beginner"},
        "javascript": {"tags": ["JavaScript", "Frontend"], "category": "development", "difficulty": "intermediate"},
        "ui/ux": {"tags": ["UI/UX", "Design", "User Experience"], "category": "design", "difficulty": "intermediate"},
        "design": {"tags": ["Design", "Creative"], "category": "design", "difficulty": "intermediate"},
        "responsive": {"tags": ["Responsive Design", "Mobile"], "category": "design", "difficulty": "intermediate"},
        
        # Data & Analytics
        "data analysis": {"tags": ["Data Analysis", "Analytics"], "category": "analysis", "difficulty": "intermediate"},
        "machine learning": {"tags": ["Machine Learning", "AI"], "category": "analysis", "difficulty": "advanced"},
        "deep learning": {"tags": ["Deep Learning", "AI", "Neural Networks"], "category": "analysis", "difficulty": "advanced"},
        "nlp": {"tags": ["NLP", "Natural Language Processing"], "category": "analysis", "difficulty": "advanced"},
        "statistics": {"tags": ["Statistics", "Data Analysis"], "category": "analysis", "difficulty": "intermediate"},
        "pandas": {"tags": ["Pandas", "Data Analysis", "Python"], "category": "data", "difficulty": "intermediate"},
        "numpy": {"tags": ["NumPy", "Data Analysis", "Python"], "category": "data", "difficulty": "intermediate"},
        "visualization": {"tags": ["Visualization", "Data"], "category": "design", "difficulty": "intermediate"},
        "chart": {"tags": ["Charts", "Visualization", "Data"], "category": "design", "difficulty": "beginner"},
        
        # Writing & Content
        "documentation": {"tags": ["Documentation", "Writing"], "category": "writing", "difficulty": "intermediate"},
        "blog": {"tags": ["Blog", "Content", "Writing"], "category": "writing", "difficulty": "beginner"},
        "article": {"tags": ["Article", "Content", "Writing"], "category": "writing", "difficulty": "beginner"},
        "seo": {"tags": ["SEO", "Marketing", "Content"], "category": "marketing", "difficulty": "intermediate"},
        "copywriting": {"tags": ["Copywriting", "Writing", "Marketing"], "category": "writing", "difficulty": "intermediate"},
        "editing": {"tags": ["Editing", "Writing"], "category": "writing", "difficulty": "intermediate"},
        "technical writing": {"tags": ["Technical Writing", "Documentation"], "category": "writing", "difficulty": "intermediate"},
        
        # Security & Devops
        "security": {"tags": ["Security", "Safety"], "category": "review", "difficulty": "advanced"},
        "authentication": {"tags": ["Authentication", "Security"], "category": "devops", "difficulty": "intermediate"},
        "authorization": {"tags": ["Authorization", "Security"], "category": "devops", "difficulty": "intermediate"},
        "encryption": {"tags": ["Encryption", "Security"], "category": "devops", "difficulty": "advanced"},
        "vulnerability": {"tags": ["Vulnerability", "Security", "Testing"], "category": "review", "difficulty": "advanced"},
        "performance": {"tags": ["Performance", "Optimization"], "category": "review", "difficulty": "advanced"},
        
        # Business & Process
        "project management": {"tags": ["Project Management", "Business"], "category": "project", "difficulty": "beginner"},
        "agile": {"tags": ["Agile", "Project Management"], "category": "project", "difficulty": "intermediate"},
        "scrum": {"tags": ["Scrum", "Agile"], "category": "project", "difficulty": "beginner"},
        "kanban": {"tags": ["Kanban", "Project Management"], "category": "project", "difficulty": "beginner"},
        "business logic": {"tags": ["Business Logic", "Architecture"], "category": "development", "difficulty": "intermediate"},
        "requirement": {"tags": ["Requirements", "Analysis"], "category": "analysis", "difficulty": "beginner"},
        
        # Other
        "code review": {"tags": ["Code Review", "Quality"], "category": "review", "difficulty": "intermediate"},
        "refactor": {"tags": ["Refactoring", "Code Quality"], "category": "development", "difficulty": "intermediate"},
        "debug": {"tags": ["Debugging", "Development"], "category": "development", "difficulty": "intermediate"},
        "error handling": {"tags": ["Error Handling", "Development"], "category": "development", "difficulty": "intermediate"},
        "logging": {"tags": ["Logging", "Debugging"], "category": "devops", "difficulty": "beginner"},
        "monitoring": {"tags": ["Monitoring", "DevOps"], "category": "devops", "difficulty": "intermediate"},
    }
    
    # Русские эквиваленты для тегов
    RUSSIAN_TAG_MAP = {
        "API": "АПИ",
        "Backend": "Backend",
        "Frontend": "Frontend",
        "DevOps": "DevOps",
        "Database": "БД",
        "Testing": "Тестирование",
        "Security": "Безопасность",
        "Performance": "Производительность",
        "Code Review": "Ревью кода",
        "Documentation": "Документация",
        "Design": "Дизайн",
    }
    
    def __init__(self):
        """Инициализация анализатора"""
        pass
    
    @staticmethod
    def _normalize_text(text: str) -> str:
        """Нормализация текста для анализа"""
        return text.lower().strip()
    
    @staticmethod
    def _extract_sentences(text: str) -> List[str]:
        """Извлечение предложений из текста"""
        sentences = re.split(r'[.!?]+', text)
        return [s.strip() for s in sentences if s.strip()]
    
    @staticmethod
    def _extract_technical_terms(text: str) -> List[str]:
        """Извлечение технических терминов (слова в backticks, все caps и т.д.)"""
        terms = []
        
        # Слова в backticks: `term`
        terms.extend(re.findall(r'`([^`]+)`', text))
        
        # Слова в кавычках: "term"
        terms.extend(re.findall(r'"([^"]+)"', text))
        
        # CamelCase слова (названия классов, функций)
        terms.extend(re.findall(r'\b[A-Z][a-z]+(?:[A-Z][a-z]+)*\b', text))
        
        # SCREAMING_SNAKE_CASE переменные
        terms.extend(re.findall(r'\b[A-Z][A-Z0-9_]*\b', text))
        
        return [t for t in terms if len(t) > 2]
    
    def analyze(self, prompt_title: str, prompt_content: str, 
                category: Optional[str] = None) -> Dict:
        """
        Анализирует промпт и возвращает предложенные теги и метаданные
        
        Args:
            prompt_title: Название промпта
            prompt_content: Содержание промпта
            category: Текущая категория (если известна)
            
        Returns:
            dict с ключами:
                - suggested_tags: List[str] предложенных тегов
                - keywords: List[str] выделенных ключевых слов
                - suggested_category: str предложенная категория
                - difficulty: str предложенный уровень сложности
                - confidence: float уверенность предложения (0.0 - 1.0)
        """
        full_text = self._normalize_text(f"{prompt_title} {prompt_content}")
        
        # Счетчики для сбора статистики
        found_tags = {}
        found_categories = {}
        found_difficulties = {}
        found_keywords = []
        
        # Поиск ключевых слов из нашего словаря
        for keyword, mapping in self.KEYWORD_MAPPINGS.items():
            if keyword in full_text:
                # Подсчитываем вхождения для взвешивания
                count = full_text.count(keyword)
                
                for tag in mapping.get("tags", []):
                    found_tags[tag] = found_tags.get(tag, 0) + count
                
                category_val = mapping.get("category")
                if category_val:
                    found_categories[category_val] = found_categories.get(category_val, 0) + count
                
                difficulty_val = mapping.get("difficulty")
                if difficulty_val:
                    found_difficulties[difficulty_val] = found_difficulties.get(difficulty_val, 0) + count
                
                found_keywords.append(keyword)
        
        # Извлечение технических терминов
        technical_terms = self._extract_technical_terms(prompt_content)
        found_keywords.extend([t for t in technical_terms if len(t) > 2])
        
        # Сортируем и выбираем топ теги
        sorted_tags = sorted(found_tags.items(), key=lambda x: x[1], reverse=True)
        suggested_tags = [tag[0] for tag in sorted_tags[:5]]  # Топ 5 тегов
        
        # Выбираем наиболее вероятную категорию
        suggested_category = None
        category_confidence = 0.0
        if found_categories:
            sorted_cats = sorted(found_categories.items(), key=lambda x: x[1], reverse=True)
            suggested_category = sorted_cats[0][0]
            # Уверенность = количество найденных слов / всего слов
            category_confidence = min(1.0, sorted_cats[0][1] / max(len(full_text.split()), 1))
        
        # Уровень сложности
        suggested_difficulty = "intermediate"
        if found_difficulties:
            sorted_diff = sorted(found_difficulties.items(), key=lambda x: x[1], reverse=True)
            suggested_difficulty = sorted_diff[0][0]
        
        # Удаляем дубликаты и ограничиваем список ключевых слов
        unique_keywords = list(set([k.lower() for k in found_keywords]))[:10]
        
        return {
            "suggested_tags": suggested_tags,
            "keywords": unique_keywords,
            "suggested_category": suggested_category,
            "suggested_difficulty": suggested_difficulty,
            "confidence": category_confidence,
            "tag_count": len(found_tags)
        }
    
    def get_difficulty_emoji(self, difficulty: str) -> str:
        """Получить эмодзи для уровня сложности"""
        emoji_map = {
            "beginner": "🟢",
            "intermediate": "🟡",
            "advanced": "🔴",
        }
        return emoji_map.get(difficulty, "⚪")
    
    def get_category_emoji(self, category: str) -> str:
        """Получить эмодзи для категории"""
        emoji_map = {
            "development": "💻",
            "writing": "✍️",
            "analysis": "📊",
            "design": "🎨",
            "marketing": "📢",
            "data": "📈",
            "import": "📥",
            "project": "📁",
            "custom": "⚙️",
            "review": "👁️",
            "devops": "🚀",
            "research": "🔬",
            "education": "🎓",
        }
        return emoji_map.get(category, "📌")


# Создаем глобальный экземпляр анализатора
analyzer = KeywordAnalyzer()

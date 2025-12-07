import re
from typing import List, Dict
from collections import Counter


class AutoTagger:
    """Автоматическое тегирование промптов на основе анализа текста"""
    
    # Основные категории и ключевые слова
    CATEGORY_KEYWORDS = {
        "development": [
            "code", "program", "develop", "python", "javascript", "java", "c++",
            "function", "class", "api", "backend", "frontend", "database", "sql",
            "react", "vue", "node", "express", "django", "flask", "algorithm",
            "data structure", "git", "version control", "debug", "test", "unit test"
        ],
        "writing": [
            "write", "article", "blog", "story", "novel", "poem", "content",
            "copywriting", "editing", "proofreading", "grammar", "style",
            "seo", "content marketing", "creative writing", "email", "newsletter"
        ],
        "analysis": [
            "analyze", "analysis", "research", "study", "data", "statistics",
            "report", "summary", "review", "evaluate", "assessment",
            "market research", "competitor analysis", "swot", "financial"
        ],
        "design": [
            "design", "ui", "ux", "graphic", "visual", "color", "layout",
            "responsive", "css", "figma", "adobe", "prototype", "wireframe",
            "animation", "icon", "font", "branding"
        ],
        "marketing": [
            "marketing", "advertising", "campaign", "brand", "audience",
            "social media", "content strategy", "sales", "conversion",
            "engagement", "email marketing", "seo", "analytics",
            "customer", "client", "promotion"
        ],
        "data": [
            "data", "analytics", "sql", "database", "csv", "json", "xml",
            "machine learning", "ai", "neural network", "model",
            "prediction", "statistics", "tableau", "power bi", "excel"
        ],
    }
    
    # Теги по умолчанию
    DEFAULT_TAGS = [
        "important", "favourite", "review", "testing", "production",
        "documentation", "tutorial", "reference", "best-practice", "example",
        "warning", "todo", "optimized", "deprecated", "custom"
    ]
    
    def tag_prompt(self, title: str, content: str) -> Dict:
        """Автоматически генерирует теги и категорию для промпта"""
        combined_text = (title + " " + content).lower()
        
        # Получаем предложенную категорию
        category, category_confidence = self._suggest_category(combined_text)
        
        # Получаем предложенные теги
        suggested_tags = self._extract_tags(combined_text, category)
        
        return {
            "category": category,
            "category_confidence": category_confidence,
            "tags": suggested_tags
        }
    
    def _suggest_category(self, text: str) -> tuple[str, float]:
        """Предлагает категорию на основе анализа текста"""
        scores = {}
        
        for category, keywords in self.CATEGORY_KEYWORDS.items():
            score = sum(text.count(keyword) for keyword in keywords)
            scores[category] = score
        
        if not scores or max(scores.values()) == 0:
            return "custom", 0.0
        
        best_category = max(scores, key=scores.get)
        total_keywords = sum(len(keywords) for keywords in self.CATEGORY_KEYWORDS.values())
        confidence = min(scores[best_category] / total_keywords, 1.0)
        
        return best_category, confidence
    
    def _extract_tags(self, text: str, category: str = None) -> List[Dict]:
        """Извлекает теги из текста"""
        tags = []
        
        # Добавляем теги на основе технологий
        tech_tags = self._extract_tech_tags(text)
        tags.extend(tech_tags)
        
        # Добавляем теги на основе ключевых слов
        keyword_tags = self._extract_keyword_tags(text)
        tags.extend(keyword_tags)
        
        # Ограничиваем количество тегов и удаляем дубликаты
        seen = set()
        unique_tags = []
        for tag in tags:
            if tag['name'] not in seen:
                seen.add(tag['name'])
                unique_tags.append(tag)
        
        # Возвращаем лучшие теги
        return sorted(unique_tags, key=lambda x: x['confidence'], reverse=True)[:10]
    
    def _extract_tech_tags(self, text: str) -> List[Dict]:
        """Извлекает технологические теги"""
        tech_patterns = {
            "Python": r'\bpython\b',
            "JavaScript": r'\b(javascript|js)\b',
            "React": r'\breact\b',
            "Vue.js": r'\bvue\b',
            "Node.js": r'\b(node|nodejs)\b',
            "SQL": r'\bsql\b',
            "API": r'\bapi\b',
            "REST": r'\brest\b',
            "GraphQL": r'\bgraphql\b',
            "Docker": r'\bdocker\b',
            "AWS": r'\baws\b',
            "Git": r'\bgit\b',
            "Database": r'\b(database|db)\b',
        }
        
        tags = []
        for tag_name, pattern in tech_patterns.items():
            matches = len(re.findall(pattern, text, re.IGNORECASE))
            if matches > 0:
                confidence = min(matches * 0.3, 1.0)  # Макс 0.3 за каждое совпадение
                tags.append({
                    "name": tag_name.lower(),
                    "confidence": confidence
                })
        
        return tags
    
    def _extract_keyword_tags(self, text: str) -> List[Dict]:
        """Извлекает теги на основе ключевых слов"""
        keyword_patterns = {
            "tutorial": r'\b(tutorial|guide|how-to|how to)\b',
            "reference": r'\b(reference|documentation|doc)\b',
            "best-practice": r'\b(best practice|best-practice)\b',
            "testing": r'\b(test|testing|unittest|pytest)\b',
            "security": r'\b(security|secure|authentication|encrypt)\b',
            "performance": r'\b(performance|optimize|fast|slow)\b',
            "beginner": r'\b(beginner|intro|introduction|basic)\b',
            "advanced": r'\b(advanced|expert|professional)\b',
        }
        
        tags = []
        for tag_name, pattern in keyword_patterns.items():
            matches = len(re.findall(pattern, text, re.IGNORECASE))
            if matches > 0:
                confidence = min(matches * 0.25, 0.9)
                tags.append({
                    "name": tag_name,
                    "confidence": confidence
                })
        
        return tags

"""
Auto-tagging service for prompts using keyword analysis
"""
from typing import List, Set
import re


class AutoTaggingService:
    """Service for automatically extracting tags and keywords from prompts"""
    
    # Keywords for different categories
    KEYWORDS_MAPPING = {
        'writing': [
            'написа', 'статья', 'пост', 'контент', 'текст', 'расскаж', 'описа',
            'персонаж', 'история', 'сценарий', 'диалог', 'письмо', 'книга',
            'рифма', 'стихотворение', 'повесть', 'новелла', 'эссе', 'рецензия'
        ],
        'coding': [
            'код', 'программ', 'скрипт', 'функция', 'класс', 'алгоритм',
            'python', 'javascript', 'java', 'c++', 'sql', 'html', 'css',
            'api', 'базе данных', 'бд', 'ошибка', 'отладк', 'тест',
            'фреймворк', 'библиотек', 'интеграция', 'плагин', 'расширение'
        ],
        'analysis': [
            'анализ', 'исследование', 'статистик', 'данные', 'метрик',
            'вывод', 'заключение', 'тенденция', 'сравнение', 'оценка',
            'прогноз', 'интерпретация', 'гипотеза', 'экспертиза', 'обзор'
        ],
        'creative': [
            'идея', 'придум', 'креатив', 'генерация', 'вдохновение',
            'фантазия', 'воображение', 'оригинальн', 'неожиданн',
            'современн', 'модный', 'тренд', 'инновация', 'эксперимент'
        ],
        'translation': [
            'переводи', 'язык', 'английском', 'немецком', 'французском',
            'испанском', 'китайском', 'японском', 'русском', 'локализ',
            'интерпретир', 'вольный перевод', 'адаптация', 'переложение'
        ],
        'education': [
            'учеб', 'обучение', 'школа', 'университет', 'курс', 'лекция',
            'объясни', 'разберемся', 'урок', 'материал', 'экзамен',
            'студент', 'профессор', 'методик', 'педагогик'
        ],
        'business': [
            'бизнес', 'компания', 'проект', 'финанс', 'маркетинг', 'продаж',
            'стратеги', 'планирование', 'бюджет', 'инвестиция', 'прибыль',
            'клиент', 'партнер', 'контракт', 'договор', 'деловой'
        ],
        'health': [
            'здоровь', 'медицин', 'врач', 'болезнь', 'лечение', 'препарат',
            'спорт', 'фитнес', 'диета', 'психолог', 'психический',
            'питание', 'упражнение', 'тренировка', 'рекомендац'
        ],
        'ai': [
            'ии', 'искусственный интеллект', 'машинное обучение', 'нейросеть',
            'гпт', 'трансформер', 'модель', 'обучение', 'предсказание',
            'классификация', 'кластеризация', 'нейтральная', 'nlp'
        ],
        'social': [
            'социальн', 'сеть', 'твитт', 'инстаграм', 'фейсбук', 'тик-ток',
            'пост', 'комментарий', 'лайк', 'поделиться', 'подписка',
            'влияние', 'сообщество', 'онлайн', 'виральный'
        ]
    }
    
    @staticmethod
    def extract_tags(content: str, title: str = "", limit: int = 5) -> List[str]:
        """
        Extract relevant tags from prompt content based on keywords
        
        Args:
            content: Prompt content text
            title: Prompt title
            limit: Maximum number of tags to extract
        
        Returns:
            List of extracted tags
        """
        # Combine title and content for analysis
        text = f"{title} {content}".lower()
        
        # Clean text - remove special characters but keep spaces
        text = re.sub(r'[^а-яА-Яa-zA-Z0-9\s\-\+]', ' ', text)
        
        # Find matching tags
        matched_tags = {}
        
        for category, keywords in AutoTaggingService.KEYWORDS_MAPPING.items():
            for keyword in keywords:
                # Use word boundaries to avoid partial matches
                pattern = r'\b' + keyword + r'[а-я]*\b'
                if re.search(pattern, text):
                    matched_tags[category] = matched_tags.get(category, 0) + 1
        
        # Sort by frequency and return top N
        sorted_tags = sorted(
            matched_tags.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        return [tag[0] for tag in sorted_tags[:limit]]
    
    @staticmethod
    def extract_keywords(content: str, limit: int = 10) -> List[str]:
        """
        Extract important keywords from content for highlighting
        
        Args:
            content: Text content
            limit: Maximum keywords to extract
        
        Returns:
            List of important keywords
        """
        # Get all keywords across all categories
        all_keywords = []
        for keywords in AutoTaggingService.KEYWORDS_MAPPING.values():
            all_keywords.extend(keywords)
        
        # Find occurrences in text
        text = content.lower()
        found_keywords = {}
        
        for keyword in all_keywords:
            pattern = r'\b' + keyword + r'[а-я]*\b'
            count = len(re.findall(pattern, text))
            if count > 0:
                found_keywords[keyword] = count
        
        # Return top keywords by frequency
        sorted_keywords = sorted(
            found_keywords.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        return [kw[0] for kw in sorted_keywords[:limit]]
    
    @staticmethod
    def categorize_prompt(content: str, title: str = "") -> str:
        """
        Automatically determine the best category for a prompt
        
        Args:
            content: Prompt content
            title: Prompt title
        
        Returns:
            Suggested category
        """
        tags = AutoTaggingService.extract_tags(content, title, limit=1)
        return tags[0] if tags else 'general'
    
    @staticmethod
    def highlight_keywords(content: str, keywords: List[str]) -> str:
        """
        Create highlighted version of content with keyword markers
        
        Args:
            content: Original content
            keywords: List of keywords to highlight
        
        Returns:
            Content with highlighted keywords marked as [[keyword]]
        """
        highlighted = content
        
        for keyword in keywords:
            pattern = r'\b(' + keyword + r'[а-я]*)\b'
            replacement = r'[[' + r'\1' + r']]'
            highlighted = re.sub(pattern, replacement, highlighted, flags=re.IGNORECASE)
        
        return highlighted

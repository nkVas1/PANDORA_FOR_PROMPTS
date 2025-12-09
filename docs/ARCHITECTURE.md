# Architecture - PANDORA

## 🏗️ Высокоуровневая архитектура

```
┌─────────────────────────────────────────────────────────────┐
│                    PANDORA Application                      │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌─────────────────────┐         ┌─────────────────────┐   │
│  │   Frontend (HTML)   │         │   Desktop Wrapper   │   │
│  │  ├─ index.html      │◄────────│  PyWebView (C#/JS)  │   │
│  │  ├─ CSS             │         │  Native Window      │   │
│  │  └─ Vanilla JS      │         └─────────────────────┘   │
│  └──────────────┬──────┘                                     │
│                 │ (HTTP API)                                 │
│                 │                                             │
│  ┌──────────────▼──────────────────────────────────────┐   │
│  │         FastAPI Backend (Python)                    │   │
│  ├──────────────────────────────────────────────────┤   │
│  │  Routes & Endpoints                              │   │
│  │  ├─ /api/prompts    (CRUD operations)           │   │
│  │  ├─ /api/projects   (Project management)        │   │
│  │  ├─ /api/tags       (Tag management)            │   │
│  │  ├─ /api/search     (Search functionality)      │   │
│  │  └─ /api/export     (Export operations)         │   │
│  ├──────────────────────────────────────────────────┤   │
│  │  Services Layer (Business Logic)                 │   │
│  │  ├─ PromptService    (Prompt operations)        │   │
│  │  ├─ TaggingService   (Auto-tagging with AI)    │   │
│  │  ├─ SearchService    (Full-text search)        │   │
│  │  └─ ExportService    (Export/Import)           │   │
│  ├──────────────────────────────────────────────────┤   │
│  │  Data Layer (SQLAlchemy ORM)                     │   │
│  │  ├─ Prompt Model                                 │   │
│  │  ├─ Project Model                                │   │
│  │  ├─ Tag Model                                    │   │
│  │  ├─ TagAssociation (M2M Relationship)           │   │
│  │  └─ Database Session Management                 │   │
│  └──────────────────────────────────────────────────┘   │
│                       │                                    │
│  ┌────────────────────▼──────────────────┐               │
│  │  SQLite Database (Development)        │               │
│  │  PostgreSQL Database (Production)     │               │
│  └───────────────────────────────────────┘               │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## 📁 Директория структура

```
PANDORA_FOR_PROMPTS/
│
├── 📂 backend/                          # Python backend
│   ├── 📂 app/
│   │   ├── 📂 models/                   # SQLAlchemy моделі
│   │   │   ├── __init__.py              # Експорт всіх моделей
│   │   │   ├── base.py                  # Базовий клас Model
│   │   │   ├── prompt.py                # Модель Prompt
│   │   │   ├── project.py               # Модель Project
│   │   │   ├── tag.py                   # Модель Tag
│   │   │   └── associations.py          # M2M асоціації
│   │   │
│   │   ├── 📂 routes/                   # API endpoints
│   │   │   ├── __init__.py
│   │   │   ├── prompts.py               # /api/prompts
│   │   │   ├── projects.py              # /api/projects
│   │   │   ├── tags.py                  # /api/tags
│   │   │   ├── search.py                # /api/search
│   │   │   └── export.py                # /api/export
│   │   │
│   │   ├── 📂 services/                 # Бізнес логіка
│   │   │   ├── __init__.py
│   │   │   ├── prompt_service.py        # Операції з промптами
│   │   │   ├── tagging_service.py       # Автотегирование
│   │   │   ├── search_service.py        # Пошук
│   │   │   └── export_service.py        # Експорт/Імпорт
│   │   │
│   │   ├── 📂 schemas/                  # Pydantic схеми
│   │   │   ├── __init__.py
│   │   │   ├── prompt_schema.py         # Request/Response для Prompt
│   │   │   ├── project_schema.py        # Request/Response для Project
│   │   │   └── tag_schema.py            # Request/Response для Tag
│   │   │
│   │   ├── 📂 utils/                    # Утилиты
│   │   │   ├── __init__.py
│   │   │   ├── validators.py            # Валидація даних
│   │   │   ├── constants.py             # Константи
│   │   │   └── helpers.py               # Допоміжні функції
│   │   │
│   │   ├── database.py                  # SQLAlchemy config
│   │   ├── logging_config.py            # Структурований лог
│   │   ├── config.py                    # Конфіг додатка
│   │   └── main.py                      # FastAPI інстанс
│   │
│   ├── 📂 tests/                        # Unit & integration тесты
│   │   ├── conftest.py                  # pytest fixtures
│   │   ├── 📂 test_api/                 # Тесты endpoints
│   │   │   ├── test_prompts.py
│   │   │   ├── test_projects.py
│   │   │   └── test_tags.py
│   │   ├── 📂 test_services/            # Тесты сервисов
│   │   │   └── test_tagging_service.py
│   │   └── 📂 test_models/              # Тесты моделей
│   │       └── test_prompt_model.py
│   │
│   └── requirements.txt                 # Python зависимости
│
├── 📂 frontend/                         # HTML/CSS/JS frontend
│   ├── index.html                       # Головна сторінка
│   ├── 📂 css/
│   │   ├── style.css                    # Основні стилі
│   │   ├── theme.css                    # Тема оформлення
│   │   └── animations.css               # Анімації
│   │
│   ├── 📂 js/
│   │   ├── main.js                      # Головний скрипт
│   │   ├── api-client.js                # API клієнт
│   │   ├── ui-handler.js                # Обробка UI
│   │   └── utils.js                     # Утиліти
│   │
│   └── 📂 images/
│       └── logo.png                     # Логотип
│
├── 📂 .github/                          # GitHub конфіг
│   └── 📂 workflows/
│       ├── tests.yml                    # CI/CD для тестів
│       └── build.yml                    # CI/CD для білда
│
├── 📂 docs/                             # Документація
│   ├── ARCHITECTURE.md                  # Цей файл
│   ├── API.md                           # API документація
│   ├── DEVELOPMENT.md                   # Розробка
│   ├── TESTING_GUIDE.md                 # Тестирование
│   ├── DEPLOYMENT.md                    # Розгортання
│   └── DATABASE_SCHEMA.md               # Схема БД
│
├── 📂 data/                             # Локальні дані
│   ├── 📂 prompts/                      # Експортовані промпты
│   ├── 📂 imports/                      # Імпортовані дані
│   └── 📂 projects/                     # Дані проектів
│
├── launcher_final.py                    # Точка входу (PyWebView)
├── splash_screen.py                     # Екран загрузки (tkinter)
├── requirements.txt                     # Root зависимості
├── pytest.ini                           # pytest конфіг
├── .pre-commit-config.yaml              # Pre-commit hooks
├── .gitignore                           # Git ignore
├── README.md                            # Проект README
└── LICENSE                              # Ліцензія
```

## 🔄 Потоки (Flow) запиту

### Приклад 1: Отримання всіх промптів

```
1. Frontend (js/main.js)
   GET /api/prompts
         │
         ▼
2. Backend: Route Handler (routes/prompts.py)
   @router.get("/")
   async def get_prompts()
         │
         ▼
3. Service Layer (services/prompt_service.py)
   get_all_prompts() ──► Database Query
         │
         ▼
4. Data Layer (database.py)
   SELECT * FROM prompts
         │
         ▼
5. SQLAlchemy ORM
   Преобразует Row в Prompt Model
         │
         ▼
6. Service
   Перетворює Model в PromptResponse
         │
         ▼
7. Route
   Повертає JSON
         │
         ▼
8. FastAPI
   Сериализует Response
         │
         ▼
9. Frontend (api-client.js)
   Отримує JSON, оновлює UI
```

### Приклад 2: Створення промпту з автотегированием

```
1. Frontend (POST /api/prompts)
   {
     "title": "My Prompt",
     "content": "..."
   }
         │
         ▼
2. Route Handler (routes/prompts.py)
   validate(data) ──► PromptCreate schema
         │
         ▼
3. Service Layer (services/prompt_service.py)
   create_prompt(data)
         │
         ├─► Database: INSERT prompt
         │
         └─► Tagging Service (auto-generate tags)
             tagging_service.generate_tags(content)
             │
             └─► LLM API / ML Model
                 Returns: ["python", "coding", ...]
                 │
                 └─► Link tags to prompt in DB
         │
         ▼
4. Database
   INSERT INTO prompts (title, content, ...)
   INSERT INTO tag_associations (prompt_id, tag_id)
         │
         ▼
5. Response
   Return: { id, title, content, tags, created_at }
         │
         ▼
6. Frontend
   Update UI with new prompt
```

## 💾 Модели та схеми

### Модель Prompt

```python
class Prompt(Base):
    __tablename__ = "prompts"
    
    id: int (primary key)
    title: str (unique, indexed)
    content: str (full-text indexed)
    description: str (optional)
    category: str (indexed)
    tags: List[Tag] (M2M relationship)
    project_id: int (foreign key)
    created_at: datetime
    updated_at: datetime
    is_favorite: bool
    usage_count: int
    rating: float
```

### Модель Project

```python
class Project(Base):
    __tablename__ = "projects"
    
    id: int (primary key)
    name: str (unique, indexed)
    description: str
    icon: str (emoji)
    color: str (hex)
    prompts: List[Prompt] (1-N relationship)
    created_at: datetime
    updated_at: datetime
```

### Модель Tag

```python
class Tag(Base):
    __tablename__ = "tags"
    
    id: int (primary key)
    name: str (unique, indexed)
    description: str
    color: str (hex)
    prompts: List[Prompt] (M2M relationship)
    created_at: datetime
```

## 🔐 Безопасность

### Валідація даних
```python
# Pydantic автоматично валідує:
class PromptCreate(BaseModel):
    title: str  # обов'язкове поле
    content: str  # обов'язкове поле
    category: str = "general"  # значення за замовченням
    
    @field_validator('title')
    @classmethod
    def title_not_empty(cls, v):
        if not v.strip():
            raise ValueError('Title cannot be empty')
        return v
```

### SQL Injection захист
```python
# SQLAlchemy параметризовані запити
# БЕЗПЕЧНО:
db.query(Prompt).filter(Prompt.id == prompt_id)

# НЕБЕЗПЕЧНО:
db.execute(f"SELECT * FROM prompts WHERE id = {prompt_id}")
```

### CORS конфигурація
```python
# fastapi/main.py
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Тільки локальні
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## 📈 Масштабування

### Поточні обмеження
- SQLite (одночасність)
- Однопоточний (sync endpoints)
- Без кешування

### Для масштабування
1. **БД**: Міграція на PostgreSQL
2. **Async**: Асинхронні endpoint'и
3. **Cache**: Redis для часто використовуваних даних
4. **Queue**: Celery для довгих операцій (експорт, теггирование)
5. **Search**: Elasticsearch для повнотекстового пошуку

## 🧪 Тестова архітектура

```
Тести виконуються в ізоляції:
│
├── Fixture: db_session (in-memory SQLite)
│   ├── Перед тестом: CREATE TABLE
│   ├── Під час тесту: ROLLBACK після кожної операції
│   └── Після тесту: DROP TABLE
│
├── Fixture: client (TestClient)
│   └── Налаштований на тестову БД
│
└── Fixture: sample_data
    └── Готові дані для тестування
```

## 📊 Залежності

### Backend

| Назва | Версія | Причина |
|-------|--------|---------|
| FastAPI | 0.104+ | REST API фреймворк |
| SQLAlchemy | 2.0+ | ORM для БД |
| Pydantic | 2.0+ | Валідація даних |
| pytest | 7.4+ | Unit тестирование |
| python-telegram-bot | 20+ | Інтеграція Telegram |

### Desktop

| Назва | Версія | Причина |
|-------|--------|---------|
| pywebview | 5.3+ | Нативне вікно |
| tkinter | 3.10+ | Splash screen |
| Pillow | 10+ | Обробка зображень |

## 🚀 Performance Optimization

### Поточні оптимізації

1. **Database**
   - Indexed поля: id, title, category, created_at
   - Foreign keys для quick joins
   - Connection pooling

2. **API**
   - Pagination для списків
   - Selective field loading
   - Кешування відповідей (Cache-Control)

3. **Frontend**
   - Lazy loading списків
   - Debounce пошуку
   - Virtual scrolling для великих списків

### Моніторинг

```python
# logging_config.py - всі операції логуються
logger.info("Query executed", extra={
    "table": "prompts",
    "duration_ms": 45,
    "rows": 250
})
```

## 🔗 Інтеграції

### Текущі
- Telegram Bot (python-telegram-bot)
- Local file storage
- SQLite/PostgreSQL

### Планове
- OpenAI API (GPT для автотегирования)
- GitHub (синхронізація)
- Slack (notifications)
- Google Drive (backup)

## 📝 API Документація

FastAPI автоматично генерує:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

Кожен endpoint документується через docstring:

```python
@router.post("/api/prompts", tags=["Prompts"])
async def create_prompt(
    prompt_data: PromptCreate,
    db: Session = Depends(get_db)
) -> PromptResponse:
    """
    Створює новий промпт.
    
    - **title**: Назва промпту (обов'язково)
    - **content**: Текст промпту (обов'язково)
    - **category**: Категорія (опціонально)
    
    Повертає: Об'єкт Prompt з ID та timestamps
    """
    pass
```

---

**Останнє оновлення**: 2024-12-20  
**Версія документації**: 2.0  
**Совместимість**: Python 3.10+, FastAPI 0.104+

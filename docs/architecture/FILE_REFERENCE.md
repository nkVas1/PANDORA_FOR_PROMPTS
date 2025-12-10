# 📂 Complete File Structure & Reference Guide

Полный справочник всех файлов проекта PANDORA for PROMPTS.

## 📋 Quick File Finder

**Быстро найти нужный файл по категориям:**

### Хочу запустить приложение
- `start.py` - главный скрипт запуска ⭐
- `.env.example` - переменные окружения
- `QUICK_START.md` - инструкция за 5 минут

### Хочу разрабатывать backend
- `backend/app/main.py` - точка входа FastAPI
- `backend/app/api/routes.py` - все endpoints ⭐
- `backend/app/services/database.py` - бизнес-логика ⭐
- `backend/app/db/models.py` - ORM модели
- `backend/requirements.txt` - зависимости

### Хочу разрабатывать frontend
- `frontend/app/page.tsx` - главная страница
- `frontend/components/` - UI компоненты
- `frontend/lib/api.ts` - API клиент ⭐
- `frontend/lib/store.ts` - состояние ⭐
- `frontend/package.json` - зависимости

### Хочу собрать exe файл
- `build.py` - скрипт сборки ⭐
- `backend/requirements.txt` - зависимости Python

### Хочу прочитать документацию
- `README.md` - основная документация
- `docs/INDEX.md` - навигация по документам ⭐
- `QUICK_START.md` - быстрый старт
- `docs/API.md` - API документация

### Что-то не работает
- `TROUBLESHOOTING.md` - решение проблем ⭐
- `docs/IDE_INTEGRATION.md` - настройка IDE

---

## 🗂️ Complete Directory Tree

```
PANDORA_FOR_PROMPTS-main/
│
├── 📄 README.md                        Главная документация
├── 📄 QUICK_START.md                   5-минутный старт ⭐
├── 📄 FINAL_CHECKLIST.md               Статус проекта
├── 📄 VERSION.md                       История версий
├── 📄 ROADMAP.md                       План развития
├── 📄 CHANGELOG.md                     История изменений
├── 📄 CONTRIBUTING.md                  Гайд контрибьютинга
├── 📄 TROUBLESHOOTING.md               Решение проблем ⭐
├── 📄 PROJECT_STATISTICS.md            Статистика
├── 📄 LICENSE                          MIT лицензия
├── 📄 .gitignore                       Git игнор
├── 📄 .env.example                     Пример переменных
│
├── 🐍 start.py                         Главный скрипт запуска ⭐⭐⭐
├── 🐍 build.py                         Сборка exe файла ⭐⭐
├── 🐍 import_data.py                   Импорт данных
│
├── 📁 backend/                         Python FastAPI приложение
│   ├── 📄 run.py                       Runner для Uvicorn
│   ├── 📄 requirements.txt             Python зависимости ⭐
│   │
│   └── app/
│       ├── 📄 main.py                  Инициализация FastAPI ⭐
│       ├── 📄 config.py                Конфигурация
│       │
│       ├── 📁 api/
│       │   └── 📄 routes.py            Все REST endpoints ⭐⭐⭐
│       │
│       ├── 📁 models/
│       │   └── 📄 schemas.py           Pydantic валидация ⭐
│       │
│       ├── 📁 db/
│       │   ├── 📄 __init__.py          Инициализация БД
│       │   └── 📄 models.py            SQLAlchemy ORM модели ⭐
│       │
│       ├── 📁 services/
│       │   └── 📄 database.py          Бизнес-логика ⭐⭐
│       │
│       ├── 📁 utils/
│       │   ├── 📄 auto_tagger.py       Auto-tagging система ⭐
│       │   └── 📄 importer.py          JSON importer
│       │
│       └── 📁 tests/                   Пусто (в v1.1)
│
├── 📁 frontend/                        Next.js React приложение
│   ├── 📄 package.json                 npm зависимости ⭐
│   ├── 📄 tsconfig.json                TypeScript конфиг
│   ├── 📄 tailwind.config.ts           Tailwind настройка
│   ├── 📄 next.config.ts               Next.js конфиг
│   ├── 📄 .eslintrc.json               ESLint правила
│   │
│   ├── app/
│   │   ├── 📄 layout.tsx               Root layout
│   │   ├── 📄 page.tsx                 Home page ⭐
│   │   └── 📄 globals.css              Глобальные стили
│   │
│   ├── 📁 components/                  UI компоненты
│   │   ├── 📄 Button.tsx               Кнопка
│   │   ├── 📄 Card.tsx                 Карточка
│   │   ├── 📄 Input.tsx                Поле ввода
│   │   ├── 📄 Textarea.tsx             Многострочный ввод
│   │   ├── 📄 Tag.tsx                  Badge
│   │   ├── 📄 Modal.tsx                Диалог
│   │   └── 📄 PromptHeader.tsx         Хедер ⭐
│   │
│   └── lib/
│       ├── 📄 api.ts                   API клиент ⭐⭐
│       └── 📄 store.ts                 Zustand store ⭐⭐
│
├── 📁 data/                            Данные (gitignored)
│   └── pandora.db                      SQLite база данных
│
├── 📁 docs/                            Документация
│   ├── 📄 INDEX.md                     Навигация по документам ⭐
│   ├── 📄 SETUP.md                     Установка
│   ├── 📄 API.md                       REST API ⭐
│   ├── 📄 USER_GUIDE.md                Руководство пользователя
│   ├── 📄 DEVELOPMENT.md               Гайд разработки ⭐
│   ├── 📄 IDE_INTEGRATION.md           Интеграция с IDE
│   ├── 📄 CI_CD.md                     GitHub Actions
│   ├── 📄 GITHUB_PAGES.md              GitHub Pages публикация
│   └── 📁 images/                      Скриншоты (опционально)
│
├── 📁 references/                      (gitignored) Исходные данные
│   └── ... prompt libraries ...
│
└── 📁 .github/                         GitHub конфиг (создать)
    ├── 📁 workflows/                   CI/CD scripts
    │   ├── 📄 tests.yml                (создать)
    │   ├── 📄 build.yml                (создать)
    │   └── 📄 deploy.yml               (опционально)
    └── 📁 ISSUE_TEMPLATE/              (опционально)
        └── 📄 bug_report.md
```

---

## 📄 Файлы в корне проекта

### Главные скрипты

| Файл | Размер | Назначение | Запуск |
|------|--------|-----------|--------|
| **start.py** ⭐⭐⭐ | 25 KB | Главный стартер | `python start.py` |
| **build.py** ⭐⭐ | 8 KB | Сборка exe | `python build.py` |
| **import_data.py** | 6 KB | Импорт данных | `python import_data.py` |

### Документация

| Файл | Размер | Для кого | Читать |
|------|--------|---------|--------|
| **README.md** ⭐ | 10 KB | Все | Первым |
| **QUICK_START.md** ⭐ | 7 KB | Новые пользователи | Вторым |
| **FINAL_CHECKLIST.md** | 8 KB | PM, Lead | После README |
| **VERSION.md** | 11 KB | Разработчики | После кода |
| **ROADMAP.md** | 18 KB | Планирование | Для планов |
| **CHANGELOG.md** | 7 KB | Все | При обновлении |
| **TROUBLESHOOTING.md** ⭐ | 11 KB | При ошибках | При проблемах |
| **CONTRIBUTING.md** | 2 KB | Контрибьюторы | Перед PR |
| **PROJECT_STATISTICS.md** | 12 KB | Аналитика | Для метрик |
| **LICENSE** | 1 KB | Юристы | Редко |

### Конфиг файлы

| Файл | Назначение | Обязательный |
|------|-----------|------------|
| **.env.example** | Пример переменных | ✅ Yes |
| **.env** | Ваши переменные | ✅ Yes (создайте из example) |
| **.gitignore** | Git игнор | ✅ Yes |

---

## 📁 Backend файлы

### Основной код

```python
backend/
├── run.py                          # Uvicorn runner
├── requirements.txt                # pip зависимости (12)
└── app/
    ├── main.py                     # FastAPI инициализация
    ├── config.py                   # Конфиг (40 lines)
    ├── api/
    │   └── routes.py               # 24+ endpoints (280 lines) ⭐
    ├── models/
    │   └── schemas.py              # Pydantic (200 lines)
    ├── db/
    │   ├── __init__.py             # Session factory
    │   └── models.py               # ORM models (100 lines) ⭐
    ├── services/
    │   └── database.py             # Services (250 lines) ⭐
    └── utils/
        ├── auto_tagger.py          # Auto-tag engine (180 lines) ⭐
        └── importer.py             # JSON importer (60 lines)
```

### Важные файлы backend

| Файл | Строк | Обязателен | Примечание |
|------|-------|-----------|-----------|
| routes.py | 280 | ✅ | Все endpoints |
| database.py | 250 | ✅ | Бизнес-логика |
| models.py (db) | 100 | ✅ | ORM структура |
| auto_tagger.py | 180 | ✅ | Tagging логика |
| schemas.py | 200 | ✅ | Валидация |
| main.py | 40 | ✅ | FastAPI app |
| requirements.txt | 12 | ✅ | Зависимости |

---

## 📁 Frontend файлы

### Основной код

```typescript
frontend/
├── package.json                    # npm config (40 lines)
├── tsconfig.json                   # TypeScript config
├── tailwind.config.ts              # Tailwind config
├── next.config.ts                  # Next.js config
├── .eslintrc.json                  # ESLint config
├── app/
│   ├── layout.tsx                  # Root layout
│   ├── page.tsx                    # Home page (140 lines) ⭐
│   └── globals.css                 # Глобальные стили (100+ lines)
├── components/                     # 7+ компонентов
│   ├── Button.tsx
│   ├── Card.tsx
│   ├── Input.tsx
│   ├── Textarea.tsx
│   ├── Tag.tsx
│   ├── Modal.tsx
│   └── PromptHeader.tsx            # Хедер (60 lines)
└── lib/
    ├── api.ts                      # API клиент (70 lines) ⭐
    └── store.ts                    # Zustand (80 lines) ⭐
```

### Важные файлы frontend

| Файл | Строк | Обязателен | Примечание |
|------|-------|-----------|-----------|
| api.ts | 70 | ✅ | API endpoints |
| store.ts | 80 | ✅ | State management |
| page.tsx | 140 | ✅ | Home page |
| components/* | 200 | ✅ | UI компоненты |
| package.json | 40 | ✅ | Dependencies |
| tsconfig.json | 20 | ✅ | TypeScript |

---

## 📚 Documentation Files

### В папке docs/

| Файл | Строк | Назначение | Читает |
|------|-------|-----------|--------|
| INDEX.md | 300 | Навигация | Все ⭐⭐ |
| SETUP.md | 150 | Установка | Новые пользователи |
| API.md | 350 | REST API | Разработчики ⭐ |
| USER_GUIDE.md | 250 | Пользователи | Конечные пользователи |
| DEVELOPMENT.md | 400 | Разработка | Разработчики ⭐ |
| IDE_INTEGRATION.md | 300 | IDE setup | Разработчики |
| CI_CD.md | 150 | GitHub Actions | DevOps |
| GITHUB_PAGES.md | 200 | Публикация | DevOps |

---

## 🔒 Git Ignored Files

Эти файлы НЕ коммитятся (в .gitignore):

```
# Python
__pycache__/
*.pyc
*.pyo
*.egg-info/
.Python
.venv/
venv/
env/

# Node.js
node_modules/
package-lock.json
.next/
dist/

# IDE
.vscode/
.idea/
*.swp
*.swo

# Environment
.env
.env.local
.env.*.local

# Data & Logs
data/
*.db
*.log
logs/

# Build
build/
dist/
*.egg

# OS
.DS_Store
Thumbs.db

# References (опционально)
references/

# Testing
.coverage
htmlcov/
.pytest_cache/

# IDE temp files
*.sublime-project
*.sublime-workspace
```

---

## 📊 File Size Statistics

### По типам файлов

| Тип | Количество | Общий размер | Примечание |
|-----|-----------|-------------|-----------|
| **Python (.py)** | 15+ | ~200 KB | Backend логика |
| **TypeScript (.ts/tsx)** | 20+ | ~80 KB | Frontend компоненты |
| **Markdown (.md)** | 17 | ~180 KB | Документация |
| **Config (json/yaml)** | 10 | ~50 KB | Конфигурация |
| **Other** | 10 | ~30 KB | License, .env и т.д. |
| **Total** | **70+** | **~540 KB** | Без node_modules, venv |

---

## 🔑 Key Files Summary

### 🌟 Must-Have Files (Требуются для запуска)

1. **start.py** - запуск приложения ⭐⭐⭐
2. **.env** - переменные окружения ⭐⭐⭐
3. **backend/requirements.txt** - Python deps ⭐⭐
4. **frontend/package.json** - npm deps ⭐⭐
5. **backend/app/main.py** - FastAPI app ⭐⭐
6. **frontend/app/page.tsx** - React app ⭐⭐

### ⭐ Important Files (Для разработки)

1. **backend/app/api/routes.py** - endpoints ⭐⭐⭐
2. **backend/app/services/database.py** - logic ⭐⭐⭐
3. **frontend/lib/api.ts** - API client ⭐⭐
4. **frontend/lib/store.ts** - state ⭐⭐
5. **docs/API.md** - documentation ⭐⭐
6. **QUICK_START.md** - quick guide ⭐⭐

### 📚 Documentation Files (Для обучения)

1. **README.md** - overview
2. **docs/INDEX.md** - navigation
3. **docs/DEVELOPMENT.md** - architecture
4. **TROUBLESHOOTING.md** - solutions
5. **ROADMAP.md** - future plans
6. **VERSION.md** - versioning

---

## 🎯 File Organization Best Practices

### Backend структура

```
backend/
├── app/
│   ├── api/                    # HTTP layer (routes)
│   ├── models/                 # Data layer (schemas)
│   ├── db/                     # Database (ORM)
│   ├── services/               # Business logic
│   ├── utils/                  # Helper functions
│   └── main.py                 # App initialization
├── tests/                      # Unit tests
└── requirements.txt            # Dependencies
```

### Frontend структура

```
frontend/
├── app/                        # Next.js pages
│   ├── page.tsx               # Routes
│   └── layout.tsx             # Layouts
├── components/                # Reusable components
├── lib/                       # Utilities & API client
├── styles/                    # CSS/Tailwind
└── package.json               # Dependencies
```

---

## 🔄 File Dependencies

### Главные зависимости файлов

```
start.py
├── backend/run.py (запускает)
├── backend/app/main.py (импортирует)
├── frontend/package.json (npm install)
└── .env (конфиг)

build.py
├── backend/requirements.txt
├── frontend/package.json
└── backend/app/main.py

routes.py (зависит от)
├── models/schemas.py
├── db/models.py
└── services/database.py

api.ts (зависит от)
└── Zustand store (опционально)

store.ts (зависит от)
└── api.ts (для fetch)
```

---

## 📋 Checklist для файлов

### При запуске убедитесь что есть

- [ ] `.env` создан из `.env.example`
- [ ] `backend/requirements.txt` существует
- [ ] `frontend/package.json` существует
- [ ] `start.py` доступен
- [ ] `data/` папка создана (или будет создана автоматически)

### При разработке следите за

- [ ] `backend/app/api/routes.py` - правильные endpoints
- [ ] `frontend/lib/api.ts` - синхронизирован с routes
- [ ] `backend/app/db/models.py` - свежая схема БД
- [ ] `frontend/lib/store.ts` - актуальное состояние
- [ ] Documentation обновлена

### При деплойе проверьте

- [ ] `build.py` запущен успешно
- [ ] `dist/PANDORA.exe` создан
- [ ] `.env` файл НЕ коммичен
- [ ] `data/` НЕ коммичен (если не нужны sample данные)
- [ ] Git tags добавлены (v1.0.0, и т.д.)

---

## 🔍 Как найти конкретный функционал

### Хочу добавить новый endpoint
1. Открыть `backend/app/api/routes.py`
2. Добавить функцию в правильный раздел (prompts, tags, etc.)
3. Добавить Pydantic schema в `backend/app/models/schemas.py`
4. Добавить сервис метод в `backend/app/services/database.py`

### Хочу добавить новый компонент
1. Создать файл в `frontend/components/`
2. Экспортировать из `components/index.ts`
3. Импортировать в нужном месте
4. Добавить в `frontend/app/page.tsx`

### Хочу добавить новую страницу
1. Создать папку в `frontend/app/`
2. Добавить `page.tsx` в папку
3. Импортировать компоненты
4. Использовать API из `frontend/lib/api.ts`

### Хочу обновить документацию
1. Найти файл в `docs/`
2. Отредактировать markdown
3. Проверить formatting (`npx remark .`)
4. Commitить с сообщением на русском

---

## 🚀 Fast Reference

### Команды для работы с файлами

```bash
# Просмотр структуры
tree /F                                    # Windows
ls -la                                     # macOS/Linux

# Поиск файлов
find . -name "*.py"                        # Python файлы
find . -name "*.tsx"                       # React файлы
find . -name "*.md"                        # Документация

# Подсчет строк
wc -l backend/app/api/routes.py            # 1 файл
find backend -name "*.py" | xargs wc -l    # Все Python файлы
```

---

## 📞 File Locations Quick Reference

| Что ищу | Файл | Путь |
|---------|------|------|
| Все endpoints | routes.py | `backend/app/api/` |
| Модели БД | models.py | `backend/app/db/` |
| Сервисы | database.py | `backend/app/services/` |
| API клиент | api.ts | `frontend/lib/` |
| Компоненты | *.tsx | `frontend/components/` |
| Главная страница | page.tsx | `frontend/app/` |
| API документация | API.md | `docs/` |
| Быстрый старт | QUICK_START.md | ROOT |
| Помощь | TROUBLESHOOTING.md | ROOT |

---

**Последнее обновление**: January 2025
**Для версии**: 1.0.0
**Всего файлов**: 70+

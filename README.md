# 🎨 PANDORA - Professional Prompt Manager
## Desktop Application | AI-Powered | Modern UI | 2.0 Architecture

![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.10.11-green.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.124.0-red.svg)
![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen.svg)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

---

## 📋 Описание

**PANDORA v2.0.0** - это профессиональное десктопное приложение для управления AI промптами с полной переработкой архитектуры, современным интерфейсом и продвинутым функционалом. Включает 5 полноценных views, реактивное управление состоянием и аналитику.

### ✨ What's New in v2.0

- 🎨 **Новая архитектура фронтенда** - Дизайн система, реактивный стейт, профессиональный роутер
- 📊 **Аналитика и статистика** - 3 новых endpoint'а для insights и метрик
- 🧵 **Thread-safe splash screen** - Красивый загрузочный экран с очередью обновлений
- 💾 **Улучшенное логирование** - Все логи в `dist/logs/` с удобным форматом
- 🏠 **5 полных Views** - Dashboard, Prompts, Editor, Projects, Analytics
- 🔄 **Продвинутый стейт** - Undo/Redo, computed properties, middleware support
- 🛣️ **Профессиональный роутер** - Guards, hooks, параметры, история
- ⚡ **Оптимизированный запуск** - < 5 сек от splash к UI

---

## 🏗️ Архитектура v2.0

### Frontend Stack (2,100+ lines)

- **Design System**: CSS переменные, типография, палитра, анимации (`tokens.css`)
- **State Management**: Реактивный proxy, observers, computed properties (`state-manager.js`)
- **Router**: Hash-based navigation с guards и hooks (`router.js`)
- **Views**: 5 complete implementations (Dashboard, Prompts, Editor, Projects, Analytics)
- **App Init**: Полная инициализация компонентов (`app.js`)

### Backend Stack (650+ lines)

- **Framework**: FastAPI 0.124.0
- **Server**: Uvicorn 0.38.0
- **Database**: SQLite (local)
- **ORM**: SQLAlchemy 2.0.44
- **API**: 50+ endpoints covering all operations

### Desktop Stack

- **Framework**: PyWebView 6.1
- **Launcher**: Professional manager with daemon threading
- **Splash**: Thread-safe UI with queue-based updates
- **Builder**: PyInstaller with optimized configuration
- **OS**: Windows 10/11 (x64)

---

## 🚀 Быстрый старт

### Требования

- **Python 3.9+**
- **Node.js 18+**
- **npm или yarn**

### 1. Установка зависимостей

```bash
# Backend
cd backend
pip install -r requirements.txt
cd ..

# Frontend
cd frontend
npm install
cd ..
```

### 2. Запуск приложения

```bash
python start.py
```

### 3. Открыть приложение

- **Frontend**: http://127.0.0.1:3000
- **API Docs**: http://127.0.0.1:8000/docs

---

## 📖 Использование

### Управление Промптами

1. **Добавить промпт** - Перейдите на вкладку "Промпты" и нажмите "Добавить"
2. **Поиск и фильтрация** - Используйте поле поиска или фильтры по категориям
3. **Автотегирование** - Система автоматически предложит релевантные теги
4. **Массовый импорт** - Загружайте промпты пакетом из JSON файлов

### Управление Проектами

1. **Создать проект** - Перейдите на вкладку "Проекты"
2. **Вести процесс разработки** - Добавляйте записи о ходе разработки
3. **Управление задачами** - Создавайте и отслеживайте задачи с приоритетами

---

## 🔌 API Endpoints

```
Промпты:
  POST   /api/prompts               # Создать
  GET    /api/prompts               # Получить все
  GET    /api/prompts/search        # Поиск
  GET    /api/prompts/{id}          # Получить один
  PUT    /api/prompts/{id}          # Обновить
  DELETE /api/prompts/{id}          # Удалить

Теги:
  GET    /api/tags                  # Получить все
  POST   /api/tags                  # Создать
  DELETE /api/tags/{id}             # Удалить

Проекты:
  GET    /api/projects              # Получить все
  POST   /api/projects              # Создать
  PUT    /api/projects/{id}         # Обновить
  DELETE /api/projects/{id}         # Удалить

Статистика:
  GET    /api/stats                 # Получить статистику
```

Полная документация: http://127.0.0.1:8000/docs

---

## 📦 Импорт данных

Приложение поддерживает импорт промптов из:
- agent-prompt-library
- ai-prompts
- awesome-prompts
- И других источников в папке references/

---

## 🎨 Темизация

Приложение использует темный UI с Tailwind CSS:
- Primary Color: Синий (#3b82f6)
- Background: Темный (#111827)
- Surface: Темный (#1f2937)

---

---

## 📚 Документация

| Документ | Описание |
|----------|---------|
| [QUICK_START.md](QUICK_START.md) | 5-минутный гайд для быстрого запуска |
| [docs/SETUP.md](docs/SETUP.md) | Подробная инструкция установки |
| [docs/API.md](docs/API.md) | Полная документация REST API |
| [docs/USER_GUIDE.md](docs/USER_GUIDE.md) | Руководство пользователя (exe версия) |
| [docs/DEVELOPMENT.md](docs/DEVELOPMENT.md) | Гайд для разработчиков |
| [docs/CI_CD.md](docs/CI_CD.md) | GitHub Actions workflows |
| [docs/GITHUB_PAGES.md](docs/GITHUB_PAGES.md) | Развертывание документации |
| [FINAL_CHECKLIST.md](FINAL_CHECKLIST.md) | Полный чек-лист проекта |
| [VERSION.md](VERSION.md) | История версий и план развития |
| [CHANGELOG.md](CHANGELOG.md) | История изменений |
| [CONTRIBUTING.md](CONTRIBUTING.md) | Руководство для контрибьюторов |

---

## 🔗 Полезные ссылки

- 📖 [Документация FastAPI](https://fastapi.tiangolo.com/)
- 📖 [Документация Next.js](https://nextjs.org/docs)
- 📖 [Документация Tailwind CSS](https://tailwindcss.com/)
- 📖 [Документация SQLAlchemy](https://docs.sqlalchemy.org/)
- 🐍 [Python Documentation](https://docs.python.org/3/)
- ⚛️ [React Documentation](https://react.dev/)

---

## 🤝 Контрибьюция

Вклады приветствуются! Пожалуйста:

1. Форкните репозиторий
2. Создайте feature branch (`git checkout -b feature/amazing-feature`)
3. Коммитьте изменения (`git commit -m 'Add amazing feature'`)
4. Пушьте в branch (`git push origin feature/amazing-feature`)
5. Откройте Pull Request

Подробнее: [CONTRIBUTING.md](CONTRIBUTING.md)

---

## 🐛 Баги и Фичи

Нашли баг или есть идея? Откройте [issue на GitHub](https://github.com/yourusername/PANDORA_FOR_PROMPTS/issues)

---

## 📞 Поддержка

- 📧 Email: `support@pandora-prompts.local`
- 💬 [GitHub Discussions](https://github.com/yourusername/PANDORA_FOR_PROMPTS/discussions)
- 📋 [GitHub Issues](https://github.com/yourusername/PANDORA_FOR_PROMPTS/issues)
- 🎯 [Roadmap](VERSION.md)

---

## 📊 Статистика проекта

| Метрика | Значение |
|---------|----------|
| Backend endpoints | 20+ |
| Database models | 5 |
| Frontend components | 7+ |
| Unit test coverage | В разработке |
| Documentation pages | 8+ |
| Lines of code | 2000+ |
| License | MIT |
| Python version | 3.9+ |
| Node.js version | 18+ |

---

## 🗺️ Дорожная карта

**v1.0.0** ✅ (Current)

- FastAPI backend
- Next.js frontend
- Auto-tagging
- Full documentation

**v1.1.0** 🚧 (Q2 2025)

- Full UI implementation
- Unit tests
- Export to CSV/PDF
- Keyboard shortcuts

**v1.2.0** 📋 (Q3-Q4 2025)

- Multi-user support
- Cloud sync
- Advanced features

**v2.0.0** 📅 (2025-2026)

- ML-based tagging
- Semantic search
- Web/Mobile versions

Подробнее: [VERSION.md](VERSION.md)

---

## 📄 Лицензия

Проект распространяется под лицензией **MIT License** - см. файл [LICENSE](LICENSE)

```text
MIT License

Copyright (c) 2024-2025 PANDORA Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
```

---

## ✨ Благодарности

Спасибо всем, кто использует и поддерживает этот проект! 🙏

- Вдохновение от лучших prompt management инструментов
- Сообщество open-source разработчиков
- Все контрибьюторы проекта

---

## 🎉 Спасибо за использование PANDORA

Сделано с ❤️ для профессионального управления промптами

**PANDORA for PROMPTS** - ваш локальный органайзер для AI промптов

Начните прямо сейчас: `python start.py`

Посетите: [`http://127.0.0.1:3000`](http://127.0.0.1:3000)

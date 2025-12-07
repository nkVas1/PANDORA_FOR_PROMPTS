# 🚀 PANDORA - Prompts Manager

[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/downloads/)
[![Node.js](https://img.shields.io/badge/Node.js-18%2B-green.svg)](https://nodejs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-009688.svg)](https://fastapi.tiangolo.com/)
[![Next.js](https://img.shields.io/badge/Next.js-15.0-black.svg)](https://nextjs.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-brightgreen.svg)](https://github.com/)

---

## 📋 Описание

**PANDORA** - это профессиональный инструмент для управления, структуризации и распределения промптов (текстовых запросов для нейросетей). Приложение предоставляет удобный интерфейс для сохранения промптов, автоматического распределения по категориям, генерации тегов, ведения истории разработки проектов и управления задачами.

### ✨ Ключевые возможности

- 💾 **Локальное хранилище** - Все данные хранятся на вашем компьютере
- 🏷️ **Автотегирование** - Автоматическое распределение по категориям и генерация релевантных тегов
- 🔍 **Умный поиск** - Быстрый поиск по названию, содержимому, тегам и категориям
- 📁 **Управление проектами** - Ведите процесс разработки и список задач
- 📤 **Массовый импорт** - Загружайте промпты пакетом из JSON файлов
- 🎨 **Современный UI** - Стильный интерфейс в темной теме с Tailwind CSS
- 📊 **Статистика** - Отслеживание использования и популярности промптов
- ⚡ **Быстрая работа** - Оптимизированная база данных SQLite

---

## 🏗️ Архитектура

### Backend
- **Framework**: FastAPI (Python)
- **Database**: SQLite с SQLAlchemy ORM
- **Features**:
  - REST API для управления промптами
  - Автоматическое тегирование на основе анализа текста
  - Поддержка массового импорта
  - Управление проектами и задачами

### Frontend
- **Framework**: Next.js 15 (React 19)
- **Styling**: Tailwind CSS + Dark Theme
- **State Management**: Zustand
- **UI Components**: Custom components

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

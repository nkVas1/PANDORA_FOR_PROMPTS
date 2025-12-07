# Инструкция по установке и запуску

## Системные требования

- **ОС**: Windows 10+, macOS 10.14+, Linux (Ubuntu 18.04+)
- **Python**: 3.9 или выше
- **Node.js**: 18 или выше
- **npm**: 9 или выше

## Установка зависимостей

### 1. Клонируйте репозиторий

```bash
git clone https://github.com/yourusername/PANDORA_FOR_PROMPTS.git
cd PANDORA_FOR_PROMPTS
```

### 2. Создайте виртуальное окружение Python (рекомендуется)

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Установите зависимости Backend

```bash
cd backend
pip install -r requirements.txt
cd ..
```

### 4. Установите зависимости Frontend

```bash
cd frontend
npm install
cd ..
```

### 5. Создайте файл .env

```bash
cp .env.example .env
```

Отредактируйте `.env` если необходимо изменить порты или другие параметры.

## Запуск приложения

### Способ 1: Автоматический запуск (рекомендуется)

**Windows:**
```bash
python start.py
```

**macOS/Linux:**
```bash
python3 start.py
```

Скрипт автоматически:
- Проверит все зависимости
- Проверит свободные порты
- Запустит Backend API
- Запустит Frontend

### Способ 2: Запуск компонентов отдельно

**Терминал 1 - Backend:**
```bash
cd backend
python run.py
```

**Терминал 2 - Frontend:**
```bash
cd frontend
npm run dev
```

### Способ 3: Только Backend (для разработки)

```bash
python start.py --backend-only
```

### Способ 4: Только Frontend

```bash
python start.py --frontend-only
```

## Доступ к приложению

После успешного запуска:

- **Web Interface**: http://127.0.0.1:3000
- **API Documentation**: http://127.0.0.1:8000/docs
- **API Health Check**: http://127.0.0.1:8000/health

## Остановка приложения

Нажмите `Ctrl+C` в терминале где работает `start.py`. Приложение корректно завершит все процессы.

## Решение проблем

### Ошибка: "Port X is already in use"

Порт уже занят другим приложением. Закройте приложение которое его использует или измените PORT в `.env`.

### Ошибка: "npm not found"

Node.js не установлен. Скачайте и установите с https://nodejs.org/

### Ошибка: "python not found"

Python не установлен или не добавлен в PATH. Скачайте с https://www.python.org/

### Ошибка: "ModuleNotFoundError"

Зависимости не установлены:
```bash
cd backend
pip install -r requirements.txt
```

### Frontend не загружается

Убедитесь что Node.js установлен и Backend запущен на порту 8000.

## Разработка

### Структура проекта

```
backend/
  ├── app/
  │   ├── api/         # API routes
  │   ├── models/      # Database models
  │   ├── services/    # Business logic
  │   ├── db/          # Database setup
  │   ├── utils/       # Utilities
  │   ├── config.py    # Configuration
  │   └── main.py      # FastAPI app
  ├── requirements.txt
  └── run.py

frontend/
  ├── app/             # Next.js pages
  ├── components/      # React components
  ├── lib/             # Utilities
  ├── styles/          # CSS files
  └── package.json
```

### Добавление новой функции

1. Создайте API endpoint в `backend/app/api/routes.py`
2. Реализуйте бизнес-логику в `backend/app/services/`
3. Создайте компонент в `frontend/components/`
4. Используйте компонент на нужной странице

### Запуск тестов

```bash
# Backend
cd backend
pytest

# Frontend
cd frontend
npm test
```

## Дополнительно

Для получения дополнительной информации см.:
- [README.md](../README.md) - Основная документация
- [API.md](./API.md) - API документация
- Встроенная документация: http://127.0.0.1:8000/docs

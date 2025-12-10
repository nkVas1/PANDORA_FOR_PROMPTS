# 🔧 Troubleshooting Guide - PANDORA for PROMPTS

Решения для часто встречающихся проблем.

## 🚀 Проблемы с запуском

### Проблема: "python: command not found"

**Причина**: Python не установлен или не в PATH

**Решение:**
```bash
# Проверьте установку
python --version
# или
python3 --version

# Установите Python с https://python.org
# При установке отметьте "Add Python to PATH"

# На Windows переустановите с опцией:
python-3.9.0-amd64.exe /InstallAllUsers=1 /PrependPath=1
```

---

### Проблема: ".env file not found"

**Причина**: Отсутствует конфигурационный файл

**Решение:**
```bash
# Скопируйте пример
cp .env.example .env

# Отредактируйте необходимые значения
# Минимум требуется BOT_TOKEN (для Telegram функций)
BOT_TOKEN=your_token_here
API_HOST=127.0.0.1
API_PORT=8000
FRONTEND_PORT=3000
```

---

### Проблема: "Port 8000 already in use"

**Причина**: Порт уже занят другим процессом

**Решение:**
```powershell
# На Windows
Get-NetTCPConnection -LocalPort 8000
# или
netstat -ano | findstr :8000

# Получите PID и завершите процесс
taskkill /PID [PID] /F

# Или измените порт в .env
API_PORT=8001
```

```bash
# На macOS/Linux
lsof -i :8000
kill -9 [PID]
```

---

### Проблема: "Module not found"

**Причина**: Зависимости не установлены

**Решение:**
```bash
# Backend
cd backend
pip install -r requirements.txt

# Frontend
cd frontend
npm install
```

---

## 🐍 Проблемы с Python/Backend

### Проблема: "ModuleNotFoundError: No module named 'fastapi'"

**Решение:**
```bash
cd backend
pip install fastapi uvicorn sqlalchemy pydantic
# или
pip install -r requirements.txt
```

---

### Проблема: "sqlite3.OperationalError: unable to open database file"

**Причина**: Нет доступа к папке data/

**Решение:**
```bash
# Создайте папку data
mkdir data

# Проверьте права доступа
chmod 755 data  # Linux/macOS
# На Windows должны быть права по умолчанию

# Удалите старую БД и создайте новую
rm data/pandora.db  # Linux/macOS
del data\pandora.db  # Windows
python start.py
```

---

### Проблема: "ImportError: cannot import name 'FastAPI'"

**Причина**: Python использует неправильный interpreter

**Решение:**
```bash
# Проверьте какой Python используется
which python
# или
where python  # Windows

# Убедитесь что используется правильный environment
# Если используете venv:
source backend/.venv/bin/activate  # Linux/macOS
backend\.venv\Scripts\activate  # Windows

# Переустановите зависимости
pip install -r requirements.txt
```

---

### Проблема: "CORS Error" в браузере

**Причина**: Frontend и Backend на разных портах и CORS не настроен

**Решение:**
```python
# backend/app/main.py
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:3000", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## ⚛️ Проблемы с Frontend/Next.js

### Проблема: "npm: command not found"

**Причина**: Node.js не установлен

**Решение:**
```bash
# Установите Node.js с https://nodejs.org/
# Рекомендуется LTS версия (18+)

# Проверьте установку
node --version
npm --version

# На Windows может потребоваться перезагрузка
```

---

### Проблема: "next: command not found"

**Причина**: Next.js не установлен в проекте

**Решение:**
```bash
cd frontend
npm install
npm run dev
```

---

### Проблема: "Unexpected token" в TypeScript

**Причина**: TypeScript конфиг неправильный или зависимости не установлены

**Решение:**
```bash
cd frontend

# Переустановите зависимости
rm -rf node_modules package-lock.json
npm install

# Проверьте tsconfig.json
cat tsconfig.json

# Очистите кэш Next.js
rm -rf .next
npm run dev
```

---

### Проблема: "Tailwind CSS not working"

**Причина**: Tailwind CSS не сконфигурирован правильно

**Решение:**
```bash
# Проверьте tailwind.config.ts
cd frontend
cat tailwind.config.ts

# Убедитесь что содержит:
module.exports = {
  content: ['./app/**/*.{js,ts,jsx,tsx}'],
  // ...
}

# Переустановите Tailwind
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
```

---

### Проблема: "Cannot find module from @/lib"

**Причина**: Path aliases неправильно настроены

**Решение:**
```json
// frontend/tsconfig.json
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@/*": ["./*"]
    }
  }
}
```

---

## 🌐 Проблемы с сетью

### Проблема: "Cannot connect to http://127.0.0.1:8000"

**Причина**: Backend не запущен

**Решение:**
```bash
# Убедитесь что backend запущен
python start.py

# Или вручную
cd backend
python run.py

# Проверьте что сервер слушает порт 8000
# Windows:
netstat -ano | findstr :8000
# Linux/macOS:
lsof -i :8000
```

---

### Проблема: "GET http://127.0.0.1:8000/api/prompts 404"

**Причина**: API endpoint неверно настроен

**Решение:**
```bash
# Откройте http://127.0.0.1:8000/docs
# Проверьте какие endpoints доступны

# Убедитесь что backend/app/api/routes.py содержит:
@router.get("/api/prompts")
def get_prompts():
    # ...
```

---

### Проблема: "Connection refused" при импорте данных

**Причина**: Backend не запущен перед импортом

**Решение:**
```bash
# Запустите backend в одном терминале
python start.py

# Или в отдельных терминалах:

# Terminal 1
cd backend
python run.py

# Terminal 2
cd frontend
npm run dev

# Terminal 3
python import_data.py
```

---

## 💾 Проблемы с базой данных

### Проблема: "Database is locked"

**Причина**: БД открыта двумя процессами одновременно

**Решение:**
```bash
# Закройте все процессы backend
# Затем удалите БД
rm data/pandora.db

# Запустите заново
python start.py
```

---

### Проблема: "Table already exists"

**Причина**: Миграция уже была выполнена

**Решение:**
```bash
# Просто перезапустите приложение
# Таблицы создаются автоматически только если их нет

# Если проблема повторяется:
rm data/pandora.db
python start.py
```

---

### Проблема: "Foreign key constraint failed"

**Причина**: Нарушено ограничение целостности данных

**Решение:**
```python
# backend/app/db/__init__.py
# Включите поддержку foreign keys для SQLite

from sqlalchemy import event
from sqlalchemy.pool import Pool

@event.listens_for(Pool, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()
```

---

## 📊 Проблемы с импортом данных

### Проблема: "JSON decode error"

**Причина**: JSON файл имеет неверный формат

**Решение:**
```bash
# Проверьте JSON синтаксис
# Используйте https://jsonlint.com/

# Правильный формат:
{
  "prompts": [
    {
      "title": "Prompt Title",
      "content": "Prompt content",
      "category": "development",
      "tags": ["tag1", "tag2"]
    }
  ]
}
```

---

### Проблема: "File not found during import"

**Причина**: Путь к файлу неверный

**Решение:**
```bash
# Проверьте что файл существует
ls data/import/

# Используйте абсолютный путь
python import_data.py /full/path/to/file.json

# Или поместите файл в папку data/import/
cd data/import
# ... поместите JSON файлы сюда
cd ../..
python import_data.py
```

---

## 🎨 Проблемы с UI

### Проблема: "Dark theme не применяется"

**Причина**: Tailwind CSS dark mode неправильно настроен

**Решение:**
```js
// frontend/tailwind.config.ts
module.exports = {
  darkMode: 'class',  // или 'media'
  theme: {
    extend: {
      colors: {
        dark: {
          50: '#f9fafb',
          100: '#f3f4f6',
          // ...
        }
      }
    }
  }
}
```

```jsx
// frontend/app/layout.tsx
<html className="dark">
  {/* ... */}
</html>
```

---

### Проблема: "Компоненты не отображаются"

**Причина**: CSS не загружен или 'use client' отсутствует

**Решение:**
```tsx
// frontend/components/Button.tsx
'use client'  // Добавьте эту строку

export function Button({ children }: { children: React.ReactNode }) {
  return (
    <button className="px-4 py-2 bg-blue-600 text-white rounded">
      {children}
    </button>
  )
}
```

---

## 🏗️ Проблемы с сборкой exe

### Проблема: "PyInstaller not found"

**Причина**: PyInstaller не установлен

**Решение:**
```bash
pip install pyinstaller
python build.py
```

---

### Проблема: "Exe file not created"

**Причина**: Ошибка в процессе сборки

**Решение:**
```bash
# Проверьте логи
python build.py

# Убедитесь что все зависимости установлены
pip install -r backend/requirements.txt

# Пересоберите
python build.py --clean

# Или соберите вручную
pyinstaller --onefile backend/run.py --name PANDORA
```

---

## 🔐 Проблемы безопасности

### Проблема: ".env файл виден в Git"

**Решение:**
```bash
# Добавьте в .gitignore
echo ".env" >> .gitignore

# Удалите из Git history (если случайно добавлен)
git rm --cached .env
git commit -m "Remove .env from tracking"
```

---

### Проблема: "Потеря данных при переустановке"

**Решение:**
```bash
# Создайте резервную копию БД перед обновлением
cp data/pandora.db data/pandora.db.backup

# После обновления можно восстановить
cp data/pandora.db.backup data/pandora.db
```

---

## 📝 Логирование и отладка

### Включить verbose логирование

```python
# backend/app/main.py
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@app.get("/api/prompts")
def get_prompts():
    logger.debug("Fetching prompts")
    # ...
```

```javascript
// frontend/lib/api.ts
const api = axios.create({
  baseURL: 'http://127.0.0.1:8000/api'
})

api.interceptors.response.use(
  response => {
    console.log('API Response:', response)
    return response
  },
  error => {
    console.error('API Error:', error)
    return Promise.reject(error)
  }
)
```

---

## ✅ Общая диагностика

Если ничего не помогло, выполните:

```bash
# 1. Очистьте всё
rm -rf backend/.venv
rm -rf frontend/node_modules
rm -rf data/
rm -rf backend/__pycache__
rm -rf frontend/.next

# 2. Переустановитесь
python -m venv backend/.venv
cd backend
source .venv/bin/activate  # или Scripts\activate
pip install -r requirements.txt

cd ../frontend
npm install

# 3. Запустите заново
cd ..
python start.py
```

---

## 🆘 Если всё ещё не работает

1. **Проверьте** логи в терминале
2. **Скопируйте** полный текст ошибки
3. **Откройте** [Issue на GitHub](https://github.com/yourusername/PANDORA_FOR_PROMPTS/issues)
4. **Включите**:
   - Операционная система (Windows/macOS/Linux)
   - Версия Python (`python --version`)
   - Версия Node.js (`node --version`)
   - Полный текст ошибки
   - Шаги для воспроизведения

---

## 📚 Дополнительные ресурсы

- [Python Troubleshooting](https://docs.python.org/3/faq/general.html)
- [FastAPI Debugging](https://fastapi.tiangolo.com/deployment/concepts/)
- [Next.js Troubleshooting](https://nextjs.org/docs/basic-features/pages#server-side-rendering-with-getserversideprops)
- [SQLAlchemy Common Issues](https://docs.sqlalchemy.org/en/20/faq/)
- [Tailwind CSS Troubleshooting](https://tailwindcss.com/docs/troubleshooting)

---

**Если нашли ошибку в этом гайде, обновите документацию!** 🙏

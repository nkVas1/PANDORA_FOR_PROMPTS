# PANDORA API Документация

## Базовый URL

```
http://127.0.0.1:8000/api
```

## Аутентификация

На данный момент API не требует аутентификации для локального использования.

## Формат ответов

Все ответы возвращаются в формате JSON.

### Успешный ответ (200)

```json
{
  "id": 1,
  "title": "Пример промпта",
  "content": "Текст промпта...",
  "category": "development",
  "tags": [],
  "created_at": "2024-12-07T10:00:00",
  "updated_at": "2024-12-07T10:00:00"
}
```

### Ошибка (400, 404, 500)

```json
{
  "detail": "Описание ошибки"
}
```

## Endpoints

### Промпты

#### Создать промпт
```http
POST /api/prompts
Content-Type: application/json

{
  "title": "Название промпта",
  "content": "Текст промпта",
  "description": "Описание (опционально)",
  "category": "development",
  "version": "1.0",
  "tag_ids": [1, 2, 3]
}
```

#### Получить все промпты
```http
GET /api/prompts?skip=0&limit=100
```

#### Поиск промптов
```http
GET /api/prompts/search?q=python&category=development&tags=tutorial&skip=0&limit=100
```

Parameters:
- `q` (string, required) - Поисковый запрос
- `category` (string, optional) - Категория
- `tags` (list, optional) - Список тегов
- `skip` (int) - Количество пропускаемых результатов
- `limit` (int) - Количество результатов

#### Получить промпт по ID
```http
GET /api/prompts/1
```

#### Обновить промпт
```http
PUT /api/prompts/1
Content-Type: application/json

{
  "title": "Новое название",
  "content": "Новый текст",
  "category": "development"
}
```

#### Удалить промпт
```http
DELETE /api/prompts/1
```

#### Увеличить счетчик использования
```http
POST /api/prompts/1/use
```

#### Автотегирование промпта
```http
POST /api/prompts/1/auto-tag
```

Response:
```json
{
  "prompt_id": 1,
  "suggested_tags": [
    {"name": "python", "confidence": 0.95},
    {"name": "tutorial", "confidence": 0.87}
  ],
  "category_suggestion": "development",
  "category_confidence": 0.92
}
```

### Теги

#### Получить все теги
```http
GET /api/tags
```

#### Создать тег
```http
POST /api/tags
Content-Type: application/json

{
  "name": "python",
  "color": "#3B82F6"
}
```

#### Удалить тег
```http
DELETE /api/tags/1
```

### Проекты

#### Создать проект
```http
POST /api/projects
Content-Type: application/json

{
  "name": "Мой проект",
  "description": "Описание проекта",
  "status": "active"
}
```

#### Получить все проекты
```http
GET /api/projects
```

#### Получить проект
```http
GET /api/projects/1
```

#### Обновить проект
```http
PUT /api/projects/1
Content-Type: application/json

{
  "name": "Новое название",
  "status": "completed"
}
```

#### Удалить проект
```http
DELETE /api/projects/1
```

#### Добавить запись процесса
```http
POST /api/projects/1/process?entry=Начал+разработку
```

#### Добавить задачу
```http
POST /api/projects/1/tasks
Content-Type: application/json

{
  "title": "Реализовать функцию X",
  "description": "Описание задачи",
  "status": "todo",
  "priority": "high",
  "due_date": "2024-12-31T23:59:59"
}
```

#### Обновить задачу
```http
PUT /api/tasks/1
Content-Type: application/json

{
  "status": "done",
  "priority": "medium"
}
```

### Импорт

#### Импортировать из JSON файла
```http
POST /api/import/json
Content-Type: multipart/form-data

file: <binary file>
source_name: awesome-prompts
```

#### Массовый импорт
```http
POST /api/import/batch
Content-Type: application/json

{
  "import_source": "my-prompts",
  "prompts": [
    {
      "title": "Промпт 1",
      "content": "Текст 1",
      "category": "development"
    },
    {
      "title": "Промпт 2",
      "content": "Текст 2",
      "category": "writing"
    }
  ]
}
```

### Статистика

#### Получить статистику
```http
GET /api/stats
```

Response:
```json
{
  "total_prompts": 150,
  "total_tags": 45,
  "total_projects": 12,
  "top_prompts": [
    {
      "id": 1,
      "title": "Популярный промпт",
      "usage_count": 42
    }
  ]
}
```

## Коды ошибок

| Код | Описание |
|-----|----------|
| 200 | OK - Успешно |
| 201 | Created - Создано |
| 400 | Bad Request - Неверный запрос |
| 404 | Not Found - Не найдено |
| 500 | Internal Server Error - Внутренняя ошибка сервера |

## Rate Limiting

На данный момент rate limiting не реализован.

## Примеры использования

### cURL

```bash
# Создать промпт
curl -X POST http://127.0.0.1:8000/api/prompts \
  -H "Content-Type: application/json" \
  -d '{
    "title": "My Prompt",
    "content": "Prompt content",
    "category": "development"
  }'

# Поиск
curl "http://127.0.0.1:8000/api/prompts/search?q=python"

# Получить все промпты
curl http://127.0.0.1:8000/api/prompts
```

### Python (requests)

```python
import requests

api_url = "http://127.0.0.1:8000/api"

# Создать промпт
response = requests.post(
    f"{api_url}/prompts",
    json={
        "title": "My Prompt",
        "content": "Prompt content",
        "category": "development"
    }
)
prompt = response.json()

# Поиск
response = requests.get(f"{api_url}/prompts/search", params={"q": "python"})
results = response.json()

# Получить статистику
response = requests.get(f"{api_url}/stats")
stats = response.json()
```

### JavaScript (fetch)

```javascript
const apiUrl = "http://127.0.0.1:8000/api";

// Создать промпт
const response = await fetch(`${apiUrl}/prompts`, {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    title: "My Prompt",
    content: "Prompt content",
    category: "development"
  })
});
const prompt = await response.json();

// Поиск
const searchResponse = await fetch(
  `${apiUrl}/prompts/search?q=python`
);
const results = await searchResponse.json();
```

## Интерактивная документация

Полная интерактивная документация доступна по адресу:
```
http://127.0.0.1:8000/docs
```

Это swagger UI, где можно тестировать все endpoints прямо из браузера.

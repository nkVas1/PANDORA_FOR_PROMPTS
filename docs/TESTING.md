# Testing Guide - PANDORA

## Запуск тестов

### Все тесты
```bash
pytest
```

### Тесты с покрытием кода
```bash
pytest --cov=backend/app --cov-report=html
```

### Конкретный тест или модуль
```bash
pytest backend/tests/test_api/test_prompts.py
pytest backend/tests/test_api/test_prompts.py::TestPromptsAPI::test_create_prompt
```

### Тесты по маркерам
```bash
pytest -m api          # Только API тесты
pytest -m "not slow"   # Исключить медленные тесты
```

### С verbose выводом
```bash
pytest -v
pytest -vv             # Очень подробный вывод
```

## Структура тестов

```
backend/tests/
├── conftest.py                 # Fixtures и конфигурация pytest
├── test_api/
│   ├── __init__.py
│   ├── test_prompts.py        # Тесты для /api/prompts
│   ├── test_projects.py       # Тесты для /api/projects
│   └── test_tags.py           # Тесты для /api/tags
├── test_services/
│   ├── __init__.py
│   └── test_auto_tagging.py   # Тесты сервиса автотегирования
└── test_models/
    ├── __init__.py
    └── test_prompt_model.py   # Тесты моделей БД
```

## Написание новых тестов

### Пример: Простой unit-тест

```python
def test_create_prompt(client, sample_prompt_data):
    """Тест создания промпта"""
    response = client.post("/api/prompts", json=sample_prompt_data)
    
    assert response.status_code == 200
    assert response.json()["title"] == sample_prompt_data["title"]
```

### Пример: Тест с подготовкой данных

```python
def test_delete_prompt(client, sample_prompt_data):
    """Тест удаления промпта"""
    # Setup: Создаём промпт
    create_response = client.post("/api/prompts", json=sample_prompt_data)
    prompt_id = create_response.json()["id"]
    
    # Test: Удаляем промпт
    response = client.delete(f"/api/prompts/{prompt_id}")
    assert response.status_code == 200
    
    # Verify: Проверяем что удалён
    get_response = client.get(f"/api/prompts/{prompt_id}")
    assert get_response.status_code == 404
```

### Пример: Параметризованные тесты

```python
@pytest.mark.parametrize("category", ["general", "technical", "creative"])
def test_create_prompt_different_categories(client, sample_prompt_data, category):
    """Тест создания промптов с разными категориями"""
    sample_prompt_data["category"] = category
    response = client.post("/api/prompts", json=sample_prompt_data)
    assert response.status_code == 200
    assert response.json()["category"] == category
```

## Fixtures (подготовка данных)

Основные fixtures в `conftest.py`:

- `client` - TestClient для API запросов
- `db_session` - Сессия БД для тестов
- `sample_prompt_data` - Пример данных промпта
- `sample_project_data` - Пример данных проекта

### Использование fixtures

```python
def test_something(client, db_session, sample_prompt_data):
    # client - готовый HTTP клиент
    # db_session - чистая БД для теста
    # sample_prompt_data - словарь с примером
    pass
```

## CI/CD Integration

Тесты автоматически запускаются при:

- Push в `main` или `develop` ветки
- Pull Request в `main` или `develop`
- Вручную через GitHub Actions

Смотрите `.github/workflows/tests.yml` для деталей.

## Целевое покрытие кода

- **Критично**: 80%+ для API endpoints
- **Желательно**: 60%+ для сервисов
- **Информативно**: 50%+ для моделей

## Pre-commit hooks

Установить:
```bash
pip install pre-commit
pre-commit install
```

Будет автоматически проверять:
- Форматирование (black)
- Liniting (flake8)
- Type checking (mypy)
- Большие файлы
- JSON/YAML синтаксис

## Решение проблем

### Тесты не находят модули
```bash
# Убедитесь что находитесь в корне проекта
cd /path/to/PANDORA_FOR_PROMPTS
pytest
```

### "ModuleNotFoundError: No module named 'backend'"
```bash
# Установите зависимости
pip install -r requirements.txt

# Или запустите из корня проекта
python -m pytest
```

### Тесты БД падают с sqlite ошибкой
```bash
# Очистите кэш pytest
pytest --cache-clear
```

## Лучшие практики

1. ✅ **DRY** - Используйте fixtures для повторяемых данных
2. ✅ **Изоляция** - Каждый тест должен быть независимым
3. ✅ **Наименование** - `test_action_outcome` (test_create_prompt_success)
4. ✅ **AAA паттерн** - Arrange (подготовка), Act (действие), Assert (проверка)
5. ✅ **Один assert** - Тест должен проверять одно правило (если возможно)

## Пример: Правильно структурированный тест

```python
def test_update_nonexistent_prompt(client):
    """
    Given: Несуществующий ID промпта
    When: Пытаемся обновить промпт
    Then: Получаем 404 ошибку
    """
    # Arrange
    update_data = {"title": "New title", "content": "New content"}
    
    # Act
    response = client.put("/api/prompts/99999", json=update_data)
    
    # Assert
    assert response.status_code == 404
```

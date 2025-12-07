# GitHub Actions CI/CD Configuration

## Описание

Этот файл содержит конфигурацию для автоматического тестирования и сборки приложения при каждом push в репозиторий.

## Как использовать

1. Создайте папку `.github/workflows` в корне репозитория
2. Скопируйте файлы workflows
3. Commitьте и pushьте изменения

## Доступные workflows

### 1. Tests (tests.yml)

Запускается при каждом push и pull request.
Проверяет:

- Синтаксис Python кода
- Зависимости Python
- Синтаксис JavaScript/TypeScript
- Зависимости npm

### 2. Build (build.yml)

Запускается при создании нового release.
Собирает:

- exe файл для Windows
- Архив с исходным кодом
- Загружает артефакты на release

### 3. Deploy (deploy.yml)

Опционально: развертывание на сервер (при наличии).

## Настройка

Для полной функциональности добавьте секреты в GitHub:

Settings > Secrets and variables > Actions

Необходимые секреты:

- `PYTHON_VERSION` - версия Python (по умолчанию 3.9)
- `NODE_VERSION` - версия Node.js (по умолчанию 18)

Опциональные секреты для деплоя:

- `DEPLOY_HOST` - хост для развертывания
- `DEPLOY_USER` - пользователь для ssh
- `DEPLOY_KEY` - приватный SSH ключ

## Примеры файлов

Создайте файл `.github/workflows/tests.yml`:

```yaml
name: Tests

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

jobs:
  backend-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.9'
      - run: pip install -r backend/requirements.txt
      - run: cd backend && pytest

  frontend-lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
      - run: cd frontend && npm install
      - run: cd frontend && npm run lint
```

Создайте файл `.github/workflows/build.yml`:

```yaml
name: Build

on:
  release:
    types: [created]

jobs:
  build-windows:
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.9'
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
      - run: pip install -r backend/requirements.txt
      - run: cd frontend && npm install
      - run: python build.py
      - uses: softprops/action-gh-release@v1
        with:
          files: dist/PANDORA/**/*
```

## Статус

Добавьте badge в README:

```markdown
[![Tests](https://github.com/yourusername/PANDORA_FOR_PROMPTS/actions/workflows/tests.yml/badge.svg)](https://github.com/yourusername/PANDORA_FOR_PROMPTS/actions)
```

## Поиск и исправление ошибок

1. Откройте вкладку "Actions" в GitHub
2. Найдите failed workflow
3. Кликните на него для просмотра логов
4. Исправьте ошибки и commitьте

## Дополнительно

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Workflow Syntax](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions)

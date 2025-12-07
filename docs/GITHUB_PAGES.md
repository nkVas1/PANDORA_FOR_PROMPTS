# GitHub Pages - Демо сайт PANDORA

Инструкции по развертыванию демо-сайта с документацией на GitHub Pages.

## 🌐 Как это работает

GitHub Pages будет хостить:
1. Документацию проекта
2. API документацию
3. Демо интерфейс (статический)

## 🔧 Настройка GitHub Pages

### Шаг 1: Создайте папку docs (если её нет)

```bash
mkdir -p docs/.github/pages
```

### Шаг 2: Создайте файл _config.yml

Для Jekyll:

```yaml
# _config.yml
title: PANDORA for PROMPTS
description: Professional local prompt management system
theme: jekyll-theme-midnight
plugins:
  - jekyll-sitemap
markdown: kramdown
```

### Шаг 3: Включите GitHub Pages

В GitHub:
1. Settings → Pages
2. Build and deployment
3. Source: Deploy from a branch
4. Branch: main, folder: /docs
5. Нажмите Save

### Шаг 4: Дождитесь сборки

GitHub автоматически соберет сайт. Ссылка:
`https://yourusername.github.io/PANDORA_FOR_PROMPTS/`

## 📄 Структура документации

```
docs/
├── index.md                 # Главная страница
├── API.md                   # API документация
├── SETUP.md                 # Установка
├── USER_GUIDE.md            # Пользовательский гайд
├── DEVELOPMENT.md           # Для разработчиков
├── _config.yml              # Jekyll конфиг
└── assets/
    └── images/              # Скриншоты (опционально)
```

## 📝 Пример главной страницы (index.md)

```markdown
---
layout: default
---

# PANDORA for PROMPTS

Professional local prompt management system with auto-tagging.

## Features

- 📝 Organize prompts with tags and categories
- 🏷️ Auto-tagging with AI analysis
- 📊 Statistics and analytics
- 💾 Local storage (SQLite)
- 🎨 Dark theme UI

## Quick Links

- [Quick Start](QUICK_START.md)
- [API Documentation](API.md)
- [Setup Guide](SETUP.md)
- [User Guide](USER_GUIDE.md)
- [Developer Guide](DEVELOPMENT.md)

## Getting Started

```bash
python start.py
```

Visit: http://127.0.0.1:3000

## GitHub

- [Repository](https://github.com/yourusername/PANDORA_FOR_PROMPTS)
- [Issues](https://github.com/yourusername/PANDORA_FOR_PROMPTS/issues)
- [Releases](https://github.com/yourusername/PANDORA_FOR_PROMPTS/releases)

---

Built with ❤️ using FastAPI + Next.js
```

## 🎨 Выбор темы Jekyll

### Встроенные темы:

```yaml
# _config.yml
theme: jekyll-theme-midnight      # Темная, подходит для проекта
# OR
theme: jekyll-theme-minimal       # Минималистичная
# OR
theme: jekyll-theme-slate         # Спокойная темная
```

### Или используйте кастомную тему:

```yaml
remote_theme: pages-themes/midnight@v0.2.0
```

## 🚀 GitHub Actions для Pages

Создайте `.github/workflows/pages.yml`:

```yaml
name: Build and Deploy GitHub Pages

on:
  push:
    branches:
      - main
  workflow_dispatch:

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Ruby
        uses: ruby/setup-ruby@v1
        with:
          ruby-version: 3.1
          bundler-cache: true
          working-directory: ./docs
      
      - name: Build with Jekyll
        run: bundle exec jekyll build -d ./docs/_site
        working-directory: ./docs
      
      - name: Deploy to GitHub Pages
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./docs/_site
```

## 📊 Добавляем скриншоты (опционально)

### Шаг 1: Сохраните скриншоты

```
docs/assets/images/
├── dashboard.png
├── prompt-list.png
├── auto-tagging.png
└── dark-theme.png
```

### Шаг 2: Добавьте в документацию

```markdown
## Dashboard

![PANDORA Dashboard](/assets/images/dashboard.png)

## Prompt List

![Prompt Management](/assets/images/prompt-list.png)
```

## 🔍 SEO оптимизация

Добавьте в _config.yml:

```yaml
title: PANDORA for PROMPTS
description: Professional local prompt management system
author: Your Name
url: https://yourusername.github.io/PANDORA_FOR_PROMPTS
repository: yourusername/PANDORA_FOR_PROMPTS
social:
  github: yourusername
keywords:
  - prompts
  - prompt management
  - ai
  - local storage
  - tagging
```

## 🎯 Sitemap

Автоматически генерируется с плагином `jekyll-sitemap`.

Доступен по адресу:
`https://yourusername.github.io/PANDORA_FOR_PROMPTS/sitemap.xml`

## 📱 Адаптивная верстка

Все встроенные темы Jekyll адаптивны.

Проверьте на мобильных устройствах:
- iPhone / iPad
- Android
- Планшеты

## 🔐 Конфиденциальность

GitHub Pages публичны! Не добавляйте:
- Приватные ключи
- Пароли
- Персональную информацию
- Лицензионные ключи

## ✅ Чек-лист

- [ ] Включена GitHub Pages в Settings
- [ ] Выбрана правильная ветка (main) и папка (docs)
- [ ] Создан _config.yml
- [ ] Создан index.md
- [ ] Тема Jekyll выбрана
- [ ] GitHub Actions workflow создан (опционально)
- [ ] Сайт собирается успешно
- [ ] Ссылка работает в браузере

## 📋 URL структура

```
/                               # Главная
/API.md                         # API документация
/SETUP.md                       # Setup гайд
/USER_GUIDE.md                  # User guide
/DEVELOPMENT.md                 # Dev guide
/assets/images/screenshot.png   # Скриншоты
```

## 🎨 Кастомизация стилей

Создайте `docs/assets/css/style.scss`:

```scss
---
---

@import "{{ site.theme }}";

body {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

a {
  color: #00d4ff;
  &:hover {
    color: #00f0ff;
  }
}

code {
  background-color: #1e1e1e;
  color: #00ff00;
}
```

## 🔄 Обновление документации

Просто отредактируйте файлы в папке `docs/`:

```bash
git add docs/
git commit -m "Обновление документации / Update documentation"
git push origin main
```

GitHub автоматически пересоберет сайт через 2-3 минуты.

## 📚 Документация Jekyll

- [Jekyll Documentation](https://jekyllrb.com/docs/)
- [GitHub Pages with Jekyll](https://docs.github.com/en/pages/setting-up-a-github-pages-site-with-jekyll)
- [Jekyll Themes](https://pages.github.com/themes/)

## 🎯 Аналитика

Добавьте Google Analytics в _config.yml:

```yaml
google_analytics: UA-XXXXXXXXX-X
```

(Для встроенной темы midnight может потребоваться кастомная реализация)

## 🚀 Заключение

GitHub Pages = бесплатный хостинг для документации вашего проекта!

Начните с:
1. Создайте файл `docs/index.md`
2. Включите GitHub Pages в Settings
3. Готово!

Сайт будет доступен по адресу:
`https://yourusername.github.io/PANDORA_FOR_PROMPTS/`

% PANDORA v2.0 - Update index.html Guide
% Пошаговое руководство по обновлению главного HTML файла
% 2024-2025

# 🔄 PANDORA v2.0 - Update index.html Guide

## 📋 Инструкции по обновлению главного HTML

Этот гайд поможет вам обновить существующий `index.html` на новую дизайн-систему v2.0.

---

## Шаг 1️⃣: Head секция

### Заменить старые стили на новые

**БЫЛО:**
```html
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PANDORA</title>
    
    <!-- Старые CSS -->
    <link rel="stylesheet" href="css/style.css">
    <link rel="stylesheet" href="css/colors.css">
    <link rel="stylesheet" href="css/responsive.css">
</head>
```

**СТАЛО:**
```html
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="PANDORA - Профессиональный менеджер промптов">
    <meta name="theme-color" content="#6366F1">
    <title>PANDORA v2.0 - Менеджер промптов</title>
    
    <!-- Preconnect для оптимизации -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    
    <!-- Google Fonts (НОВОЕ - необходимо!) -->
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
    
    <!-- Новая дизайн-система (это импортирует всё!) -->
    <link rel="stylesheet" href="css/styles.css">
    
    <!-- Favicon -->
    <link rel="icon" type="image/svg+xml" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='75' font-size='75'>P</text></svg>">
</head>
```

---

## Шаг 2️⃣: Body структура

### Обновить основной layout

**БЫЛО:**
```html
<body>
    <div class="app">
        <header class="header">...</header>
        <nav class="nav">...</nav>
        <main class="main-content">
            ...
        </main>
        <footer class="footer">...</footer>
    </div>
    
    <script src="js/old.js"></script>
</body>
```

**СТАЛО:**
```html
<body>
    <div id="app" class="app-layout">
        <!-- Sidebar слева -->
        <aside class="sidebar-wrapper">
            <!-- Навигация здесь -->
        </aside>
        
        <!-- Основной контент справа -->
        <div class="main-content">
            <!-- Navbar вверху -->
            <nav class="navbar">
                ...
            </nav>
            
            <!-- Основное содержимое -->
            <main class="flex-1 overflow-y-auto">
                <div class="content-wrapper">
                    <!-- Ваш контент здесь -->
                </div>
            </main>
        </div>
    </div>
    
    <!-- НОВЫЙ JavaScript (в конец body) -->
    <script src="js/app.js"></script>
</body>
```

---

## Шаг 3️⃣: Обновить Navbar

### Навигационная панель

**БЫЛО:**
```html
<header class="header">
    <h1>PANDORA</h1>
    <nav class="nav-items">
        <a href="/">Home</a>
        <a href="/prompts">Prompts</a>
    </nav>
    <button class="theme-toggle">🌙</button>
</header>
```

**СТАЛО:**
```html
<nav class="navbar">
    <div class="flex items-center gap-4">
        <!-- Кнопка меню на мобильных -->
        <button data-sidebar-toggle class="btn btn-icon btn-ghost" style="display: none;">
            ☰
        </button>
    </div>
    
    <!-- Центральная навигация -->
    <div class="navbar-nav">
        <!-- Добавьте нужные ссылки -->
    </div>
    
    <!-- Правая часть -->
    <div class="navbar-end">
        <!-- Поиск -->
        <div class="search-bar" style="max-width: 300px;">
            <span>🔍</span>
            <input type="text" placeholder="Быстрый поиск...">
        </div>
        
        <!-- Уведомления -->
        <button class="btn btn-icon btn-ghost">🔔</button>
        
        <!-- User menu -->
        <button class="btn btn-icon btn-ghost" data-menu-trigger="user-menu">👤</button>
    </div>
</nav>
```

---

## Шаг 4️⃣: Обновить Sidebar

### Боковая навигация

**БЫЛО:**
```html
<nav class="sidebar">
    <div class="logo">PANDORA</div>
    <ul class="nav-menu">
        <li><a href="/">Dashboard</a></li>
        <li><a href="/prompts">Prompts</a></li>
    </ul>
</nav>
```

**СТАЛО:**
```html
<aside class="sidebar-wrapper">
    <!-- Логотип -->
    <div style="padding: var(--space-6) var(--space-4);">
        <a href="/" class="flex items-center gap-2 text-lg font-bold text-primary">
            <span style="font-size: 28px;">🎨</span>
            <span>PANDORA</span>
        </a>
    </div>
    
    <!-- Поиск -->
    <div style="padding: 0 var(--space-4) var(--space-4);">
        <div class="search-bar">
            <span>🔍</span>
            <input type="text" placeholder="Поиск...">
        </div>
    </div>
    
    <!-- Меню навигации -->
    <nav style="padding: 0 var(--space-4);">
        <div class="sidebar-section">
            <div class="sidebar-title">Основное</div>
            <a href="/" class="sidebar-item active">
                <span class="sidebar-icon">📊</span>
                <span>Панель управления</span>
            </a>
            <a href="/prompts" class="sidebar-item">
                <span class="sidebar-icon">💬</span>
                <span>Все промпты</span>
            </a>
        </div>
    </nav>
    
    <!-- Footer -->
    <div style="margin-top: auto; padding: var(--space-4); border-top: 1px solid var(--border-color);">
        <button class="btn btn-ghost" data-action="toggle-theme">🌙</button>
    </div>
</aside>
```

---

## Шаг 5️⃣: Обновить контент

### Основное содержимое страницы

**БЫЛО:**
```html
<main class="main-content">
    <div class="container">
        <h1 class="page-title">Welcome</h1>
        <p class="page-desc">Description</p>
        
        <button class="btn-primary">Click me</button>
        <div class="card">Content</div>
    </div>
</main>
```

**СТАЛО:**
```html
<main class="flex-1 overflow-y-auto">
    <div class="content-wrapper">
        <!-- Page Header -->
        <div class="page-header">
            <h1>Добро пожаловать в PANDORA v2.0</h1>
            <p class="page-description">Описание страницы</p>
        </div>
        
        <!-- Основной контент -->
        <div style="margin-bottom: var(--space-8);">
            <button class="btn btn-primary">
                Основная кнопка
            </button>
            <button class="btn btn-secondary">
                Вторичная кнопка
            </button>
        </div>
        
        <!-- Cards Grid -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3">
            <div class="card animate-slide-up">
                <div class="card-header">
                    <h3 class="card-title">Карточка 1</h3>
                </div>
                <div class="card-body">
                    Содержимое
                </div>
                <div class="card-footer">
                    <button class="btn btn-sm btn-primary">Действие</button>
                </div>
            </div>
        </div>
    </div>
</main>
```

---

## Шаг 6️⃣: Обновить формы

### Форма для создания/редактирования

**БЫЛО:**
```html
<form class="form">
    <input type="text" placeholder="Name" class="form-input">
    <input type="email" placeholder="Email" class="form-input">
    <textarea placeholder="Message" class="form-textarea"></textarea>
    <button type="submit" class="btn-primary">Submit</button>
</form>
```

**СТАЛО:**
```html
<form class="form-grid">
    <div class="input-group">
        <label for="name">Имя</label>
        <input 
            type="text" 
            id="name"
            class="input" 
            placeholder="Введите имя"
            required
        >
    </div>
    
    <div class="input-group">
        <label for="email">Email</label>
        <input 
            type="email" 
            id="email"
            class="input" 
            placeholder="your@email.com"
            required
        >
    </div>
    
    <div class="input-group" style="grid-column: 1 / -1;">
        <label for="message">Сообщение</label>
        <textarea 
            id="message"
            class="textarea" 
            placeholder="Ваше сообщение..."
            required
        ></textarea>
    </div>
    
    <div class="flex gap-4" style="grid-column: 1 / -1;">
        <button type="submit" class="btn btn-primary">Отправить</button>
        <button type="reset" class="btn btn-secondary">Очистить</button>
    </div>
</form>
```

---

## Шаг 7️⃣: Обновить список элементов

### Список с элементами

**БЫЛО:**
```html
<ul class="list">
    <li class="list-item">
        <span>Item 1</span>
        <button class="btn-small">View</button>
    </li>
    <li class="list-item">
        <span>Item 2</span>
        <button class="btn-small">View</button>
    </li>
</ul>
```

**СТАЛО:**
```html
<div class="list-container">
    <div class="list-item">
        <div style="flex: 1;">
            <h4 class="text-base font-semibold">Item 1</h4>
            <p class="text-sm text-secondary">Описание</p>
        </div>
        <div style="display: flex; gap: var(--space-2);">
            <span class="badge badge-secondary">Tag</span>
        </div>
        <button class="btn btn-sm btn-ghost">→</button>
    </div>
    
    <div class="list-item">
        <div style="flex: 1;">
            <h4 class="text-base font-semibold">Item 2</h4>
            <p class="text-sm text-secondary">Описание</p>
        </div>
        <div style="display: flex; gap: var(--space-2);">
            <span class="badge badge-success">Active</span>
        </div>
        <button class="btn btn-sm btn-ghost">→</button>
    </div>
</div>
```

---

## Шаг 8️⃣: Обновить модальные окна

### Modal примеры

**БЫЛО:**
```html
<div class="modal" style="display: none;">
    <div class="modal-content">
        <h2>Modal Title</h2>
        <p>Modal content</p>
        <button class="btn-primary" onclick="closeModal()">Close</button>
    </div>
</div>
```

**СТАЛО:**
```html
<!-- Trigger -->
<button class="btn btn-primary" data-modal-trigger="my-modal">
    Открыть диалог
</button>

<!-- Modal -->
<div class="modal-backdrop" data-modal-id="my-modal">
    <div class="modal">
        <div class="modal-header">
            <h2 class="modal-title">Заголовок диалога</h2>
            <button class="modal-close" data-modal-close>✕</button>
        </div>
        
        <div class="modal-body">
            <p>Содержимое модали</p>
        </div>
        
        <div class="modal-footer">
            <button class="btn btn-secondary" data-modal-close">
                Отмена
            </button>
            <button class="btn btn-primary">Действие</button>
        </div>
    </div>
</div>
```

---

## Шаг 9️⃣: Обновить CSS классы

### Таблица замен классов

| Было | Стало |
|------|--------|
| `.btn-primary` | `.btn btn-primary` |
| `.btn-secondary` | `.btn btn-secondary` |
| `.btn-small` | `.btn btn-sm` |
| `.card-style` | `.card` |
| `.form-input` | `.input` |
| `.form-textarea` | `.textarea` |
| `.badge-success` | `.badge badge-success` |
| `.grid-col-3` | `.grid-cols-3` |
| `.flex-center` | `.flex items-center justify-center` |
| `.mt-4` | `.mt-4` (осталось, добавьте новые если нужны) |

---

## Шаг 🔟: Добавить JavaScript

### Подключить новый JS в конец body

**БЫЛО:**
```html
<script src="js/old.js"></script>
<script src="js/another.js"></script>
```

**СТАЛО:**
```html
<!-- Удалить старые скрипты выше -->

<!-- Добавить новый JavaScript v2.0 -->
<script src="js/app.js"></script>

<!-- Опциональные инициализирующие скрипты -->
<script>
    // Пример: инициализировать счётчики на странице
    document.addEventListener('DOMContentLoaded', () => {
        // Ваш код здесь
    });
</script>
```

---

## ✅ Checkpoints после каждого шага

После обновления каждого раздела проверьте:

- [ ] **После Head**: Стили загружаются, нет ошибок в консоли
- [ ] **После Body**: Основной layout выглядит правильно
- [ ] **После Navbar**: Навигация видна, все кнопки работают
- [ ] **После Sidebar**: Боковое меню отображается правильно
- [ ] **После контента**: Текст, кнопки, карточки выглядят красиво
- [ ] **После форм**: Инпуты стилизованы, фокус работает
- [ ] **После списков**: Список выглядит правильно, элементы выравнены
- [ ] **После модалей**: Модали открываются/закрываются
- [ ] **После CSS**: Все старые классы заменены на новые
- [ ] **После JS**: Нет ошибок в консоли, всё работает интерактивно

---

## 🧪 Тестирование после обновления

### Функциональное тестирование
- [ ] Light режим работает
- [ ] Dark режим переключается (Ctrl+Shift+L)
- [ ] Все кнопки кликаются
- [ ] Все ссылки работают
- [ ] Модали открываются и закрываются
- [ ] Поиск работает

### Визуальное тестирование
- [ ] Все элементы отображаются правильно
- [ ] Цвета соответствуют палитре
- [ ] Текст читаемый
- [ ] Отступы выглядят правильно
- [ ] Анимации гладкие

### Адаптивное тестирование
- [ ] Desktop (1920x1080) - всё работает
- [ ] Tablet (1024x768) - адаптивность OK
- [ ] Mobile (375x667) - меню работает, всё видно

### Keyboard & Accessibility
- [ ] Tab навигация работает
- [ ] Enter на кнопках работает
- [ ] Escape закрывает модали
- [ ] Горячие клавиши работают (Ctrl+K, Ctrl+Shift+L)

---

## 🔍 Решение проблем

### Проблема: Стили не применяются
**Решение:**
1. Проверьте, что `css/styles.css` загружен (откройте Sources в DevTools)
2. Очистите кеш браузера (Ctrl+Shift+Del)
3. Проверьте консоль на ошибки загрузки (F12 → Console)

### Проблема: Шрифты выглядят неправильно
**Решение:**
1. Убедитесь, что добавили Google Fonts link в head
2. Дождитесь загрузки шрифтов (может быть задержка)
3. Проверьте, что CSS правильно ссылается на шрифты

### Проблема: Темой не переключается
**Решение:**
1. Проверьте, что `js/app.js` загружен (F12 → Sources)
2. Откройте консоль (F12 → Console) и введите: `App.theme.toggleTheme()`
3. Если работает в консоли, но не в UI - проверьте button с `data-action="toggle-theme"`

### Проблема: Модали не открываются
**Решение:**
1. Проверьте, что у modal-backdrop есть правильный `data-modal-id`
2. Проверьте, что у trigger button есть правильный `data-modal-trigger`
3. Проверьте консоль на ошибки JavaScript

---

## 📚 Полезные ссылки

- **DESIGN_SYSTEM.md** - полное описание компонентов
- **QUICK_START.md** - быстрый гайд
- **index-v2.html** - готовый пример
- **INTEGRATION_GUIDE.md** - детальная интеграция

---

## 🎉 Вы завершили обновление!

После выполнения всех шагов:

✅ Ваш `index.html` обновлен на v2.0
✅ Все стили работают с новой дизайн-системой
✅ Интерфейс выглядит современно и профессионально
✅ Поддержка light/dark режимов работает
✅ Все компоненты функциональны

**Следующий шаг:** Обновите остальные HTML страницы используя эти же инструкции.

---

**Версия:** v2.0
**Дата:** 2024-2025
**Статус:** ✅ Update Complete
**Время обновления:** ~30-60 минут в зависимости от сложности

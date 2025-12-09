% PANDORA v2.0 - Design System Documentation
% Полная документация дизайн-системы PANDORA
% 2024-2025

# 🎨 PANDORA v2.0 - Design System

## 📚 Содержание

1. [Введение](#введение)
2. [Design Tokens](#design-tokens)
3. [Компоненты](#компоненты)
4. [Макеты](#макеты)
5. [Анимации](#анимации)
6. [Утилиты](#утилиты)
7. [Примеры использования](#примеры-использования)

---

## Введение

PANDORA v2.0 использует современную дизайн-систему, основанную на **Design Tokens** - системе переиспользуемых переменных для всех визуальных свойств. Это позволяет:

✅ **Быстро менять тему** - весь интерфейс переключается одной строкой кода
✅ **Согласованность** - все компоненты используют одни и те же значения
✅ **Поддержка light/dark режимов** - встроенная поддержка обеих тем
✅ **Легко масштабировать** - добавляйте новые компоненты используя существующие токены

---

## Design Tokens

### 📁 Где находятся токены?

**Файл:** `frontend/css/design-tokens.css`

Все токены это CSS переменные (Custom Properties), которые определяют:

```css
--color-primary-50  /* Самый светлый оттенок */
--color-primary-500 /* Основной оттенок */
--color-primary-900 /* Самый тёмный оттенок */

--space-1 /* 4px */
--space-2 /* 8px */
--space-4 /* 16px */
/* и т.д. */

--font-size-base /* 16px */
--font-size-lg   /* 18px */
/* и т.д. */
```

### 🎨 Цветовая система

**3 основных цвета:**

1. **Primary (Индиго)** - основной цвет, логотип, ссылки
   - Dark: `#6366F1`
   - Range: 50, 100, 200, ..., 900

2. **Secondary (Фиолет)** - вторичный, акценты
   - Dark: `#8B5CF6`
   - Range: 50, 100, 200, ..., 900

3. **Accent (Розовый)** - для привлечения внимания
   - Dark: `#EC4899`
   - Range: 50, 100, 200, ..., 900

**Нейтральные оттенки:**

```css
--color-neutral-50    /* Почти белый */
--color-neutral-100
--color-neutral-200
--color-neutral-300
--color-neutral-400
--color-neutral-500   /* Середина */
--color-neutral-600
--color-neutral-700
--color-neutral-800
--color-neutral-900   /* Почти чёрный #0F172A */
```

**Использование:**

```html
<div class="bg-gradient-primary">Основной градиент</div>
<button class="text-primary">Основной цвет текста</button>
<span style="color: var(--color-primary-600)">Программный доступ</span>
```

### 📏 Система расстояний (Spacing)

Основана на **8px сетке**:

```css
--space-0  = 0px
--space-1  = 4px
--space-2  = 8px   /* базовое расстояние */
--space-3  = 12px
--space-4  = 16px  /* очень часто используется */
--space-6  = 24px
--space-8  = 32px
--space-12 = 48px
--space-16 = 64px
--space-20 = 80px
```

**Использование:**

```html
<div class="p-4">Padding 16px</div>
<div class="m-6">Margin 24px</div>
<div class="gap-4">Gap между flex/grid элементами</div>
```

### 🔤 Типография

**Размеры:**

```css
--font-size-xs   = 12px  /* подписи, small text */
--font-size-sm   = 14px  /* текст кнопок */
--font-size-base = 16px  /* основной текст */
--font-size-lg   = 18px  /* заголовки маленькие */
--font-size-xl   = 20px
--font-size-2xl  = 24px
--font-size-3xl  = 30px
--font-size-4xl  = 36px
--font-size-5xl  = 48px  /* главные заголовки */
```

**Веса шрифта:**

```css
--font-weight-light     = 300  /* редкое использование */
--font-weight-normal    = 400  /* обычный текст */
--font-weight-medium    = 500  /* акцент в тексте */
--font-weight-semibold  = 600  /* подзаголовки */
--font-weight-bold      = 700  /* заголовки, кнопки */
```

**Шрифты:**

```css
--font-family-primary = 'Inter', 'Plus Jakarta Sans', sans-serif
--font-family-mono    = 'JetBrains Mono', 'Courier New', monospace
```

### ⏱️ Анимации

**Скорости переходов:**

```css
--transition-fast     = 150ms cubic-bezier(0.4, 0, 0.2, 1)
--transition-standard = 250ms cubic-bezier(0.4, 0, 0.2, 1)
--transition-slow     = 500ms cubic-bezier(0.4, 0, 0.2, 1)
```

**Использование:**

```css
.button {
  transition: all var(--transition-fast);
}

.button:hover {
  transform: translateY(-2px);
  transition: all var(--transition-standard);
}
```

### 🎭 Тени (Shadows)

```css
--shadow-xs    /* маленькая тень для subtle эффектов */
--shadow-sm    /* small, для карточек */
--shadow-md    /* medium, для dropdown */
--shadow-lg    /* large, для модальных окон */
--shadow-xl
--shadow-2xl   /* очень большая тень */
```

### 📐 Скругления (Border Radius)

```css
--radius-sm    = 4px      /* маленькие элементы */
--radius-md    = 8px      /* обычные элементы */
--radius-lg    = 12px     /* карточки */
--radius-xl    = 16px
--radius-2xl   = 24px     /* большие блоки */
--radius-full  = 9999px   /* полная окружность */
```

---

## Компоненты

### 📁 Где находятся компоненты?

**Файл:** `frontend/css/components.css`

### 🔘 Кнопки

**Основные варианты:**

```html
<!-- Primary (главная кнопка) -->
<button class="btn btn-primary">Сохранить</button>

<!-- Secondary (вторичная) -->
<button class="btn btn-secondary">Отмена</button>

<!-- Ghost (без фона) -->
<button class="btn btn-ghost">Подробнее</button>

<!-- Danger (опасное действие) -->
<button class="btn btn-danger">Удалить</button>
```

**Размеры:**

```html
<button class="btn btn-sm btn-primary">Маленькая</button>
<button class="btn btn-primary">Средняя (по умолчанию)</button>
<button class="btn btn-lg btn-primary">Большая</button>

<!-- Круглая иконка кнопка -->
<button class="btn btn-primary btn-icon">⚙️</button>
```

**Состояния:**

```html
<button class="btn btn-primary" disabled>Disabled</button>
<button class="btn btn-primary loading">
  <span class="spinner"></span> Загрузка...
</button>
```

### 🎴 Карточки

```html
<div class="card">
  <div class="card-header">
    <h3 class="card-title">Заголовок карточки</h3>
    <button class="btn btn-ghost">...</button>
  </div>
  
  <div class="card-body">
    <p>Содержимое карточки</p>
  </div>
  
  <div class="card-footer">
    <span>Подпись</span>
    <button class="btn btn-sm btn-primary">Действие</button>
  </div>
</div>
```

**С иконкой:**

```html
<div class="card card-with-icon">
  <div class="card-icon">🎯</div>
  <div>
    <h4 class="card-title">Заголовок</h4>
    <p class="card-subtitle">Описание</p>
  </div>
</div>
```

### ✍️ Инпуты и формы

```html
<div class="input-group">
  <label for="email">Email</label>
  <input 
    type="email" 
    class="input" 
    id="email"
    placeholder="your@email.com"
  />
</div>

<!-- С иконкой -->
<div class="input-wrapper">
  <span class="input-icon">🔍</span>
  <input type="text" class="input" placeholder="Поиск...">
</div>

<!-- С ошибкой -->
<div class="input-group">
  <label>Пароль</label>
  <input type="password" class="input error">
  <div class="error-message">Пароль слишком короткий</div>
</div>

<!-- Textarea -->
<textarea class="textarea" placeholder="Ваше сообщение..."></textarea>
```

### 🏷️ Бэджи и теги

```html
<!-- Badge (значок) -->
<span class="badge">Новое 🆕</span>
<span class="badge badge-success">Активен ✓</span>
<span class="badge badge-danger">Ошибка ✕</span>

<!-- Tag (тег) -->
<span class="tag">Python</span>
<span class="tag active">React ×</span>

<!-- С эмодзи -->
<span class="tag">
  <span class="tag-emoji">🎨</span>
  Дизайн
</span>
```

### 🪟 Модальные окна

```html
<!-- Trigger -->
<button class="btn btn-primary" data-modal-trigger="confirm-modal">
  Открыть диалог
</button>

<!-- Modal -->
<div class="modal-backdrop" data-modal-id="confirm-modal">
  <div class="modal">
    <div class="modal-header">
      <h2 class="modal-title">Подтверждение</h2>
      <button class="modal-close" data-modal-close>✕</button>
    </div>
    
    <div class="modal-body">
      <p>Вы уверены?</p>
    </div>
    
    <div class="modal-footer">
      <button class="btn btn-secondary" data-modal-close>Отмена</button>
      <button class="btn btn-primary">Подтвердить</button>
    </div>
  </div>
</div>
```

---

## Макеты

### 🎯 Grid система

```html
<!-- Автоматическая сетка -->
<div class="grid">
  <div>Элемент 1</div>
  <div>Элемент 2</div>
  <div>Элемент 3</div>
</div>

<!-- Фиксированное количество столбцов -->
<div class="grid grid-cols-3">
  <div>Col 1</div>
  <div>Col 2</div>
  <div>Col 3</div>
</div>

<!-- Flex с gap -->
<div class="flex gap-4">
  <div>Item 1</div>
  <div>Item 2</div>
</div>
```

### 📱 Адаптивная сетка

```html
<div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4">
  <div>Адаптивный элемент</div>
</div>
```

---

## Анимации

### 📁 Где находятся анимации?

**Файл:** `frontend/css/animations.css`

### ✨ Встроенные анимации

```html
<!-- Появление -->
<div class="animate-fade-in">Fade in</div>
<div class="animate-slide-up">Slide up</div>
<div class="animate-zoom-in">Zoom in</div>

<!-- Заголовок с эффектом -->
<h1 class="animate-bounce-in">Привет! 👋</h1>

<!-- Бесконечные анимации -->
<div class="animate-pulse">Пульс</div>
<div class="animate-spin">⏳ Загрузка...</div>
<div class="animate-bounce">Прыг-скок</div>

<!-- С задержкой (для stagger эффекта) -->
<div class="animate-slide-up delay-100">Item 1</div>
<div class="animate-slide-up delay-200">Item 2</div>
<div class="animate-slide-up delay-300">Item 3</div>
```

### 🎬 Кастомные анимации

```css
/* Создаём свою анимацию */
@keyframes my-animation {
  from {
    opacity: 0;
    transform: translateX(-20px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

/* Применяем */
.my-element {
  animation: my-animation var(--transition-standard);
}
```

---

## Утилиты

### 📁 Где находятся утилиты?

**Файл:** `frontend/css/utilities.css`

### Примеры утилит

```html
<!-- Margin & Padding -->
<div class="p-4 m-4 mt-8 mb-6">
  Отступы и поля
</div>

<!-- Display -->
<div class="flex items-center justify-between gap-4">
  Гибкий контейнер
</div>

<!-- Размеры -->
<div class="w-full h-screen">Полная ширина и высота</div>

<!-- Текст -->
<p class="text-lg font-bold text-primary">Большой жирный текст</p>

<!-- Фон и граница -->
<div class="bg-primary-500 rounded-lg shadow-md border border-primary">
  Стилизованный блок
</div>

<!-- Адаптивность -->
<div class="grid-cols-1 sm:grid-cols-2 md:grid-cols-3">
  Адаптивная сетка
</div>
```

---

## Примеры использования

### 📝 Пример 1: Простая карточка

```html
<div class="card">
  <h3 class="card-title">Мой первый проект</h3>
  <p class="card-subtitle">Создано вчера</p>
  
  <div class="card-body">
    <p>Описание проекта...</p>
  </div>
  
  <div class="card-footer">
    <span class="badge badge-success">Активен</span>
    <button class="btn btn-sm btn-primary">Открыть</button>
  </div>
</div>
```

### 📝 Пример 2: Форма с валидацией

```html
<form class="form-grid">
  <div class="input-group">
    <label>Имя</label>
    <input type="text" class="input" placeholder="Ваше имя">
  </div>
  
  <div class="input-group">
    <label>Email</label>
    <input type="email" class="input error">
    <div class="error-message">Некорректный email</div>
  </div>
  
  <div class="input-group">
    <label>Сообщение</label>
    <textarea class="textarea"></textarea>
  </div>
  
  <div class="flex gap-2">
    <button class="btn btn-primary">Отправить</button>
    <button class="btn btn-secondary">Отмена</button>
  </div>
</form>
```

### 📝 Пример 3: Список с фильтрацией

```html
<div>
  <!-- Фильтр -->
  <div class="filter-bar">
    <div class="filter-section">
      <label class="filter-label">Сортировка</label>
      <select class="input">
        <option>По дате</option>
        <option>По названию</option>
      </select>
    </div>
    
    <div class="flex gap-2 flex-wrap">
      <span class="tag active">Все</span>
      <span class="tag">Активные</span>
      <span class="tag">Архивные</span>
    </div>
  </div>
  
  <!-- Список -->
  <div class="list-container">
    <div class="list-item">
      <span class="tag-emoji">📝</span>
      <div class="flex-1">
        <h4 class="text-base font-semibold">Заголовок</h4>
        <p class="text-sm text-secondary">Описание</p>
      </div>
      <button class="btn btn-ghost">→</button>
    </div>
  </div>
</div>
```

---

## 🎨 Как использовать в HTML

### Подключение стилей

```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  
  <!-- Главный файл стилей (импортирует всё остальное) -->
  <link rel="stylesheet" href="/frontend/css/styles.css">
</head>
<body>
  <div id="app">
    <!-- Ваш контент здесь -->
  </div>
  
  <!-- JavaScript для интерактивности -->
  <script src="/frontend/js/app.js"></script>
</body>
</html>
```

### Переключение темы

```javascript
// Переключить тему программно
window.App.theme.toggleTheme();

// Получить текущую тему
const currentTheme = window.App.theme.getCurrentTheme(); // 'light' или 'dark'

// Установить конкретную тему
window.App.theme.setTheme('dark');

// Слушать изменения темы
document.addEventListener('theme-changed', (e) => {
  console.log('Тема изменена на:', e.detail.theme);
});
```

### Показать уведомление

```javascript
// Toast notifications
App.ui.showToast('Сохранено!', 'success');
App.ui.showToast('Ошибка при сохранении', 'error');
App.ui.showToast('Внимание!', 'warning');
App.ui.showToast('Информация', 'info');
```

### Открыть модальное окно

```javascript
// Открыть модаль
App.ui.openModal('confirm-modal');

// Закрыть модаль
App.ui.closeModal('confirm-modal');

// Закрыть все модали
App.ui.closeAllModals();
```

---

## ✅ Чек-лист для разработчика

При создании нового компонента:

- [ ] Использую Design Tokens (цвета, размеры, шрифты)
- [ ] Добавил поддержку light/dark тем
- [ ] Указал правильный border-radius
- [ ] Добавил transition для интерактивных элементов
- [ ] Проверил адаптивность на мобильных
- [ ] Добавил accessibility атрибуты (aria-label, role)
- [ ] Протестировал на клавиатуре
- [ ] Добавил анимации для лучшего UX

---

## 📚 Дополнительные ресурсы

- **Design Tokens**: `frontend/css/design-tokens.css`
- **Компоненты**: `frontend/css/components.css`
- **Анимации**: `frontend/css/animations.css`
- **Утилиты**: `frontend/css/utilities.css`
- **Главные стили**: `frontend/css/styles.css`
- **JavaScript**: `frontend/js/app.js`

---

**Последнее обновление:** 2024
**Версия:** v2.0
**Автор:** PANDORA Team ✨

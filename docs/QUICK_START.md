% PANDORA v2.0 - Quick Start Guide
% Быстрый гайд для начала работы с v2.0
% 2024-2025

# 🚀 PANDORA v2.0 - Quick Start Guide

## ⚡ 30-сек старт

### 1. Подключите CSS (одна строка)
```html
<link rel="stylesheet" href="css/styles.css">
```

### 2. Добавьте шрифты
```html
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
```

### 3. Подключите JavaScript
```html
<script src="js/app.js"></script>
```

### 4. Используйте компоненты!
```html
<button class="btn btn-primary">Кликните меня</button>
<div class="card">Карточка</div>
```

**Готово!** Ваш сайт теперь выглядит как PANDORA v2.0 ✨

---

## 📚 Основные компоненты (5 минут)

### Кнопки
```html
<!-- 4 варианта -->
<button class="btn btn-primary">Primary</button>
<button class="btn btn-secondary">Secondary</button>
<button class="btn btn-ghost">Ghost</button>
<button class="btn btn-danger">Danger</button>

<!-- 3 размера -->
<button class="btn btn-sm btn-primary">Small</button>
<button class="btn btn-primary">Default</button>
<button class="btn btn-lg btn-primary">Large</button>

<!-- Иконка кнопка -->
<button class="btn btn-icon btn-primary">⚙️</button>
```

### Карточки
```html
<div class="card">
  <div class="card-header">
    <h3 class="card-title">Заголовок</h3>
  </div>
  <div class="card-body">
    Содержимое карточки
  </div>
  <div class="card-footer">
    <button class="btn btn-sm btn-primary">Действие</button>
  </div>
</div>
```

### Инпуты
```html
<div class="input-group">
  <label>Ваше имя</label>
  <input type="text" class="input" placeholder="Введите...">
</div>

<!-- С ошибкой -->
<div class="input-group">
  <label>Email</label>
  <input type="email" class="input error" placeholder="...">
  <div class="error-message">Некорректный email</div>
</div>
```

### Бэджи и теги
```html
<!-- Бэджи -->
<span class="badge">Новое</span>
<span class="badge badge-success">Активен</span>

<!-- Теги -->
<span class="tag">Python</span>
<span class="tag active">React ✕</span>
```

---

## 🎨 Цвета (2 минут)

### Основные цвета
```html
<!-- Text цвета -->
<p class="text-primary">Основной цвет</p>
<p class="text-secondary">Вторичный цвет</p>
<p class="text-accent">Акцент</p>

<!-- Background цвета -->
<div class="bg-primary-500">Основной фон</div>
<div class="bg-gradient-primary">Градиент</div>
```

### Палитра
- **Primary (Индиго):** #6366F1 - основной цвет
- **Secondary (Фиолет):** #8B5CF6 - вторичный
- **Accent (Розовый):** #EC4899 - привлечение внимания
- **Success (Зелёный):** #22c55e
- **Warning (Оранжевый):** #fb923c
- **Error (Красный):** #ef4444

Каждый цвет имеет 10 оттенков: 50, 100, 200, ..., 900

---

## 📏 Отступы (2 минуты)

### Margin & Padding
```html
<!-- Со всех сторон -->
<div class="m-4">Margin 16px</div>
<div class="p-6">Padding 24px</div>

<!-- Горизонтально/вертикально -->
<div class="mx-4">Margin left/right</div>
<div class="py-4">Padding top/bottom</div>

<!-- Конкретные стороны -->
<div class="mt-4 mb-6 pl-2">Custom отступы</div>
```

### Значения (8px сетка)
```
--space-1  = 4px
--space-2  = 8px
--space-3  = 12px
--space-4  = 16px  ← часто используется
--space-6  = 24px
--space-8  = 32px
... и т.д. до 80px
```

---

## 🏗️ Макеты (3 минут)

### Flex контейнер
```html
<!-- Строка, центрирован -->
<div class="flex items-center justify-center gap-4">
  <div>Item 1</div>
  <div>Item 2</div>
</div>

<!-- Колонна, распределение -->
<div class="flex flex-col gap-2 justify-between">
  <div>Top</div>
  <div>Bottom</div>
</div>
```

### Grid контейнер
```html
<!-- Сетка 3 столбца -->
<div class="grid grid-cols-3 gap-4">
  <div>Card 1</div>
  <div>Card 2</div>
  <div>Card 3</div>
</div>

<!-- Адаптивная сетка -->
<div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3">
  Меняется по размеру экрана
</div>
```

---

## 🌓 Тёмный режим (1 минута)

### Переключить тему
```javascript
// Переключить между light и dark
App.theme.toggleTheme();

// Получить текущую тему
App.theme.getCurrentTheme(); // 'light' или 'dark'

// Установить конкретную
App.theme.setTheme('dark');

// Слушать изменения
document.addEventListener('theme-changed', (e) => {
  console.log('Новая тема:', e.detail.theme);
});
```

### Button для переключения
```html
<button 
  class="btn btn-icon"
  data-action="toggle-theme"
  title="Переключить тему"
>
  🌙
</button>
```

---

## 💬 Модальные окна (2 минут)

### Создать модаль
```html
<!-- Кнопка для открытия -->
<button class="btn btn-primary" data-modal-trigger="my-modal">
  Открыть
</button>

<!-- Сама модаль -->
<div class="modal-backdrop" data-modal-id="my-modal">
  <div class="modal">
    <div class="modal-header">
      <h2 class="modal-title">Заголовок</h2>
      <button class="modal-close" data-modal-close>✕</button>
    </div>
    
    <div class="modal-body">
      Содержимое здесь
    </div>
    
    <div class="modal-footer">
      <button class="btn btn-secondary" data-modal-close>
        Отмена
      </button>
      <button class="btn btn-primary">Действие</button>
    </div>
  </div>
</div>
```

### JavaScript управление
```javascript
App.ui.openModal('my-modal');
App.ui.closeModal('my-modal');
App.ui.closeAllModals();
```

---

## 🔔 Уведомления (1 минута)

### Показать тост
```javascript
// Успех
App.ui.showToast('Сохранено!', 'success');

// Ошибка
App.ui.showToast('Произошла ошибка', 'error');

// Предупреждение
App.ui.showToast('Внимание!', 'warning');

// Информация
App.ui.showToast('Информационное сообщение', 'info');

// С кастомной длительностью
App.ui.showToast('Быстро исчезнет', 'info', 2000);
```

---

## ✨ Анимации (2 минут)

### Встроенные анимации
```html
<!-- Появление -->
<div class="animate-fade-in">Fade in</div>
<div class="animate-slide-up">Slide up</div>
<div class="animate-zoom-in">Zoom in</div>

<!-- Эффекты -->
<div class="animate-pulse">Пульс</div>
<div class="animate-spin">Вращение</div>
<div class="animate-bounce">Прыг-скок</div>

<!-- С задержкой (для последовательности) -->
<div class="animate-slide-up delay-100">Item 1</div>
<div class="animate-slide-up delay-200">Item 2</div>
<div class="animate-slide-up delay-300">Item 3</div>
```

### Скорости
```css
--transition-fast     = 150ms  (для быстрого фидбэка)
--transition-standard = 250ms  (обычный переход)
--transition-slow     = 500ms  (привлечение внимания)
```

---

## 🎯 Практические примеры (5 минут)

### Пример 1: Кнопка с ауты
```html
<div class="flex items-center gap-4">
  <button class="btn btn-primary">Сохранить</button>
  <button class="btn btn-secondary">Отмена</button>
</div>
```

### Пример 2: Форма
```html
<form class="form-grid">
  <div class="input-group">
    <label>Имя</label>
    <input type="text" class="input">
  </div>
  
  <div class="input-group">
    <label>Email</label>
    <input type="email" class="input">
  </div>
  
  <div class="flex gap-4" style="grid-column: 1 / -1;">
    <button class="btn btn-primary">Отправить</button>
    <button class="btn btn-secondary">Reset</button>
  </div>
</form>
```

### Пример 3: Карточка с изображением
```html
<div class="card animate-slide-up">
  <img src="image.jpg" style="width: 100%; border-radius: var(--radius-lg); margin-bottom: var(--space-4);">
  
  <h3 class="card-title">Название</h3>
  <p class="card-subtitle">Подпись</p>
  
  <div class="card-body">
    <p>Описание продукта...</p>
  </div>
  
  <div class="card-footer">
    <span class="badge badge-success">В наличии</span>
    <button class="btn btn-primary">Купить</button>
  </div>
</div>
```

### Пример 4: Dashboard stats
```html
<div class="dashboard-grid">
  <div class="stat-card">
    <div class="stat-value">1,234</div>
    <div class="stat-label">Пользователей</div>
    <p class="text-sm text-secondary mt-2">↑ 12% за неделю</p>
  </div>
  
  <div class="stat-card">
    <div class="stat-value">5,678</div>
    <div class="stat-label">Продаж</div>
    <p class="text-sm text-secondary mt-2">↑ 23% за месяц</p>
  </div>
  
  <div class="stat-card">
    <div class="stat-value">89%</div>
    <div class="stat-label">Удовлетворение</div>
    <p class="text-sm text-secondary mt-2">Отличный результат</p>
  </div>
</div>
```

---

## 🔧 JavaScript утилиты (2 минут)

### Копирование в буфер обмена
```javascript
App.utils.copyToClipboard('текст для копирования');
```

### Анимация счётчика
```javascript
const element = document.querySelector('.number');
App.utils.animateNumber(element, 100, 1000); // до 100 за 1 сек
```

### Проверка мобильного
```javascript
if (App.utils.isMobile()) {
  // мобильный код
}
```

### Плавный скролл
```javascript
App.utils.smoothScroll('#target-section');
```

### Дебаунс (для поиска)
```javascript
const search = App.utils.debounce((query) => {
  // поиск по query
}, 300);

input.addEventListener('input', (e) => search(e.target.value));
```

---

## ⌨️ Горячие клавиши (1 минута)

### Встроенные
```
Ctrl+K (Cmd+K на Mac)      → Фокус на поиск
Escape                    → Закрыть модали
Ctrl+/ (Cmd+/)            → Справка
Ctrl+Shift+L (Cmd+Shift+L) → Переключить тему
```

### Добавить свою
```javascript
App.shortcuts.register('ctrl+s', 'cmd+s', () => {
  console.log('Сохранить!');
});
```

---

## 🚀 Полезные утилити классы

### Размер текста
```
text-xs, text-sm, text-base, text-lg, text-xl, text-2xl, text-3xl, text-4xl, text-5xl
```

### Вес текста
```
font-light, font-normal, font-medium, font-semibold, font-bold
```

### Цвета текста
```
text-primary, text-secondary, text-tertiary, text-accent, text-danger, text-success
```

### Border radius
```
rounded-sm, rounded-md, rounded-lg, rounded-xl, rounded-2xl, rounded-full
```

### Тени
```
shadow-xs, shadow-sm, shadow-md, shadow-lg, shadow-xl, shadow-2xl
```

### Display
```
block, inline-block, inline, flex, inline-flex, grid, hidden, invisible
```

---

## 🧪 Тестирование

### Light & Dark режимы
```javascript
// Быстро переключать для тестирования
App.theme.setTheme('light');
App.theme.setTheme('dark');
```

### Responsive тестирование
Используйте браузерные инструменты (F12 → Toggle device toolbar)
- Мобильные: < 640px
- Планшеты: 640px - 1024px
- Десктоп: > 1024px

### Проверка контрастности
Все цвета соответствуют WCAG AA стандартам

---

## 📖 Где искать помощь

1. **DESIGN_SYSTEM.md** - полное описание всех компонентов
2. **index-v2.html** - примеры всех компонентов
3. **INTEGRATION_GUIDE.md** - более детальная документация
4. **app.js** - код JavaScript функций

---

## 🎉 Вы готовы!

Теперь вы можете:
✅ Создавать красивые кнопки
✅ Строить современные формы
✅ Делать гладкие анимации
✅ Переключать тему на лету
✅ Показывать модальные окна и уведомления

**Начните работать с v2.0!** 🚀

---

**Версия:** v2.0
**Дата:** 2024-2025
**Статус:** ✅ Production Ready
**Размер:** 40 KB (CSS + JS)

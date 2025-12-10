# Toast Notifications System - v2.0.2

## 📋 Обзор

**Toast Notifications** - это система уведомлений для пользователя в PANDORA v2.0. Toast'ы автоматически появляются в нижнем правом углу экрана и показывают информационные сообщения о выполнении операций.

## 🎯 Возможности

✅ **4 типа уведомлений**:
- **Success** (зеленый) - успешное завершение операции
- **Error** (красный) - ошибка при выполнении операции  
- **Warning** (оранжевый) - предупреждение
- **Info** (синий) - информационное сообщение

✅ **Функции**:
- Автоматическое скрытие через заданный интервал
- Ручное закрытие кнопкой "✕"
- Анимация появления/исчезновения (slideInRight/slideOutRight)
- Иконки для каждого типа
- Поддержка длинных текстов с переносом
- Responsive дизайн для мобильных устройств
- Dark mode поддержка

## 📚 API

### Глобальный доступ

```javascript
window.Toast.success(message, duration)  // Зеленое уведомление
window.Toast.error(message, duration)    // Красное уведомление
window.Toast.warning(message, duration)  // Оранжевое уведомление
window.Toast.info(message, duration)     // Синее уведомление
```

### Примеры использования

```javascript
// Успешное уведомление, скроется через 3 секунды (по умолчанию)
window.Toast.success('Prompt saved successfully');

// Ошибка с кастомной длительностью (5 секунд)
window.Toast.error('Failed to load data', 5000);

// Предупреждение (4 секунды)
window.Toast.warning('This action cannot be undone', 4000);

// Информация (не скроется автоматически)
window.Toast.info('Click to dismiss', 0);

// Кастомное уведомление с собственной иконкой и цветом
window.Toast.custom(
    'Processing...',
    '⏳',
    '#6b7280',  // backgroundColor
    0           // duration
);
```

## 🔧 Параметры

| Параметр | Тип | По умолчанию | Описание |
|----------|-----|--------------|---------|
| `message` | `string` | - | Текст уведомления |
| `type` | `string` | `'info'` | Тип: 'success', 'error', 'warning', 'info' |
| `duration` | `number` | Зависит от типа | Время отображения в мс (0 = не скрывать) |

### Длительность по умолчанию

- **success**: 3000ms
- **error**: 5000ms
- **warning**: 4000ms
- **info**: 4000ms

## 📍 Расположение и Стили

Toast'ы появляются в **нижнем правом углу** экрана:

```
+----------------------------------+
|                                  |
|                   ✓ Success      |
|                                  |
+----------------------------------+
```

### Цвета

```css
.toast-success  { background-color: #10b981; }  /* Green */
.toast-error    { background-color: #ef4444; }  /* Red */
.toast-warning  { background-color: #f59e0b; }  /* Amber */
.toast-info     { background-color: #3b82f6; }  /* Blue */
```

## 🎬 Анимации

Включены две основные анимации:

### slideInRight (появление)
```css
@keyframes slideInRight {
    from { opacity: 0; transform: translateX(400px); }
    to { opacity: 1; transform: translateX(0); }
}
```

### slideOutRight (исчезновение)
```css
@keyframes slideOutRight {
    from { opacity: 1; transform: translateX(0); }
    to { opacity: 0; transform: translateX(400px); }
}
```

## 🔗 Интеграция

### 1. HTTP Client интеграция (app.js)

Автоматически показывает error toast при ошибках запроса:

```javascript
try {
    const response = await fetch(url, options);
    
    if (!response.ok) {
        // Автоматически показывает error toast
        Toast.error(`Error ${response.status}: ${response.statusText}`);
    }
} catch (error) {
    // Показывает error toast при сетевых ошибках
    Toast.error(`Request failed: ${error.message}`);
}
```

### 2. CRUD операции (PromptsView.js)

Показывает Toast при успешных/неудачных операциях:

```javascript
// При загрузке промптов
window.Toast?.success(`Loaded ${allPrompts.length} prompts`, 2000);

// При удалении
window.Toast?.success('Prompt deleted successfully');

// При ошибке
window.Toast?.error(`Failed to delete prompt: ${error.message}`);
```

## 📁 Файлы

| Файл | Описание |
|------|---------|
| `frontend/src/components/Toast.js` | Компонент Toast |
| `frontend/src/css/toast.css` | Стили Toast |
| `frontend/src/core/app.js` | Интеграция с HTTP Client |
| `frontend/src/views/PromptsView.js` | Примеры использования |

## 🔄 Примеры из кода

### Загрузка данных

```javascript
async function loadPrompts() {
    try {
        const response = await window.http.get('/api/prompts');
        allPrompts = response.data || [];
        
        if (allPrompts.length > 0) {
            window.Toast?.success(`Loaded ${allPrompts.length} prompts`, 2000);
        }
    } catch (error) {
        window.Toast?.error(`Failed to load prompts: ${error.message}`);
    }
}
```

### Удаление элемента

```javascript
card.querySelector('.btn-icon[title="Delete"]')
    .addEventListener('click', async (e) => {
        if (confirm('Delete this prompt?')) {
            try {
                await window.http.delete(`/api/prompts/${id}`);
                window.Toast?.success('Prompt deleted successfully');
            } catch (err) {
                window.Toast?.error(`Failed to delete: ${err.message}`);
            }
        }
    });
```

## 🎓 Best Practices

### ✅ ДО

```javascript
// Хорошо: информативное, краткое сообщение
window.Toast.success('Prompt saved');
window.Toast.error('Failed to save prompt');
```

### ❌ ПОСЛЕ

```javascript
// Плохо: слишком длинное
window.Toast.error('An error occurred while trying to save the prompt. Please check your internet connection and try again.');

// Плохо: слишком техничное
window.Toast.error('Error 422: Unprocessable Entity');
```

## 🐛 Troubleshooting

### Toast не появляется

**Проверка:**
1. Убедитесь что `window.Toast` определен:
   ```javascript
   console.log(window.Toast); // должен быть объект ToastManager
   ```

2. Проверьте CSS подключен в index.html:
   ```html
   <link rel="stylesheet" href="./css/toast.css">
   ```

3. Убедитесь что JavaScript выполняется (откройте консоль F12)

### Toast скрывается слишком быстро/медленно

Измените duration параметр:

```javascript
// Дольше (10 секунд)
window.Toast.success('Message', 10000);

// Короче (1 секунда)
window.Toast.success('Message', 1000);

// Никогда не скроется (ручное закрытие)
window.Toast.success('Click to dismiss', 0);
```

### Toast перекрывает контент

Измените позицию в CSS:

```css
#toast-container {
    /* Для левого верхнего угла: */
    top: 20px;
    left: 20px;
    right: auto;
    bottom: auto;
}
```

## 📊 Статистика

- **Размер компонента**: ~7 KB (неминифицированный)
- **Зависимости**: Нет (vanilla JavaScript)
- **Браузеры**: Все современные (ES6+)
- **Accessibility**: Поддерживает screen readers

## 🔮 Планы на будущее

- [ ] Queue управление (ограничение количества одновременных Toast'ов)
- [ ] Action buttons в Toast'ах (Undo, Retry)
- [ ] Progress bar для долгих операций
- [ ] Sound notifications
- [ ] Toast history/log

## ✅ Чек-лист интеграции

При добавлении нового компонента с Toast:

- [ ] Импортирован `window.Toast` в нужной view
- [ ] Используются типы: success/error/warning/info
- [ ] Сообщения информативны и краткие
- [ ] Длительность подходит для типа уведомления
- [ ] Протестировано в браузере (F12 → Console)
- [ ] Работает на мобильных устройствах

---

**Версия**: 2.0.2  
**Дата**: 2025-12-10  
**Статус**: ✅ Готов к использованию

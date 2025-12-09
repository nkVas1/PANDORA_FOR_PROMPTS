# 🚀 PANDORA v2.0 - Phase 3 Развитие функционала (АКТУАЛИЗИРОВАННЫЙ ПЛАН)

**Версия:** 2.0.1  
**Дата начала:** 9 декабря 2025  
**Статус:** 🔄 IN PROGRESS  
**Исправлено:** Адаптивность и layout система

---

## 📋 Обзор Phase 3

Phase 3 - это разработка основного функционала приложения согласно концепции DESIGN_VISION_v2.0.md.

### Что уже сделано в Phase 3:
- ✅ Создана профессиональная система build/deployment (5 скриптов)
- ✅ Написана полная документация по развертыванию
- ✅ **ИСПРАВЛЕНА адаптивность и layout система**
- ✅ Создана новая CSS система layout-system.css

### Что остаётся делать:
- 🔄 Интеграция API search (в прогрессе после fix)
- 🔄 Реализация enhanced editor
- 🔄 Система таггирования
- 🔄 Analytics dashboard
- 🔄 Финальная сборка EXE v2.0.1

---

## 🔄 Task 1: Интеграция API Search (2-3 часа)

### Что есть сейчас
- ✅ Frontend search UI (HTML + CSS)
- ✅ Search debounce (300ms)
- ✅ Keyboard navigation (arrows, escape, enter)
- ❌ API integration (placeholder только)

### Что нужно сделать

#### 1.1 Подключить к API endpoint
```javascript
// Файл: frontend/index.html, функция performSearch()
async function performSearch(query) {
  try {
    const response = await fetch(
      `${API_URL}/api/prompts/search?q=${query}&limit=10`
    );
    const data = await response.json();
    
    if (data.results && data.results.length > 0) {
      displaySearchResults(data.results);
    }
  } catch (error) {
    console.error('Search error:', error);
  }
}
```

#### 1.2 Отобразить результаты
```javascript
function displaySearchResults(results) {
  const html = results.map(item => `
    <div class="search-result-item" onclick="selectPrompt('${item.id}')">
      <div class="search-result-icon">✨</div>
      <div class="search-result-content">
        <div class="search-result-title">${item.title}</div>
        <div class="search-result-preview">${item.content.substring(0, 60)}...</div>
        <div class="search-result-category">${item.category || 'General'}</div>
      </div>
    </div>
  `).join('');
  
  searchResults.innerHTML = html;
  searchResults.style.display = 'block';
}
```

#### 1.3 Навигация и выбор
```javascript
// Выбор промпта по ID
function selectPrompt(promptId) {
  // Загрузить полный промпт
  fetch(`${API_URL}/api/prompts/${promptId}`)
    .then(r => r.json())
    .then(prompt => openPromptEditor(prompt));
}

// Открыть редактор с промптом
function openPromptEditor(prompt) {
  // Переключиться на page: prompts
  // Заполнить форму данными
  // Показать модальное окно редактирования
}
```

### Файлы для изменения
- `frontend/index.html` - строка 675+ (функция performSearch)
- `frontend/js/app.js` - добавить selectPrompt, displaySearchResults

### Время реализации: 1-2 часа

---

## 🛠️ Task 2: Enhanced Prompt Editor (4-6 часов)

### Концепция (из DESIGN_VISION_v2.0.md)
Расширенный редактор для создания и редактирования промптов с:
- Syntax highlighting для code blocks
- Live preview (markdown)
- Character/word count
- Version history
- Drag-and-drop для файлов
- Auto-save

### Архитектура

#### 2.1 HTML форма
```html
<div id="prompt-modal" class="modal">
  <div class="modal-content">
    <!-- Информация о промпте -->
    <input type="text" id="prompt-title" placeholder="Название промпта">
    <select id="prompt-category">
      <option>General</option>
      <option>Code</option>
      <option>Writing</option>
      <!-- ... -->
    </select>

    <!-- Редактор -->
    <div class="editor-container">
      <div class="editor-left">
        <textarea id="prompt-content" placeholder="Напишите промпт..."></textarea>
        <div class="editor-meta">
          <span id="char-count">0 chars</span> | 
          <span id="word-count">0 words</span>
        </div>
      </div>

      <div class="editor-right">
        <div id="prompt-preview" class="preview-pane markdown"></div>
      </div>
    </div>

    <!-- Управление -->
    <div class="modal-actions">
      <button class="btn btn-secondary" onclick="closeModal()">Отмена</button>
      <button class="btn btn-primary" onclick="savePrompt()">Сохранить</button>
    </div>
  </div>
</div>
```

#### 2.2 JavaScript логика
```javascript
class PromptEditor {
  constructor(containerId) {
    this.container = document.getElementById(containerId);
    this.init();
  }

  init() {
    // Обработчики для auto-save
    this.contentInput = this.container.querySelector('#prompt-content');
    this.contentInput.addEventListener('input', (e) => {
      this.updatePreview(e.target.value);
      this.updateStats(e.target.value);
      this.autoSave();
    });
  }

  updatePreview(markdown) {
    // Используем marked.js или простой конвертер
    const html = this.convertMarkdown(markdown);
    this.container.querySelector('#prompt-preview').innerHTML = html;
  }

  updateStats(text) {
    const chars = text.length;
    const words = text.split(/\s+/).length;
    this.container.querySelector('#char-count').textContent = `${chars} chars`;
    this.container.querySelector('#word-count').textContent = `${words} words`;
  }

  autoSave() {
    // Сохранить в localStorage для восстановления
    const draft = {
      title: this.container.querySelector('#prompt-title').value,
      content: this.contentInput.value,
      category: this.container.querySelector('#prompt-category').value,
      savedAt: new Date().toISOString()
    };
    localStorage.setItem('prompt-draft', JSON.stringify(draft));
  }
}
```

#### 2.3 CSS стили
```css
.editor-container {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--space-6);
  height: 500px;
}

.editor-left {
  display: flex;
  flex-direction: column;
}

#prompt-content {
  flex: 1;
  padding: var(--space-4);
  font-family: 'JetBrains Mono', monospace;
  font-size: 14px;
  line-height: 1.6;
  background: var(--bg-secondary);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-lg);
  resize: none;
}

.editor-right {
  overflow-y: auto;
  padding: var(--space-4);
  background: var(--bg-secondary);
  border-radius: var(--radius-lg);
  border: 1px solid var(--border-color);
}

.preview-pane.markdown {
  font-size: 14px;
  line-height: 1.8;
}

.preview-pane.markdown h1 { font-size: 28px; font-weight: bold; margin-bottom: var(--space-3); }
.preview-pane.markdown h2 { font-size: 22px; font-weight: bold; margin-bottom: var(--space-2); }
.preview-pane.markdown code { 
  background: var(--bg-primary); 
  padding: 2px 6px; 
  border-radius: 4px;
  font-family: 'JetBrains Mono', monospace;
}

@media (max-width: 1024px) {
  .editor-container {
    grid-template-columns: 1fr;
  }

  .editor-right {
    max-height: 300px;
  }
}
```

### Файлы для создания/изменения
- `frontend/js/editor.js` (NEW) - PromptEditor class
- `frontend/index.html` - добавить HTML для модального окна
- `frontend/css/editor.css` (NEW) - стили редактора

### Зависимости
- Optional: marked.js для markdown parsing (добавить в requirements.txt)

### Время реализации: 4-5 часов

---

## 🏷️ Task 3: Система Таггирования (3-4 часа)

### Концепция
- Управление тегами и категориями
- Auto-tagging при создании промпта
- Фильтрация по тегам
- Тег облако (tag cloud)
- Редактирование тегов

### Архитектура

#### 3.1 Backend (FastAPI)
```python
# backend/app/api/routes.py

@router.post("/api/tags")
def create_tag(tag: TagCreate, db: Session = Depends(get_db)):
    """Создать новый тег"""
    db_tag = Tag(**tag.dict())
    db.add(db_tag)
    db.commit()
    return db_tag

@router.put("/api/tags/{tag_id}")
def update_tag(tag_id: int, tag: TagUpdate, db: Session = Depends(get_db)):
    """Обновить тег"""
    db_tag = db.query(Tag).filter(Tag.id == tag_id).first()
    db_tag.name = tag.name
    db.commit()
    return db_tag

@router.delete("/api/tags/{tag_id}")
def delete_tag(tag_id: int, db: Session = Depends(get_db)):
    """Удалить тег"""
    db.query(Tag).filter(Tag.id == tag_id).delete()
    db.commit()
    return {"status": "deleted"}

@router.get("/api/tags/cloud")
def get_tag_cloud(db: Session = Depends(get_db)):
    """Получить облако тегов"""
    tags = db.query(Tag).all()
    # Добавить count для каждого тега
    return [{"name": t.name, "count": len(t.prompts)} for t in tags]
```

#### 3.2 Frontend (HTML/JS)
```html
<!-- Tags Page в index.html -->
<div id="tags" class="page">
  <div class="page-header">
    <h1 class="page-title">Теги и Категории</h1>
    <button class="btn btn-primary" data-action="open-tag-modal">
      ➕ Новый Тег
    </button>
  </div>

  <!-- Tag Cloud -->
  <div id="tag-cloud" class="tag-cloud">
    <!-- Динамически заполняется -->
  </div>

  <!-- Tag List -->
  <div id="tags-list" class="tag-list">
    <!-- Динамически заполняется -->
  </div>
</div>

<!-- Tag Modal -->
<div id="tag-modal" class="modal">
  <input type="text" id="tag-name" placeholder="Название тега">
  <textarea id="tag-description" placeholder="Описание (опционально)"></textarea>
  <button onclick="saveTag()">Сохранить</button>
</div>
```

```javascript
class TagManager {
  async loadTags() {
    const response = await fetch(`${API_URL}/api/tags`);
    const tags = await response.json();
    this.displayTags(tags);
  }

  displayTags(tags) {
    const html = tags.map(tag => `
      <div class="tag-item">
        <span class="tag-name">${tag.name}</span>
        <span class="tag-count">${tag.count}</span>
        <button onclick="deleteTag('${tag.id}')">🗑️</button>
      </div>
    `).join('');
    document.getElementById('tags-list').innerHTML = html;
  }

  async saveTag(tagData) {
    const response = await fetch(`${API_URL}/api/tags`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(tagData)
    });
    return response.json();
  }
}
```

### Файлы для создания/изменения
- `backend/app/api/routes.py` - добавить endpoints для тегов
- `frontend/js/tag-manager.js` (NEW)
- `frontend/css/tags.css` (NEW)

### Время реализации: 3-4 часа

---

## 📊 Task 4: Analytics Dashboard (3-4 часа)

### Концепция
- Статистика по использованию
- Графики по категориям
- Аналитика тегов
- Недавно использованные промпты
- Рейтинг популярности

### Архитектура

#### 4.1 Backend
```python
@router.get("/api/stats/overview")
def get_stats_overview(db: Session = Depends(get_db)):
    """Общая статистика"""
    return {
        "total_prompts": db.query(Prompt).count(),
        "total_categories": db.query(Category).count(),
        "total_tags": db.query(Tag).count(),
        "total_views": sum(p.views for p in db.query(Prompt).all())
    }

@router.get("/api/stats/by-category")
def get_stats_by_category(db: Session = Depends(get_db)):
    """Статистика по категориям"""
    return [
        {
            "category": c.name,
            "count": len(c.prompts),
            "percentage": (len(c.prompts) / db.query(Prompt).count()) * 100
        }
        for c in db.query(Category).all()
    ]

@router.get("/api/stats/trending")
def get_trending(db: Session = Depends(get_db)):
    """Популярные промпты"""
    prompts = db.query(Prompt).order_by(Prompt.views.desc()).limit(10).all()
    return prompts
```

#### 4.2 Frontend компоненты
```html
<!-- Dashboard с графиками -->
<div id="dashboard" class="page active">
  <div class="stats-overview">
    <div class="stat-card">
      <h3>Всего промптов</h3>
      <p id="stat-total-prompts" class="stat-value">0</p>
    </div>
    <!-- ... больше карточек -->
  </div>

  <!-- Графики (используем Chart.js или Recharts) -->
  <div class="charts-grid">
    <div id="category-chart" class="chart-container"></div>
    <div id="trending-chart" class="chart-container"></div>
  </div>
</div>
```

### Файлы для создания/изменения
- `backend/app/api/routes.py` - добавить stats endpoints
- `frontend/js/dashboard.js` (NEW)
- `frontend/css/dashboard.css` (NEW)
- Optional: добавить Chart.js в requirements

### Время реализации: 3-4 часа

---

## 📅 Timeline по задачам

```
Неделя 1 (текущая):
├─ Task 1: API Search Integration (2-3 часа)
└─ Task 2: Enhanced Editor (4-5 часов)
  Итого: 6-8 часов ✓

Неделя 2:
├─ Task 3: Tagging System (3-4 часа)
├─ Task 4: Analytics Dashboard (3-4 часа)
└─ Тестирование (2 часа)
  Итого: 8-10 часов

Неделя 3:
├─ Финальное тестирование (2-3 часа)
├─ Оптимизация производительности (2 часа)
├─ Сборка v2.0.1 EXE (1-2 часа)
└─ Развертывание (1 час)
  Итого: 6-8 часов
```

---

## ✅ Чек-лист Phase 3

### Завершено
- [x] Build & deployment система (5 скриптов)
- [x] Полная документация
- [x] **Исправлена адаптивность (layout-system.css)**
- [x] Frontend search UI

### В процессе
- [ ] Task 1: API Search Integration
- [ ] Task 2: Enhanced Editor
- [ ] Task 3: Tagging System
- [ ] Task 4: Analytics Dashboard

### Тестирование
- [ ] Unit тесты для API
- [ ] Integration тесты для frontend
- [ ] Manual тестирование на разных устройствах
- [ ] Performance тестирование

### Финализация
- [ ] Сборка Windows EXE v2.0.1
- [ ] Создание NSIS installer
- [ ] Документирование изменений
- [ ] Release notes

---

## 🔄 Как продолжить работу

### Шаг 1: Запустить приложение локально
```powershell
.\venv\Scripts\Activate.ps1
python start_v2.py
```

### Шаг 2: Проверить адаптивность
- Откройте DevTools (F12)
- Включите "Responsive Design Mode"
- Тестируйте разные размеры экрана

### Шаг 3: Начать с Task 1 (Search API)
- Измените `performSearch()` в `frontend/index.html`
- Подключитесь к `/api/prompts/search` endpoint
- Тестируйте в браузере

### Шаг 4: Двигайтесь по задачам последовательно
- Каждая задача заканчивается чистым состоянием
- Коммитьте после каждой завершённой задачи

---

## 📞 Вопросы и решения

### Q: Как быстро начать Task 1?
A: В файле `frontend/index.html` найдите функцию `performSearch()` (строка ~675). Она уже готова к подключению API.

### Q: Есть ли примеры для Task 2 (Editor)?
A: Да, примеры есть в этом документе выше. Используйте их как шаблон.

### Q: Где исходный код Backend API?
A: В `backend/app/api/routes.py`. Endpoints для поиска, проектов, тегов уже реализованы.

### Q: Как тестировать API?
A: Используйте встроенный Swagger UI: `http://127.0.0.1:8000/docs`

---

**Версия:** 2.0.1  
**Дата обновления:** 9 декабря 2025  
**Статус:** 🔄 ACTIVE DEVELOPMENT  
**Следующий milestone:** Task 1 completion (2-3 часа)

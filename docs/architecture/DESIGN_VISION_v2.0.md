# 🎨 PANDORA v2.0 - Complete Redesign Plan

## 📋 Философия Дизайна

### Визуальный стиль
- **Основа:** Минимализм с эклектичными деталями
- **Палитра:** 3 основных цвета с красивыми градиентами
- **Формы:** Мягкие закругленные углы, органичные кривые
- **Пространство:** Просторный, воздушный дизайн
- **Текстуры:** Glass morphism, neumorphism элементы, subsurface scattering

### Эстетика
- Гибрид 2D и 3D элементов
- Экспрессионизм + Футуризм + Гранж
- Технологичный мультяшный стиль
- Округлые, мягкие формы (ощущение безопасности)
- Чувство технологического прорыва

### Референсы
1. **Notion** - минимализм, модульность, чистота
2. **Perplexity** - гладкие анимации, градиенты, совремeнность
3. **Trello** - card-based UI, drag-and-drop
4. **ComfyUI** - граф-подобный интерфейс, node-based
5. **Blender** - профессиональный инструмент, много функций, но удобно
6. **Figma** - интерактивность, smooth transitions, collaborative feel

---

## 🎯 Фазы Развития

### ФАЗА 1: Foundation (v2.0.0) - 3-4 дня
1. Новая color palette и design tokens
2. Custom component library (buttons, cards, inputs)
3. Animation system
4. Typography system
5. Layout framework (grid, flex utilities)
6. Новая главная страница (dashboard)

### ФАЗА 2: Core UI (v2.1.0) - 3-4 дня
1. Переработка prompts page (cards, filters, search)
2. Категория система с красивыми табами
3. Модальные окна с new design
4. Sidebar navigation с иконками
5. Темная тема (auto-detect)
6. Responsive дизайн для мобильных

### ФАЗА 3: Advanced Features (v2.2.0) - 3-4 дня
1. Projects management переделка
2. Редактор промтов с syntax highlighting
3. AI assistant chat interface
4. Import/Export с визуализацией
5. Analytics dashboard
6. Keyboard shortcuts panel

### ФАЗА 4: Polish & Performance (v2.3.0) - 2-3 дня
1. Микроанимации и transitions
2. Loading states и skeletons
3. Error boundaries и nice error messages
4. Accessibility improvements (WCAG AA)
5. Performance optimization
6. Dark mode refinement

---

## 🎨 COLOR PALETTE

### Primary Colors (выберем из этих)
```
Option A (Modern Gradient):
- Primary: #6366F1 (Индиго)
- Secondary: #8B5CF6 (Фиолетовый)
- Accent: #EC4899 (Розовый)
- Neutral: #0F172A (Very Dark Blue)

Option B (Tech-Forward):
- Primary: #00D9FF (Киберпрозрачный)
- Secondary: #7C3AED (Глубокий фиолетовый)
- Accent: #FF006E (Хотпинк)
- Neutral: #1A1A2E (Темный)

Option C (Warm Futuristic):
- Primary: #FFB92C (Электрический золотой)
- Secondary: #FF006E (Маджента)
- Accent: #00F0FF (Киан)
- Neutral: #0A0E27 (Полночь)
```

### Выбираем Option A (классический, уверенный, профессиональный)

---

## 📐 TYPOGRAPHY

```
Заголовок (Display):
- Font: "Inter" или "Plus Jakarta Sans"
- Size: 48-64px
- Weight: 700
- Spacing: -2px

Заголовок (Large):
- Font: "Inter"
- Size: 32-40px
- Weight: 600
- Spacing: -1px

Заголовок (Medium):
- Font: "Inter"
- Size: 20-24px
- Weight: 600

Заголовок (Small):
- Font: "Inter"
- Size: 16-18px
- Weight: 600

Body (Large):
- Font: "Inter"
- Size: 16px
- Weight: 400
- Line-height: 1.6

Body (Regular):
- Font: "Inter"
- Size: 14px
- Weight: 400
- Line-height: 1.5

Body (Small):
- Font: "Inter"
- Size: 12px
- Weight: 400
- Line-height: 1.4

Code (Monospace):
- Font: "JetBrains Mono" или "Fira Code"
- Size: 12px
- Weight: 400

UI Labels:
- Font: "Inter"
- Size: 12px
- Weight: 500
- Transform: Uppercase
- Spacing: 1px
```

---

## 🎬 ANIMATION SYSTEM

### Timing Functions
```
Fast: cubic-bezier(0.16, 1, 0.3, 1) - 150ms
Standard: cubic-bezier(0.2, 0, 0, 1) - 250ms
Slow: cubic-bezier(0.33, 0, 0.66, 0) - 500ms
```

### Animation Types
1. **Entrance** - Fade in + Slide up (150ms)
2. **Exit** - Fade out + Slide down (100ms)
3. **Hover** - Scale + Color shift (200ms)
4. **Loading** - Smooth rotation or pulse (2s)
5. **Transitions** - Page transitions (300ms)
6. **Micro** - Button feedback (100ms)

---

## 🧩 COMPONENT LIBRARY

### Buttons
```
Primary: Solid gradient background
Secondary: Outlined
Tertiary: Ghost (text only)
Danger: Red accent
Sizes: Small, Medium, Large
States: Normal, Hover, Active, Disabled, Loading
```

### Cards
```
Style: Glass morphism with subtle shadow
Border: Subtle 1px rgba(255,255,255,0.1)
Padding: 24px
Border-radius: 16px
Backdrop-filter: blur(10px)
Background: rgba(15, 23, 42, 0.6)
```

### Inputs
```
Type: Text, Textarea, Select, Search
Style: Minimal with bottom border accent
Focus: Color shift + scale up slightly
Error: Red accent border + icon
Success: Green accent border + checkmark
```

### Tags/Badges
```
Style: Pill-shaped
Colors: By category (emoji + color)
Interactive: Clickable for filtering
```

### Modal/Dialog
```
Backdrop: Blur + dark overlay
Position: Center screen
Animation: Scale up + fade in
Size: Responsive (max 800px)
Close: X button + ESC key + click outside
```

---

## 📄 PAGE STRUCTURE

### Dashboard (Home)
```
Header:
- Logo + branding
- Search bar
- User menu (top-right)
- Theme toggle

Main Content:
- Welcome card with quick stats
- Recent prompts (horizontal scroll)
- Quick access categories
- Featured/trending prompts
- Analytics mini cards

Footer:
- Links + social
- Version info
```

### Prompts Library
```
Sidebar:
- Navigation
- Category filters (collapsible tree)
- Tag cloud
- Search by difficulty/model/etc

Main:
- Grid of prompt cards (3-4 columns responsive)
- Each card: title, description, category, difficulty, tags, actions
- Sort/filter controls at top
- Infinite scroll or pagination
- Empty state with illustration

Modal (on card click):
- Full prompt editor
- Metadata on side
- Auto-tagging suggestions
- Export/Copy buttons
- Related prompts
```

### Projects
```
Board view (like Trello):
- Columns: Todo, In Progress, Done
- Draggable cards
- Quick add button
- Category/filter tabs

Details modal:
- Files (tasks.txt, process.txt)
- Edit in modal (side-by-side)
- Auto-save indicator
- Share options
```

### Settings
```
Theme:
- Light / Dark / Auto

Appearance:
- Color scheme select
- Font size control
- Animation intensity
- Compact mode toggle

API:
- API key management
- Usage statistics
- Export data

About:
- Version info
- Changelog
- Credits
- Social links
```

---

## 🎨 DESIGN TOKENS (CSS Variables)

```css
/* Colors */
--color-primary: #6366F1
--color-secondary: #8B5CF6
--color-accent: #EC4899
--color-dark: #0F172A
--color-light: #F1F5F9

/* Gradients */
--gradient-primary: linear-gradient(135deg, #6366F1, #8B5CF6)
--gradient-accent: linear-gradient(135deg, #EC4899, #FF006E)
--gradient-warm: linear-gradient(135deg, #FFB92C, #EC4899)

/* Spacing */
--space-xs: 4px
--space-sm: 8px
--space-md: 16px
--space-lg: 24px
--space-xl: 32px
--space-2xl: 48px

/* Border radius */
--radius-sm: 8px
--radius-md: 12px
--radius-lg: 16px
--radius-full: 9999px

/* Typography */
--font-primary: 'Inter', sans-serif
--font-mono: 'JetBrains Mono', monospace

/* Shadows */
--shadow-sm: 0 1px 2px rgba(0,0,0,0.1)
--shadow-md: 0 4px 6px rgba(0,0,0,0.1)
--shadow-lg: 0 10px 15px rgba(0,0,0,0.1)
--shadow-xl: 0 20px 25px rgba(0,0,0,0.1)

/* Transitions */
--transition-fast: 150ms cubic-bezier(0.16, 1, 0.3, 1)
--transition-standard: 250ms cubic-bezier(0.2, 0, 0, 1)
--transition-slow: 500ms cubic-bezier(0.33, 0, 0.66, 0)
```

---

## 🗂️ Структура Файлов

```
frontend/
├── index.html (переделанный)
├── css/
│   ├── index.css (главный)
│   ├── design-tokens.css (переменные)
│   ├── components.css (компоненты)
│   ├── animations.css (анимации)
│   ├── responsive.css (медиа-запросы)
│   └── themes/
│       ├── light.css
│       └── dark.css
├── js/
│   ├── app.js (главный скрипт)
│   ├── components.js (компоненты)
│   ├── modals.js (модальные окна)
│   ├── api.js (API клиент)
│   ├── theme.js (тема переключатель)
│   ├── animations.js (анимации)
│   └── utils.js (утилиты)
└── images/
    ├── logo.svg
    ├── illustrations/
    └── icons/
```

---

## 🚀 Первый Шаг: Design Token System

Создаём универсальную систему токенов, которая позволит:
1. Быстро переключаться между темами
2. Сохранять консистентность дизайна
3. Легко обновлять стили глобально
4. Поддерживать темную/светлую тему

---

## ⏱️ Примерный Timeline

- **День 1-2:** Design tokens + Component library (buttons, cards, inputs)
- **День 3:** Dashboard redesign + Sidebar navigation
- **День 4:** Prompts page redesign
- **День 5:** Modals redesign + Animations
- **День 6:** Projects redesign
- **День 7:** Polish, Dark theme, Responsive
- **День 8:** Performance, Testing, Deployment

---

**Готово начинать? Начнём с самого фундамента - Design Token System!**

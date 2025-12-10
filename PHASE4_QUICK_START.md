# PANDORA v2.0 - Quick Integration Guide

## 🚀 Current Status

**Phase**: 4.1 Complete (Desktop & Bootstrap)
**Ready for**: Phase 4.2 (Frontend Views)
**ETA to v2.0**: 4-5 more hours

---

## ✅ What's Done

```
desktop/launcher.py   ✅ Daemon thread, graceful shutdown, FROZEN support
desktop/build.py      ✅ PyInstaller builder with checks
frontend/src/core/app.js      ✅ Bootstrap with router init
frontend/src/core/router.js   ✅ Hash-based router (existing)
```

**Critical Fix**: Infinite windows bug SOLVED via daemon thread architecture

---

## 🎯 What's Needed (Phase 4.2)

### 1. Views (Easy - Copy & Adapt Pattern)

**Pattern from existing Dashboard.js**:
```javascript
export default function PromptsView() {
    const container = document.createElement('div');
    container.className = 'prompts-view';
    
    // Create UI
    const header = document.createElement('div');
    header.className = 'view-header';
    header.innerHTML = '<h1>Prompts</h1>';
    
    // Fetch data
    window.http.get('/api/prompts?limit=50')
        .then(res => {
            // Render cards
        })
        .catch(err => console.error(err));
    
    container.appendChild(header);
    return container;
}
```

### 2. Add to frontend/src/views/:

**PromptsView.js** (150 lines)
- List layout with pagination
- Filter by category/tags
- Search box
- GlassCard for each prompt
- Context menu (edit, delete, duplicate)
- Empty state

**ProjectsView.js** (120 lines)
- Grid layout
- Create/Edit/Delete project
- Link prompts to projects
- Progress indicator
- Quick stats

**EditorView.js** (80 lines)
- Wrapper for PromptEditor component
- Save to /api/prompts
- Auto-save on interval
- Loading states

**AnalyticsView.js** (100 lines)
- Stats from /api/analytics/dashboard
- Simple charts (or text summary)
- Insights from /api/analytics/insights

---

## 📋 Checklist for Phase 4.2

```markdown
## Views Creation
- [ ] frontend/src/views/PromptsView.js
- [ ] frontend/src/views/ProjectsView.js
- [ ] frontend/src/views/EditorView.js
- [ ] frontend/src/views/AnalyticsView.js

## Styling
- [ ] frontend/src/styles/design-system/tokens.css
- [ ] frontend/src/styles/design-system/animations.css
- [ ] frontend/src/styles/design-system/utilities.css
- [ ] frontend/src/styles/components/*.css
- [ ] frontend/src/styles/views/*.css

## HTML & Config
- [ ] frontend/index.html
- [ ] frontend/package.json (if using Vite)
- [ ] frontend/vite.config.js (if using Vite)

## Testing
- [ ] Run: python start.py
- [ ] Verify all routes work
- [ ] Check API calls
- [ ] Test graceful shutdown
- [ ] Build: python desktop/build.py
- [ ] Run EXE on clean VM

## Documentation
- [ ] Update README.md
- [ ] Update CHANGELOG.md
- [ ] Create RELEASE_NOTES.md
- [ ] Commit with message
- [ ] Tag v2.0.0
```

---

## 🔧 Development Workflow

### Start Session
```bash
cd g:\CODING\PANDORA_FOR_PROMPTS\PANDORA_FOR_PROMPTS-main

# Activate virtual environment
python -m venv venv
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start dev server
python start.py
```

### Test in Browser
```
http://127.0.0.1:8000/   (Backend serves frontend)
Ctrl+K                   (Command palette)
#/dashboard              (Manual navigation)
```

### Build EXE
```bash
python desktop/build.py
# Creates dist/PANDORA/ and PANDORA_v2.0.exe
```

### Git Workflow
```bash
# Work on feature
# Test everything
git add -A
git commit -m "feat: View integration for v2.0"
git push
```

---

## 📂 File Structure Reference

```
frontend/
├── index.html                    (entry point)
├── src/
│   ├── core/
│   │   ├── app.js              (bootstrap) ✅
│   │   ├── router.js           (router) ✅
│   │   ├── state-manager.js    (state) ✅
│   │   └── http-client.js      (http) ✅
│   ├── views/
│   │   ├── Dashboard.js        (analytics) ✅
│   │   ├── PromptsView.js      ⏳
│   │   ├── ProjectsView.js     ⏳
│   │   ├── EditorView.js       ⏳
│   │   └── AnalyticsView.js    ⏳
│   ├── components/
│   │   ├── base/
│   │   │   ├── Card.js         (GlassCard) ✅
│   │   │   └── ...
│   │   └── prompt/
│   │       └── PromptEditor.js ✅
│   ├── styles/
│   │   ├── design-system/
│   │   │   ├── tokens.css      ✅
│   │   │   ├── animations.css  ✅
│   │   │   └── utilities.css   ⏳
│   │   ├── components/         ⏳
│   │   └── views/              ⏳
│   └── utils/
│       ├── http.js             ✅
│       ├── animated-background.js ✅
│       └── state-manager.js    ✅
├── dist/                        (build output)
├── package.json                 ⏳
└── vite.config.js              ⏳
```

---

## 🎨 CSS Architecture

All CSS uses design tokens from `tokens.css`:

```css
/* frontend/src/styles/design-system/tokens.css */
:root {
  --font-sans: 'Inter', system-ui;
  --font-mono: 'JetBrains Mono', monospace;
  --bg-app: #0a0a0f;
  --bg-surface: #13131a;
  --brand-primary: #8b5cf6;
  --space-4: 1rem;
  --radius-xl: 1rem;
  --transition-base: 250ms cubic-bezier(0.4, 0, 0.2, 1);
}

/* Usage everywhere */
.prompt-card {
  background: var(--bg-surface);
  padding: var(--space-4);
  border-radius: var(--radius-xl);
  transition: all var(--transition-base);
}
```

---

## 🔗 API Endpoints Reference

```
GET  /api/prompts?skip=0&limit=50&category=&tags=[]&search=&sort_by=created_at&order=desc
POST /api/prompts
GET  /api/prompts/{id}
PUT  /api/prompts/{id}
DELETE /api/prompts/{id}
POST /api/prompts/search
POST /api/prompts/{id}/duplicate
POST /api/prompts/{id}/favorite
GET  /api/prompts/{id}/versions
POST /api/prompts/{id}/optimize

GET  /api/projects
POST /api/projects
GET  /api/projects/{id}
PUT  /api/projects/{id}
DELETE /api/projects/{id}

GET  /api/analytics/dashboard
GET  /api/analytics/insights
```

---

## 🚨 Common Pitfalls to Avoid

```javascript
❌ DON'T:
- Forget to export default function
- Use require() instead of import/export
- Block the main thread (no while loops!)
- Create multiple router instances
- Forget error handling in fetch

✅ DO:
- Use async/await for API calls
- Check window.http before using
- Handle loading states
- Use CSS variables from tokens.css
- Test navigation between views
```

---

## 📞 Quick Help

### Router navigation
```javascript
window.router.navigate('/prompts');
```

### API call
```javascript
try {
    const res = await window.http.get('/api/prompts');
    console.log(res.data);
} catch (error) {
    console.error('API error:', error);
}
```

### Create card
```javascript
const card = new GlassCard({ variant: 'elevated', glow: true });
const el = card.create({
    header: 'Title',
    body: 'Content',
    footer: 'Action'
});
container.appendChild(el);
```

### State observation
```javascript
window.appState.observe('prompts', (newVal, oldVal) => {
    console.log('Prompts changed:', newVal);
    // Update UI
});
```

---

## ⏱️ Time Estimates

| Task | Time | Difficulty |
|------|------|------------|
| PromptsView.js | 45 min | Easy |
| ProjectsView.js | 45 min | Easy |
| EditorView.js | 30 min | Easy |
| AnalyticsView.js | 60 min | Medium |
| Styling (all) | 90 min | Medium |
| HTML + Config | 30 min | Easy |
| Testing | 45 min | Easy |
| Docs + Commit | 30 min | Easy |
| **TOTAL** | **5.5 hours** | - |

---

## 🎯 Success Indicators

By end of next session:
- ✅ All 4 views created and tested
- ✅ Styling complete and consistent
- ✅ `python start.py` works perfectly
- ✅ All routes navigate smoothly
- ✅ `python desktop/build.py` succeeds
- ✅ EXE runs on clean Windows 11 VM
- ✅ v2.0.0 tagged on GitHub

---

**Good luck! 🚀 You've got this!**

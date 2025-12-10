---
title: "PANDORA - Quick Start Guide"
---

# 🚀 PANDORA Desktop Application - Quick Start

## ⚡ Fastest Way to Run

### Step 1: Build (One-time)
```bash
cd G:\CODING\PANDORA_FOR_PROMPTS\PANDORA_FOR_PROMPTS-main
python build.py
```
**Wait:** 2-3 minutes for PyInstaller to compile

### Step 2: Run
**Option A - Direct Double-Click:**
1. Open `dist/PANDORA/` folder
2. Double-click `PANDORA.exe`
3. Wait 3-5 seconds for startup
4. Beautiful UI appears! 🎉

**Option B - Command Line:**
```bash
dist\PANDORA\PANDORA.exe
```

---

## ✅ What Should Happen

### Startup Sequence
1. **Console Output** (if running from terminal):
   ```
   [timestamp] INFO: ======================================================================
   [timestamp] INFO: PANDORA - Professional Prompt Management System
   [timestamp] INFO: ⬇️ Initializing PANDORA Backend...
   [timestamp] INFO: ⏳ Waiting for backend to be ready...
   [timestamp] INFO: Starting FastAPI Backend in main process...
   [timestamp] INFO: ✓ Backend is ready at http://127.0.0.1:8000
   [timestamp] INFO: 🪟 Creating application window...
   [timestamp] INFO: ✓ Application window created
   [timestamp] INFO: 📍 Frontend: http://127.0.0.1:8000/
   ```

2. **Window Opens:**
   - Embedded PyWebView browser appears
   - Shows PANDORA dashboard
   - Beautiful gradient UI with sidebar
   - Status shows: ✓ Backend Running, ✓ Database Connected, ✓ API Available

3. **Ready to Use:**
   - Navigate with sidebar menu
   - Click "Create New Prompt"
   - Access API docs: `/docs` link
   - Manage projects and prompts

---

## 🎨 UI Overview

### Dashboard Features
```
┌─ Navigation Bar ─────────────────────────────┐
│ 🚀 PANDORA  |  Prompts  Projects  API Docs  │
└──────────────────────────────────────────────┘
┌─ Sidebar ──────────────────────────────────┐
│ • Dashboard                                 │
│ • ➕ Create Prompt                          │
│ • 📁 My Projects                            │
│ • 🏷️ Tags                                   │
│ • ⭐ Favorites                              │
│ • 🆕 Recent                                 │
└────────────────────────────────────────────┘
┌─ Main Content ─────────────────────────────┐
│                                             │
│ Welcome to PANDORA 🎉                       │
│ Professional Prompt Management System       │
│                                             │
│ System Status: [🟢 All Systems Running]    │
│                                             │
│ Key Features:                               │
│ 📝 Prompt Management  🏷️ Auto-Tagging     │
│ 📊 Project Tracking   🔍 Advanced Search   │
│ 📚 API Integration    🔄 Real-time Sync    │
│                                             │
│ [➕ Create New Prompt]  [📚 View Docs]    │
│                                             │
└────────────────────────────────────────────┘
```

### Sidebar Navigation
- **Dashboard** - Main overview
- **Create Prompt** - Add new prompts
- **My Projects** - Project management
- **Tags** - Organize by tags
- **Favorites** - Quick access
- **Recent** - Recently used
- **Settings** - Configuration
- **Documentation** - Help
- **About** - App info

---

## 🔌 API Access

### While Application is Running

**Web UI:**
- Main: http://127.0.0.1:8000/
- API Docs: http://127.0.0.1:8000/docs (interactive)
- OpenAPI JSON: http://127.0.0.1:8000/openapi.json

**API Base URL:**
```
http://127.0.0.1:8000/api/v1/
```

**Example API Calls:**
```bash
# Get all prompts
curl http://127.0.0.1:8000/api/v1/prompts

# Create new prompt
curl -X POST http://127.0.0.1:8000/api/v1/prompts \
  -H "Content-Type: application/json" \
  -d '{"title": "My Prompt", "content": "..."}'

# Get projects
curl http://127.0.0.1:8000/api/v1/projects
```

---

## ⚙️ System Requirements

- **OS:** Windows 10 or later (Windows 11 recommended)
- **RAM:** 512 MB minimum (1 GB recommended)
- **Disk:** 300 MB for application
- **Port:** 8000 must be available
- **No additional software needed!**

---

## ❌ Troubleshooting

### Issue: "Port 8000 is already in use"
**Solution:**
```bash
# Find what's using port 8000
netstat -ano | findstr :8000

# Kill the process (replace PID)
taskkill /PID <PID> /F
```

### Issue: "Window doesn't appear"
**Solution:**
1. Check if process is running: `tasklist | findstr PANDORA`
2. Try from terminal to see error: `dist\PANDORA\PANDORA.exe`
3. Ensure PyWebView is installed: `pip install pywebview`

### Issue: "ModuleNotFoundError" or import errors
**Solution:**
- Rebuild: `python build.py`
- Clean and rebuild: 
  ```bash
  rm -r dist build PANDORA.spec
  python build.py
  ```

### Issue: Application closes immediately
**Solution:**
1. Run from terminal to see error messages
2. Check that all dependencies are in venv
3. Try fresh rebuild

---

## 📋 First-Time Setup Checklist

- [ ] Clone/download repository
- [ ] Ensure Python 3.10+ is installed
- [ ] Create virtual environment (venv) - done during build
- [ ] Run `python build.py` once
- [ ] Keep `dist/PANDORA/` folder
- [ ] Can run `PANDORA.exe` multiple times after that
- [ ] Port 8000 is available

---

## 🎯 Key Directories

```
PANDORA_FOR_PROMPTS/
├── dist/PANDORA/PANDORA.exe          👈 RUN THIS
├── backend/                            (API + Database)
├── frontend/                           (HTML UI)
├── build.py                            (Build script)
└── launcher_final.py                   (Main launcher)
```

---

## 🔄 Development Workflow

### Modify Backend
1. Edit `backend/app/` files
2. Run `python build.py` to rebuild exe
3. Test the new exe

### Modify Frontend (HTML)
1. Edit `frontend/index.html`
2. Run `python build.py` to rebuild exe
3. Test in the new exe

### Build & Test
```bash
# Full rebuild
python build.py

# Run exe
dist\PANDORA\PANDORA.exe

# Or double-click in explorer
# dist/PANDORA/PANDORA.exe
```

---

## 📊 Performance Tips

- **First Launch:** Might take 5+ seconds (loads all modules)
- **Subsequent Launches:** 3-4 seconds (cached)
- **Memory:** ~150 MB typical usage
- **CPU:** Minimal when idle

---

## 📞 Support

### Getting Help
1. **API Documentation:** http://127.0.0.1:8000/docs
2. **Terminal Output:** Look for [ERROR] or [WARNING] messages
3. **Project Files:** Check `BUGFIX_v1_0_3.md` for technical details

### Reporting Issues
Include:
- Error message or screenshot
- What OS and version
- Terminal output if available
- What you were trying to do

---

## 🎉 You're All Set!

**PANDORA is ready to use!**

- ✅ No infinite loops
- ✅ Beautiful modern UI
- ✅ Full API backend
- ✅ Professional desktop app
- ✅ Windows 11 compatible

**Enjoy! 🚀**

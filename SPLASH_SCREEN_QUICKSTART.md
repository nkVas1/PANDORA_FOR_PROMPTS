# 🎨 PANDORA v2.0.1 - Splash Screen Quick Start

## What's New? 🆕

**Launcher v4 with Professional Splash Screen:**
- 🎨 Beautiful dark-themed loading screen
- 📊 Real-time progress bar
- 📝 Live log output with color coding
- ✨ Smooth animations
- 🔧 Full backend integration

---

## Quick Start (2 minutes)

### 1. Install Dependencies
```bash
cd backend
pip install -r requirements.txt
cd ..

cd frontend
npm install
cd ..
```

### 2. Run Development Mode
```bash
python start_dev.py
```

### What You'll See
```
╔════════════════════════════════════════╗
║  PANDORA v2.0                          ║
║  Professional Prompt Manager           ║
║                                        ║
║  ████████████░░░░░░░░░░░░░░░░  50%    ║
║                                        ║
║  [✓] Starting Backend Server            ║
║  [▶] Loading Frontend                   ║
║  [ ] Creating Window                    ║
║                                        ║
║  Initializing API and loading prompts   ║
╚════════════════════════════════════════╝
```

### 3. Wait for "Application Ready"
- Splash will automatically close
- Main window will appear
- Ready to use!

---

## Features

### Splash Screen Progress
| Step | Duration | Status |
|------|----------|--------|
| Starting Backend | 3-5s | Loading prompts from database |
| Loading Frontend | 1-2s | Preparing UI |
| Creating Window | 0.5s | Launching main window |
| **Total** | **5-10s** | **Ready!** |

### Log Messages
- ✓ **Green** - Success messages
- 📝 **Blue** - Info messages
- ⚠️ **Yellow** - Warnings
- ✗ **Red** - Errors
- ▶️ **Cyan** - Step transitions

### Error Handling
If anything goes wrong:
- ✅ Error shown in splash screen
- ✅ Fallback to no-splash mode
- ✅ Detailed logs in console
- ✅ Application still starts

---

## Commands

### Start Development
```bash
# With splash screen
python start_dev.py

# Or direct launcher
python desktop/launcher.py
```

### Build EXE (Future)
```bash
# Will include splash screen in exe
python desktop/build_exe_final.py
```

### Test Splash Screen Only
```python
python -c "
from desktop.splash_screen_pro import create_splash_and_manager

splash, manager = create_splash_and_manager()
splash.show()

manager.add_step('Test 1', 'Description')
manager.add_step('Test 2', 'Description')

manager.step(0, 'Test 1', 'Running...')
manager.log_success('Test 1 passed!')

manager.step(1, 'Test 2', 'Running...')
manager.log_warning('Test 2 has a warning')

import time
time.sleep(5)
splash.close()
"
```

---

## Troubleshooting

### Splash Doesn't Appear
**Solution:**
```bash
# Check module exists
python -c "from desktop.splash_screen_pro import create_splash_and_manager; print('OK')"

# If error, reinstall desktop requirements
pip install -r backend/requirements.txt
```

### Logs Not Showing
**Solution:**
```bash
# Check that backend is passing manager
# In launcher.py, verify:
launcher = AppLauncher(_splash, _manager)  # ✓ Correct

# Not:
launcher = AppLauncher()  # ✗ Wrong - no manager
```

### Backend Connection Refused
**Solution:**
```bash
# Check port 8000 is free
netstat -an | findstr :8000  # Windows
lsof -i :8000              # macOS/Linux

# If occupied, kill the process or use different port
# In launcher.py change:
BACKEND_PORT = 9000  # Instead of 8000
```

---

## Customization

### Change Splash Colors
Edit `desktop/splash_screen_pro.py`:
```python
DARK_BG = "#1a1a2e"      # Change background
ACCENT_COLOR = "#6366f1" # Change accent
```

### Change Splash Size
```python
WINDOW_WIDTH = 500   # Width
WINDOW_HEIGHT = 400  # Height
```

### Add Custom Steps
In `main()` function of launcher.py:
```python
_manager.add_step("Custom Step", "Your description here")
# Will appear in splash screen order
```

### Custom Log Messages
In any launcher method:
```python
self._log("Your message", "info")      # Blue
self._log("Success!", "success")       # Green
self._log("Warning!", "warning")       # Yellow
self._log("Error!", "error")           # Red
```

---

## Architecture

### How It Works

```
User clicks PANDORA.exe
        ↓
   main() starts
        ↓
   Splash screen appears (Tkinter window)
        ↓
   Backend starts in daemon thread
   (Splash shows progress: 0% → 33%)
        ↓
   Frontend loads
   (Splash shows progress: 33% → 66%)
        ↓
   PyWebView window created
   (Splash shows progress: 66% → 100%)
        ↓
   Splash closes automatically
        ↓
   Main application window shows
        ↓
   Ready to use!
```

### Process Diagram

```
main()
  ├─→ Splash Screen (Tkinter)
  │   └─ Progress: 0% → 100%
  │
  ├─→ App Launcher
  │   ├─→ Backend Thread (FastAPI)
  │   │   └─ Splash: 0% → 33%
  │   │
  │   ├─→ Frontend Loading
  │   │   └─ Splash: 33% → 66%
  │   │
  │   └─→ PyWebView Window
  │       └─ Splash: 66% → 100%
  │
  ├─→ Splash Closes
  │
  └─→ UI Event Loop (PyWebView)
```

---

## Performance

### Startup Times
- Python initialization: ~0.5s
- Splash screen: ~0.3s
- Backend startup: ~3-5s
- Frontend load: ~1-2s
- UI render: ~0.5s
- **Total: 5-10 seconds**

### Resource Usage
- RAM: ~150-200 MB
- CPU: ~30-50% (during startup)
- Disk: 39.6 MB (exe)

---

## Next Steps

1. ✅ Try running `python start_dev.py`
2. ✅ See the splash screen appear
3. ✅ Watch the progress bar
4. ✅ Read the log messages
5. ✅ Use PANDORA normally

---

## Questions?

Check these files:
- 📖 `docs/LAUNCHER_v4_SPLASH_SCREEN.md` - Full documentation
- 🔧 `docs/LAUNCHER_v4_IMPLEMENTATION_REPORT.md` - Technical details
- 🚀 `QUICK_START.md` - General quick start

---

**PANDORA v2.0.1 - Now with Professional Splash Screen!** ✨

*Made with ❤️ for productivity*

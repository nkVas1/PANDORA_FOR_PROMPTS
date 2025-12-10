#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PANDORA v2.0 - Quick Start & Test Script
Быстрый запуск приложения для разработки и тестирования
"""

import os
import sys
import subprocess
import webbrowser
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent
BACKEND_DIR = PROJECT_ROOT / "backend"
DESKTOP_DIR = PROJECT_ROOT / "desktop"
FRONTEND_DIR = PROJECT_ROOT / "frontend"

def print_banner():
    print("\n" + "=" * 70)
    print("  PANDORA v2.0 - Development Mode")
    print("=" * 70)
    print()

def print_section(title):
    print(f"\n[STEP] {title}")
    print("-" * 70)

def print_info(msg):
    print(f"  ℹ️  {msg}")

def print_success(msg):
    print(f"  ✅ {msg}")

def print_error(msg):
    print(f"  ❌ {msg}")

def check_python():
    print_section("Checking Python Version")
    version = sys.version.split()[0]
    print_info(f"Python {version}")
    if int(sys.version_info.major) < 3 or int(sys.version_info.minor) < 10:
        print_error("Python 3.10+ required!")
        return False
    print_success("Python version OK")
    return True

def check_dependencies():
    print_section("Checking Dependencies")
    
    required = {
        'fastapi': 'FastAPI',
        'uvicorn': 'Uvicorn',
        'sqlalchemy': 'SQLAlchemy',
        'pydantic': 'Pydantic',
        'openai': 'OpenAI API',
    }
    
    missing = []
    for module, name in required.items():
        try:
            __import__(module)
            print_success(f"{name} installed")
        except ImportError:
            print_error(f"{name} NOT installed")
            missing.append(module)
    
    if missing:
        print(f"\n  Install missing packages:")
        print(f"  pip install {' '.join(missing)}")
        return False
    
    return True

def check_files():
    print_section("Checking Project Files")
    
    files_to_check = {
        'backend/app/main.py': 'Backend main file',
        'backend/app/db/models.py': 'Database models',
        'frontend/index.html': 'Frontend entry',
        'frontend/src/core/app.js': 'Frontend app.js',
        'desktop/launcher.py': 'Desktop launcher',
        'desktop/splash_screen_v3.py': 'Splash screen',
    }
    
    missing = []
    for path, desc in files_to_check.items():
        full_path = PROJECT_ROOT / path
        if full_path.exists():
            print_success(f"{desc} → {path}")
        else:
            print_error(f"{desc} → {path}")
            missing.append(path)
    
    return len(missing) == 0

def run_launcher():
    print_section("Starting PANDORA Desktop Application")
    
    launcher = DESKTOP_DIR / "launcher.py"
    print_info(f"Running: {launcher}")
    
    try:
        subprocess.run([
            sys.executable,
            str(launcher)
        ], cwd=str(DESKTOP_DIR))
    except KeyboardInterrupt:
        print_info("Application closed")
        return True
    except Exception as e:
        print_error(f"Failed to run launcher: {e}")
        return False
    
    return True

def run_backend_only():
    print_section("Starting Backend Only (Uvicorn)")
    
    print_info("Backend running at http://127.0.0.1:8000")
    print_info("API docs at http://127.0.0.1:8000/docs")
    print_info("Press Ctrl+C to stop")
    
    try:
        subprocess.run([
            sys.executable, '-m', 'uvicorn',
            'app.main:app',
            '--reload',
            '--host', '127.0.0.1',
            '--port', '8000'
        ], cwd=str(BACKEND_DIR))
    except KeyboardInterrupt:
        print_info("Backend stopped")
        return True
    except Exception as e:
        print_error(f"Failed to start backend: {e}")
        return False
    
    return True

def run_frontend_dev():
    print_section("Starting Frontend Dev Server")
    
    print_info("Frontend running at http://127.0.0.1:8080")
    print_info("Press Ctrl+C to stop")
    
    try:
        subprocess.run([
            sys.executable, '-m', 'http.server',
            '8080',
            '--bind', '127.0.0.1'
        ], cwd=str(FRONTEND_DIR))
    except KeyboardInterrupt:
        print_info("Frontend server stopped")
        return True
    except Exception as e:
        print_error(f"Failed to start frontend server: {e}")
        return False
    
    return True

def main():
    print_banner()
    
    # Check environment
    if not check_python():
        return 1
    
    if not check_files():
        print_error("Some required files are missing!")
        return 1
    
    if not check_dependencies():
        print_error("Some dependencies are missing!")
        print_info("Install dependencies:")
        print("  pip install -r backend/requirements.txt")
        return 1
    
    print_section("Choose Mode")
    print("""
  1. Full App (Desktop with Splash Screen)
  2. Backend Only (Uvicorn)
  3. Frontend Only (HTTP Server)
  4. Exit
    """)
    
    choice = input("Enter choice (1-4): ").strip()
    
    if choice == '1':
        return 0 if run_launcher() else 1
    elif choice == '2':
        return 0 if run_backend_only() else 1
    elif choice == '3':
        return 0 if run_frontend_dev() else 1
    elif choice == '4':
        print("Goodbye!")
        return 0
    else:
        print_error("Invalid choice")
        return 1

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\nInterrupted")
        sys.exit(0)

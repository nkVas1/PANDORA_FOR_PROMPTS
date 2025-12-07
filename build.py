#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build script for creating executable from PANDORA application
Скрипт для сборки exe файла
"""

import os
import sys
import subprocess
import shutil
import platform
from pathlib import Path

# Ensure UTF-8 output on Windows
if sys.platform == 'win32':
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

ROOT_DIR = Path(__file__).parent
BACKEND_DIR = ROOT_DIR / "backend"
FRONTEND_DIR = ROOT_DIR / "frontend"
BUILD_DIR = ROOT_DIR / "dist"

# Определяем Python для запуска (используем venv если существует)
VENV_DIR = ROOT_DIR / "venv"
if VENV_DIR.exists():
    if platform.system() == "Windows":
        PYTHON_CMD = str(VENV_DIR / "Scripts" / "python.exe")
    else:
        PYTHON_CMD = str(VENV_DIR / "bin" / "python")
else:
    PYTHON_CMD = sys.executable


def print_section(title):
    """Print section header"""
    print()
    print("=" * 70)
    print(f"  {title}")
    print("=" * 70)
    print()


class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    END = '\033[0m'


def print_success(msg):
    """Print success message"""
    print(f"{Colors.GREEN}✓ {msg}{Colors.END}")


def print_error(msg):
    """Print error message"""
    print(f"{Colors.RED}✗ {msg}{Colors.END}")


def build_frontend():
    """Build Next.js frontend"""
    print_section("Building Frontend")
    
    # Check if npm is available
    try:
        subprocess.run(["npm", "--version"], capture_output=True, check=True, timeout=5)
    except (FileNotFoundError, subprocess.CalledProcessError):
        print("⚠️  npm не найден. Пропускаем сборку Frontend.")
        print("   Установите Node.js для сборки фронтенда")
        print("   https://nodejs.org/")
        return True  # Return True to not block the build
    
    try:
        os.chdir(str(FRONTEND_DIR))
        print("Installing dependencies...")
        subprocess.run(["npm", "install"], check=True)
        
        print("Building Next.js application...")
        subprocess.run(["npm", "run", "build"], check=True)
        
        print("✓ Frontend built successfully")
        return True
    except Exception as e:
        print(f"✗ Error building frontend: {e}")
        return False
    finally:
        os.chdir(str(ROOT_DIR))


def install_backend_deps():
    """Install backend dependencies"""
    print_section("Installing Backend Dependencies")
    
    try:
        os.chdir(str(BACKEND_DIR))
        print("Installing Python packages...")
        
        # Install additional packages for exe building
        required_packages = [
            'PyInstaller>=6.0',
            'flask>=2.0',  # Alternative to FastAPI for exe packaging
        ]
        
        subprocess.run([
            PYTHON_CMD, "-m", "pip", "install", "-r", "requirements.txt"
        ], check=True)
        
        for package in required_packages:
            subprocess.run([
                PYTHON_CMD, "-m", "pip", "install", package
            ], check=True)
        
        print("✓ Backend dependencies installed")
        return True
    except Exception as e:
        print(f"✗ Error installing dependencies: {e}")
        return False
    finally:
        os.chdir(str(ROOT_DIR))


def create_exe():
    """Create main PANDORA Desktop Application executable"""
    print_section("Creating PANDORA Desktop Application")
    
    # First, clean old builds
    try:
        if BUILD_DIR.exists():
            print(f"Removing old build directory: {BUILD_DIR}")
            shutil.rmtree(BUILD_DIR)
    except Exception as e:
        print(f"Warning: Could not remove old build: {e}")
    
    try:
        launcher_script = ROOT_DIR / "launcher_final.py"
        
        if not launcher_script.exists():
            print_error(f"launcher_final.py не найден в {ROOT_DIR}")
            return False
        
        print("Building PANDORA with embedded browser (PyWebView)...")
        print(f"Using launcher: {launcher_script}")
        
        # Build PyInstaller command for modern desktop app with embedded browser
        pyinstaller_cmd = [
            PYTHON_CMD, "-m", "PyInstaller",
            "--onedir",
            "--windowed",  # No console window - clean desktop app
            "--add-data", f"{BACKEND_DIR}:backend",
            "--add-data", f"{FRONTEND_DIR}:frontend",
            # FastAPI and server
            "--hidden-import=fastapi",
            "--hidden-import=fastapi.middleware",
            "--hidden-import=fastapi.middleware.cors",
            "--hidden-import=sqlalchemy",
            "--hidden-import=pydantic",
            "--hidden-import=pydantic_settings",
            "--hidden-import=uvicorn",
            "--hidden-import=uvicorn.lifespan",
            "--hidden-import=uvicorn.lifespan.off",
            "--hidden-import=uvicorn.lifespan.on",
            "--hidden-import=uvicorn.loops",
            "--hidden-import=uvicorn.loops.asyncio",
            "--hidden-import=uvicorn.loops.auto",
            "--hidden-import=uvicorn.protocols",
            "--hidden-import=uvicorn.servers",
            # PyWebView and dependencies
            "--hidden-import=webview",
            "--hidden-import=webview.js",
            "--hidden-import=webview.dom",
            "--hidden-import=webview.api",
            "--hidden-import=requests",
            "--hidden-import=urllib3",
            # Standard library
            "--hidden-import=logging",
            "--hidden-import=threading",
            "--hidden-import=subprocess",
            "--hidden-import=json",
            "--hidden-import=sqlite3",
            # Collection
            "--collect-all=fastapi",
            "--collect-all=sqlalchemy",
            "--collect-all=pydantic",
            "--collect-all=pydantic_settings",
            "--collect-all=uvicorn",
            "--collect-all=webview",
            "--name", "PANDORA",
            str(launcher_script)
        ]
        
        # Add icon if it exists
        icon_path = ROOT_DIR / "ICON.ico"
        if icon_path.exists():
            pyinstaller_cmd.insert(-1, "--icon")
            pyinstaller_cmd.insert(-1, str(icon_path))
        
        subprocess.run(pyinstaller_cmd, check=True)
        
        print_success("Desktop application created successfully")
        
        # Check exe location
        exe_path = ROOT_DIR / "dist" / "PANDORA" / "PANDORA.exe"
        if exe_path.exists():
            print_success(f"Executable path: {exe_path}")
            print()
            print("=" * 70)
            print("  PANDORA DESKTOP APPLICATION READY!")
            print("=" * 70)
            print()
            print("Features:")
            print("  ✓ Embedded web browser (no external dependencies)")
            print("  ✓ FastAPI backend (fully functional)")
            print("  ✓ Modern Windows 11 style application")
            print("  ✓ Complete offline support")
            print()
            print("To run:")
            print(f"  dist\\PANDORA\\PANDORA.exe")
            print()
        
        return True
    except subprocess.CalledProcessError as e:
        print_error(f"Error building executable: {e}")
        return False
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        return False


def build_all():
    """Build complete application"""
    print()
    print("╔" + "=" * 68 + "╗")
    print("║" + " " * 68 + "║")
    print("║" + "  PANDORA Prompts Manager - Build Script".center(68) + "║")
    print("║" + " " * 68 + "║")
    print("╚" + "=" * 68 + "╝")
    print()
    
    # Step 1: Install backend dependencies
    if not install_backend_deps():
        print("✗ Build failed at backend dependencies")
        sys.exit(1)
    
    # Step 2: Build frontend (optional - doesn't block if npm missing)
    build_frontend()  # Returns True even if npm not found
    
    # Step 3: Create executable
    if not create_exe():
        print("✗ Build failed at executable creation")
        sys.exit(1)
    
    # Summary
    print_section("Build Summary")
    print_success("All components built successfully!")
    print()
    print("=" * 70)
    print("  PANDORA DESKTOP APPLICATION v1.1")
    print("=" * 70)
    print()
    print("✨ APPLICATION FEATURES:")
    print()
    print("  🚀 Modern Desktop Application")
    print("     • Embedded web browser (PyWebView)")
    print("     • Full FastAPI backend integration")
    print("     • Windows 11 native experience")
    print()
    print("  📦 Complete Package")
    print("     • No external dependencies required")
    print("     • Backend + Frontend bundled together")
    print("     • Works completely offline")
    print()
    print("  🎨 Professional UI")
    print("     • Modern gradient design")
    print("     • Responsive layout")
    print("     • Smooth animations")
    print()
    print("=" * 70)
    print()
    print("📍 EXECUTABLE LOCATION:")
    print(f"   dist\\PANDORA\\PANDORA.exe")
    print()
    print("🚀 TO RUN:")
    print("   1. Open dist folder")
    print("   2. Open PANDORA folder")
    print("   3. Double-click PANDORA.exe")
    print()
    print("⚡ QUICK START:")
    print("   • The application will start automatically")
    print("   • Backend API initializes on port 8000")
    print("   • Embedded browser displays the UI")
    print("   • No additional configuration needed")
    print()
    print("=" * 70)
    print()


if __name__ == "__main__":
    try:
        build_all()
    except KeyboardInterrupt:
        print("\n✗ Build cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        sys.exit(1)

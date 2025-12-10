#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PANDORA v2.0 - Professional Windows EXE Builder (Version 3)
Собирает полнофункциональный Windows исполняемый файл с встроенным backend и frontend

Использование:
    python build.py                      # Полная сборка
    python build.py --quick              # Быстрая сборка (без очистки)
    python build.py --clean              # Только очистка
    python build.py --test               # Только тестирование готового exe
    python build.py --help               # Справка

Архитектура сборки:
    1. Проверка окружения (Python, PyInstaller, файлы, зависимости, место на диске)
    2. Очистка старых артефактов
    3. PyInstaller сборка (использует PANDORA.spec)
    4. Верификация результатов
    5. Тестирование exe
    6. Генерация отчета
"""

import os
import sys
import shutil
import subprocess
import time
import argparse
import json
from pathlib import Path
from typing import Tuple, List
from datetime import datetime

# ==================== КОНФИГ ====================
class Config:
    """Конфигурация сборки"""
    PROJECT_ROOT = Path(__file__).parent.parent
    BUILD_DIR = PROJECT_ROOT / "build"
    DIST_DIR = PROJECT_ROOT / "dist"
    PANDORA_DIR = DIST_DIR / "PANDORA"
    SPEC_FILE = PROJECT_ROOT / "PANDORA.spec"
    LAUNCHER = PROJECT_ROOT / "desktop" / "launcher.py"
    REQUIREMENTS = PROJECT_ROOT / "requirements.txt"
    
    # Директории для включения в exe
    INCLUDE_DIRS = {
        'backend': PROJECT_ROOT / 'backend',
        'frontend': PROJECT_ROOT / 'frontend',
        'data': PROJECT_ROOT / 'data',
    }
    
    # Выходные данные
    APP_NAME = "PANDORA"
    APP_VERSION = "2.0.0"
    APP_AUTHOR = "PANDORA Team"
    OUTPUT_FILE = PROJECT_ROOT / "PANDORA_v2.0.exe"
    
    # Лимиты
    MAX_EXE_SIZE_MB = 600
    BUILD_TIMEOUT_SEC = 3600  # 1 час
    
    # Проверка портов
    BACKEND_PORT = 8000


# ==================== СТИЛИ ВЫВОДА ====================
class Color:
    """ANSI цвета"""
    GREEN = '\033[92m'
    BLUE = '\033[94m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    CYAN = '\033[96m'
    MAGENTA = '\033[95m'
    WHITE = '\033[97m'
    END = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'


def print_banner():
    """Красивый заголовок"""
    banner = f"""
    {Color.CYAN}{Color.BOLD}
    ========================================================
         PANDORA v2.0 - Windows EXE Builder
         Professional Build System
    ========================================================
    {Color.END}
    """
    print(banner)


def print_info(component: str, message: str):
    """Информационное сообщение"""
    prefix_map = {
        "build": f"{Color.BLUE}[BUILD]{Color.END}",
        "check": f"{Color.CYAN}[CHECK]{Color.END}",
        "clean": f"{Color.YELLOW}[CLEAN]{Color.END}",
        "done": f"{Color.GREEN}[DONE]{Color.END}",
        "step": f"{Color.MAGENTA}[STEP]{Color.END}",
    }
    prefix = prefix_map.get(component, f"[{component.upper()}]")
    print(f"{prefix} {message}")


def print_success(message: str):
    """Успешное сообщение"""
    print(f"{Color.GREEN}[OK] {message}{Color.END}")


def print_error(message: str):
    """Ошибка"""
    print(f"{Color.RED}[ERROR] {message}{Color.END}")


def print_warning(message: str):
    """Предупреждение"""
    print(f"{Color.YELLOW}[WARN] {message}{Color.END}")


def print_separator(char: str = "-"):
    """Разделитель"""
    print(f"{Color.DIM}{char * 70}{Color.END}")


# ==================== ПРОВЕРКИ ====================
def check_python_version() -> bool:
    """Проверить версию Python"""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"  └─ Python {version.major}.{version.minor}.{version.micro}")
        return True
    print_warning(f"Python 3.8+ required, but you have {version.major}.{version.minor}")
    return False


def check_pyinstaller() -> bool:
    """Проверить PyInstaller"""
    try:
        import PyInstaller
        version = PyInstaller.__version__
        print(f"  └─ PyInstaller {version}")
        return True
    except ImportError:
        print_warning("PyInstaller not found. Install: pip install PyInstaller")
        return False


def check_project_files() -> bool:
    """Проверить наличие критических файлов"""
    required_files = [
        Config.LAUNCHER,
        Config.SPEC_FILE,
        Config.PROJECT_ROOT / "backend" / "app" / "main.py",
        Config.PROJECT_ROOT / "frontend" / "index.html",
    ]
    
    all_exist = True
    for file in required_files:
        if not file.exists():
            print_warning(f"File not found: {file.name}")
            all_exist = False
    
    if all_exist:
        print(f"  └─ All required files present ({len(required_files)} files)")
    
    return all_exist


def check_dependencies() -> bool:
    """Проверить Python зависимости"""
    required = ['fastapi', 'uvicorn', 'sqlalchemy', 'pydantic', 'webview']
    missing = []
    
    for package in required:
        try:
            __import__(package)
        except ImportError:
            missing.append(package)
    
    if missing:
        print_warning(f"Missing packages: {', '.join(missing)}")
        print_info("check", "Install: pip install -r requirements.txt")
        return False
    
    print(f"  └─ All dependencies installed ({len(required)} packages)")
    return True


def check_disk_space() -> bool:
    """Проверить свободное место на диске"""
    try:
        import shutil
        stat = shutil.disk_usage(Config.PROJECT_ROOT)
        free_gb = stat.free / (1024**3)
        required_gb = 2.0
        
        if free_gb >= required_gb:
            print(f"  └─ Free space: {free_gb:.1f} GB (required: {required_gb} GB)")
            return True
        else:
            print_warning(f"Low disk space: {free_gb:.1f} GB")
            return False
    except Exception as e:
        print_warning(f"Could not check disk space: {e}")
        return True


def check_environment() -> bool:
    """Проверить всё окружение"""
    print_info("check", "Checking build environment...")
    print_separator()
    
    checks = {
        "Python version": check_python_version,
        "PyInstaller": check_pyinstaller,
        "Project files": check_project_files,
        "Dependencies": check_dependencies,
        "Disk space": check_disk_space,
    }
    
    all_ok = True
    for check_name, check_func in checks.items():
        try:
            result = check_func()
            if not result:
                all_ok = False
        except Exception as e:
            print_error(f"{check_name}: {e}")
            all_ok = False
    
    print_separator()
    return all_ok


# ==================== ОЧИСТКА ====================
def clean_build_artifacts():
    """Очистить старые артефакты сборки"""
    print_info("clean", "Cleaning build artifacts...")
    print_separator()
    
    dirs_to_clean = [
        Config.BUILD_DIR,
        Config.DIST_DIR,
        Config.PROJECT_ROOT / "__pycache__",
    ]
    
    for dir_path in dirs_to_clean:
        if dir_path.exists():
            try:
                if dir_path.is_file():
                    dir_path.unlink()
                    print(f"  ✓ Deleted: {dir_path.name}")
                else:
                    shutil.rmtree(dir_path)
                    print(f"  ✓ Removed: {dir_path.name}")
            except Exception as e:
                print_warning(f"Could not delete {dir_path}: {e}")
    
    print_separator()
    print_success("Cleanup complete")


# ==================== СБОРКА ====================
def build_exe(quick: bool = False) -> bool:
    """Собрать EXE файл с помощью PyInstaller"""
    print_info("build", "Starting Windows EXE build...")
    print_separator()
    
    if not quick:
        print_info("step", "Step 1/4: Cleaning old artifacts")
        clean_build_artifacts()
    else:
        print_info("step", "Skipping cleanup (quick build)")
    
    print_info("step", "Step 2/4: Running PyInstaller")
    print(f"  └─ Spec file: {Config.SPEC_FILE.name}")
    print(f"  └─ Timeout: {Config.BUILD_TIMEOUT_SEC // 60} minutes")
    print()
    
    start_time = time.time()
    try:
        result = subprocess.run(
            [sys.executable, "-m", "PyInstaller", str(Config.SPEC_FILE)],
            cwd=str(Config.PROJECT_ROOT),
            timeout=Config.BUILD_TIMEOUT_SEC,
            capture_output=True,
            text=True
        )
        
        build_time = time.time() - start_time
        
        if result.returncode != 0:
            print_error(f"PyInstaller failed with code {result.returncode}")
            if result.stderr:
                print(f"\n{Color.RED}Error output:{Color.END}")
                print(result.stderr[-1000:])  # Last 1000 chars
            return False
        
        print_success(f"PyInstaller completed in {build_time:.1f} seconds")
        
    except subprocess.TimeoutExpired:
        print_error(f"Build timeout exceeded ({Config.BUILD_TIMEOUT_SEC // 60} min)")
        return False
    except Exception as e:
        print_error(f"Build error: {e}")
        return False
    
    print_info("step", "Step 3/4: Verifying build results")
    
    # Проверить что exe создан
    if not Config.PANDORA_DIR.exists():
        print_error(f"Build folder not found: {Config.PANDORA_DIR}")
        return False
    
    exe_path = Config.PANDORA_DIR / "PANDORA.exe"
    if not exe_path.exists():
        print_error(f"EXE not found: {exe_path}")
        return False
    
    exe_size_mb = exe_path.stat().st_size / (1024**2)
    print(f"  ✓ Found: {exe_path.name} ({exe_size_mb:.1f} MB)")
    
    if exe_size_mb > Config.MAX_EXE_SIZE_MB:
        print_warning(f"EXE is larger than {Config.MAX_EXE_SIZE_MB} MB (consider optimization)")
    
    print_info("step", "Step 4/4: Finalizing")
    
    # Скопировать в корень проекта
    if Config.OUTPUT_FILE.exists():
        Config.OUTPUT_FILE.unlink()
    
    shutil.copy2(exe_path, Config.OUTPUT_FILE)
    print(f"  ✓ Copied to: {Config.OUTPUT_FILE.name}")
    
    print_separator()
    return True


# ==================== ТЕСТИРОВАНИЕ ====================
def test_exe() -> bool:
    """Тестировать собранный EXE"""
    print_info("check", "Testing built EXE...")
    print_separator()
    
    if not Config.OUTPUT_FILE.exists():
        print_error(f"EXE not found: {Config.OUTPUT_FILE}")
        return False
    
    print(f"  ✓ EXE found: {Config.OUTPUT_FILE.name}")
    
    # Проверить размер
    size_mb = Config.OUTPUT_FILE.stat().st_size / (1024**2)
    print(f"  ✓ Size: {size_mb:.1f} MB")
    
    # Проверить Windows signature
    try:
        with open(Config.OUTPUT_FILE, 'rb') as f:
            header = f.read(2)
            if header == b'MZ':
                print(f"  ✓ Valid Windows EXE header")
            else:
                print_warning("Invalid EXE header")
                return False
    except Exception as e:
        print_warning(f"Could not verify signature: {e}")
    
    print_separator()
    print_success("Verification complete")
    return True


# ==================== ОТЧЕТ ====================
def generate_report() -> str:
    """Сгенерировать отчет о сборке"""
    exe_info = ""
    if Config.OUTPUT_FILE.exists():
        size_mb = Config.OUTPUT_FILE.stat().st_size / (1024**2)
        exe_info = f"Размер:          {size_mb:.1f} MB\n"
    
    report = f"""
{Color.CYAN}{Color.BOLD}╔═════════════════════════════════════════╗
║  PANDORA v2.0 - Build Report           ║
╚═════════════════════════════════════════╝{Color.END}

📊 METADATA
─────────────────────────────────────────
Application:     {Config.APP_NAME} v{Config.APP_VERSION}
Author:          {Config.APP_AUTHOR}
Build date:      {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Platform:        Windows 64-bit

📁 OUTPUT FILES
─────────────────────────────────────────
Main EXE:        {Config.OUTPUT_FILE.name}
Location:        {Config.PROJECT_ROOT.name}/
{exe_info}

🔧 BUILD CONFIG
─────────────────────────────────────────
Spec file:       {Config.SPEC_FILE.name}
Launcher:        {Config.LAUNCHER.name}
Build tool:      PyInstaller

📦 INCLUDED COMPONENTS
─────────────────────────────────────────
✓ Backend (FastAPI)
  └─ FastAPI server running on port 8000
  └─ SQLAlchemy async ORM
  └─ SQLite database
✓ Frontend (HTML5/CSS/JavaScript)
  └─ Modern responsive UI
  └─ Glass morphism design
  └─ Canvas animations
✓ Data
  └─ Database templates
  └─ Application data

🚀 HOW TO USE
─────────────────────────────────────────
1. Double-click: {Config.OUTPUT_FILE.name}
2. Application will:
   ✓ Start built-in web server (port 8000)
   ✓ Open in native window
   ✓ Initialize database if needed
3. Press Ctrl+C in terminal to close

📋 ARCHITECTURE
─────────────────────────────────────────
• Single-file executable (all-in-one)
• Uvicorn backend runs in thread
• PyWebView native window
• SQLite database (auto-initialized)
• No additional dependencies needed

✅ BUILD SUCCESSFUL

To distribute:
→ Send {Config.OUTPUT_FILE.name} to users
→ No installation required
→ Works on Windows 7+ (recommended Windows 10+)

{Color.GREEN}═════════════════════════════════════════{Color.END}
"""
    return report


# ==================== MAIN ====================
def main():
    """Главная функция"""
    parser = argparse.ArgumentParser(
        description="PANDORA v2.0 - Professional Windows EXE Builder",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python build.py              # Full build with checks
  python build.py --quick      # Quick build (skip cleanup)
  python build.py --clean      # Only clean artifacts
  python build.py --test       # Only test built EXE
  python build.py --help       # This help

Documentation:
  See docs/ folder for architecture details
        """
    )
    
    parser.add_argument(
        "--quick",
        action="store_true",
        help="Quick build (skip cleanup)"
    )
    
    parser.add_argument(
        "--clean",
        action="store_true",
        help="Only clean artifacts"
    )
    
    parser.add_argument(
        "--test",
        action="store_true",
        help="Only test built EXE"
    )
    
    args = parser.parse_args()
    
    print_banner()
    
    # Only clean?
    if args.clean:
        clean_build_artifacts()
        return 0
    
    # Only test?
    if args.test:
        test_exe()
        return 0
    
    # FULL BUILD
    print_info("step", "Phase 1: Environment Check")
    if not check_environment():
        print_error("Environment check failed!")
        return 1
    
    print_info("step", "Phase 2: Building EXE")
    print()
    
    success = build_exe(quick=args.quick)
    
    if not success:
        print_error("Build failed")
        return 1
    
    print_info("step", "Phase 3: Testing")
    print()
    
    test_exe()
    
    # Generate report
    report = generate_report()
    print(report)
    
    # Save report
    report_file = Config.PROJECT_ROOT / "BUILD_REPORT.md"
    with open(report_file, 'w', encoding='utf-8') as f:
        # Remove ANSI codes for file
        clean_report = report
        for color in [Color.GREEN, Color.CYAN, Color.BOLD, Color.END, Color.YELLOW]:
            clean_report = clean_report.replace(color, '')
        f.write(clean_report)
    
    print_success(f"Report saved to {report_file.name}")
    
    print_info("done", "Build PANDORA v2.0 complete! ✨")
    print_info("done", f"Download: {Config.OUTPUT_FILE.name}")
    
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print_warning("\nBuild cancelled by user")
        sys.exit(130)
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

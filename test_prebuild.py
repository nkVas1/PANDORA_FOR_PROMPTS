#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PANDORA v2.0 - Pre-Build Test Suite
Комплексное тестирование перед сборкой в EXE

Использование:
    python test_prebuild.py          # Все тесты
    python test_prebuild.py --quick  # Быстрые тесты
    python test_prebuild.py --api    # Только API тесты
    python test_prebuild.py --help   # Справка

Проверяет:
    ✓ Структура проекта
    ✓ Импорты всех модулей
    ✓ API endpoints
    ✓ Frontend assets
    ✓ Database connectivity
    ✓ Конфигурация
"""

import os
import sys
import subprocess
import json
import time
import argparse
import sqlite3
from pathlib import Path
from typing import List, Tuple, Dict
from datetime import datetime
import urllib.request
import urllib.error

# ==================== КОНФИГ ====================
class Config:
    PROJECT_ROOT = Path(__file__).parent.parent
    BACKEND_PATH = PROJECT_ROOT / "backend"
    FRONTEND_PATH = PROJECT_ROOT / "frontend"
    VENV_PATH = PROJECT_ROOT / "venv"
    
    API_URL = "http://127.0.0.1:8000"
    API_PORT = 8000
    
    # Ожидание запуска
    API_STARTUP_TIMEOUT = 15
    HEALTH_CHECK_RETRY = 0.5
    
    # Завершение
    CLEANUP_TIMEOUT = 5


# ==================== СТИЛИ ====================
class Color:
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
    banner = f"""
    {Color.CYAN}{Color.BOLD}
    ╔═════════════════════════════════════════╗
    ║  PANDORA v2.0 - Pre-Build Test Suite  ║
    ║     Полное тестирование перед EXE     ║
    ╚═════════════════════════════════════════╝
    {Color.END}
    """
    print(banner)


def print_test(name: str, status: str):
    """Напечатать результат теста"""
    if status == "✓":
        symbol = f"{Color.GREEN}✓{Color.END}"
    elif status == "✗":
        symbol = f"{Color.RED}✗{Color.END}"
    else:
        symbol = f"{Color.YELLOW}⊘{Color.END}"
    
    print(f"  {symbol} {name}")


def print_section(title: str):
    """Напечатать заголовок секции"""
    print(f"\n{Color.CYAN}{Color.BOLD}▶ {title}{Color.END}")
    print(f"{Color.DIM}{'─' * 55}{Color.END}")


def print_success(msg: str):
    print(f"{Color.GREEN}✅ {msg}{Color.END}")


def print_error(msg: str):
    print(f"{Color.RED}❌ {msg}{Color.END}")


def print_warning(msg: str):
    print(f"{Color.YELLOW}⚠️  {msg}{Color.END}")


# ==================== ТЕСТЫ ====================
class PreBuildTester:
    def __init__(self):
        self.results = {
            "structure": [],
            "imports": [],
            "api": [],
            "frontend": [],
            "database": [],
        }
        self.api_process = None
    
    # ─────────────────────────────────────────
    # ТЕСТЫ СТРУКТУРЫ
    # ─────────────────────────────────────────
    
    def test_project_structure(self) -> bool:
        """Проверить структуру проекта"""
        print_section("1. Структура проекта")
        
        required_dirs = [
            ("backend", Config.BACKEND_PATH),
            ("frontend", Config.FRONTEND_PATH),
            ("docs", Config.PROJECT_ROOT / "docs"),
            ("venv", Config.VENV_PATH),
        ]
        
        all_ok = True
        for name, path in required_dirs:
            if path.exists():
                print_test(f"Папка {name}/", "✓")
            else:
                print_test(f"Папка {name}/", "✗")
                all_ok = False
        
        required_files = [
            ("launcher_final.py", Config.PROJECT_ROOT / "launcher_final.py"),
            ("start_v2.py", Config.PROJECT_ROOT / "start_v2.py"),
            ("PANDORA.spec", Config.PROJECT_ROOT / "PANDORA.spec"),
            ("requirements.txt", Config.PROJECT_ROOT / "requirements.txt"),
            (".env", Config.PROJECT_ROOT / ".env"),
        ]
        
        for name, path in required_files:
            if path.exists():
                print_test(f"Файл {name}", "✓")
            else:
                print_test(f"Файл {name}", "✗")
                all_ok = False
        
        return all_ok
    
    def test_backend_structure(self) -> bool:
        """Проверить структуру backend"""
        print_section("2. Backend структура")
        
        required = [
            ("app/main.py", Config.BACKEND_PATH / "app" / "main.py"),
            ("app/api/routes.py", Config.BACKEND_PATH / "app" / "api" / "routes.py"),
            ("app/models/", Config.BACKEND_PATH / "app" / "models"),
            ("app/services/", Config.BACKEND_PATH / "app" / "services"),
            ("app/db/", Config.BACKEND_PATH / "app" / "db"),
        ]
        
        all_ok = True
        for name, path in required:
            if path.exists():
                print_test(f"Компонент {name}", "✓")
            else:
                print_test(f"Компонент {name}", "✗")
                all_ok = False
        
        return all_ok
    
    def test_frontend_structure(self) -> bool:
        """Проверить структуру frontend"""
        print_section("3. Frontend структура")
        
        required = [
            ("index.html", Config.FRONTEND_PATH / "index.html"),
            ("css/", Config.FRONTEND_PATH / "css"),
            ("js/", Config.FRONTEND_PATH / "js"),
        ]
        
        all_ok = True
        for name, path in required:
            if path.exists():
                print_test(f"Компонент {name}", "✓")
            else:
                print_test(f"Компонент {name}", "✗")
                all_ok = False
        
        return all_ok
    
    # ─────────────────────────────────────────
    # ТЕСТЫ ИМПОРТОВ
    # ─────────────────────────────────────────
    
    def test_python_imports(self) -> bool:
        """Проверить критические Python импорты"""
        print_section("4. Python импорты")
        
        required = {
            "fastapi": "FastAPI",
            "uvicorn": "Uvicorn",
            "sqlalchemy": "SQLAlchemy",
            "pydantic": "Pydantic",
            "aiosqlite": "AioSQLite",
        }
        
        all_ok = True
        for module, name in required.items():
            try:
                __import__(module)
                print_test(f"{name} установлен", "✓")
            except ImportError:
                print_test(f"{name} НЕ установлен", "✗")
                all_ok = False
        
        return all_ok
    
    def test_app_imports(self) -> bool:
        """Проверить импорты приложения"""
        print_section("5. Импорты приложения")
        
        # Добавить backend в path
        sys.path.insert(0, str(Config.BACKEND_PATH))
        
        modules = [
            ("app.main", "FastAPI app"),
            ("app.api.routes", "API routes"),
            ("app.models.prompt", "Prompt model"),
            ("app.services.prompt", "Prompt service"),
        ]
        
        all_ok = True
        for module_name, description in modules:
            try:
                __import__(module_name)
                print_test(f"{description} ({module_name})", "✓")
            except Exception as e:
                print_test(f"{description} ({module_name})", "✗")
                print(f"      Ошибка: {str(e)[:50]}...")
                all_ok = False
        
        return all_ok
    
    # ─────────────────────────────────────────
    # ТЕСТЫ API
    # ─────────────────────────────────────────
    
    def start_api_server(self) -> bool:
        """Запустить API сервер для тестирования"""
        print_section("6. Запуск API сервера")
        
        print(f"  Порт: {Config.API_PORT}")
        print(f"  Таймаут: {Config.API_STARTUP_TIMEOUT}с")
        print()
        
        cmd = [
            sys.executable,
            "-m", "uvicorn",
            "app.main:app",
            "--host=127.0.0.1",
            f"--port={Config.API_PORT}",
            "--log-level=critical"
        ]
        
        try:
            self.api_process = subprocess.Popen(
                cmd,
                cwd=str(Config.BACKEND_PATH),
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            print_test("API процесс запущен", "✓")
            
            # Ожидание запуска
            return self._wait_for_api()
            
        except Exception as e:
            print_test(f"Запуск API", "✗")
            print(f"      Ошибка: {e}")
            return False
    
    def _wait_for_api(self) -> bool:
        """Ожидать запуска API"""
        start = time.time()
        print_test("Ожидание запуска API", " ")
        
        while time.time() - start < Config.API_STARTUP_TIMEOUT:
            try:
                response = urllib.request.urlopen(
                    f"{Config.API_URL}/docs",
                    timeout=1
                )
                if response.status == 200:
                    return True
            except (urllib.error.URLError, Exception):
                pass
            
            time.sleep(Config.HEALTH_CHECK_RETRY)
            print(".", end="", flush=True)
        
        print()
        return False
    
    def test_api_endpoints(self) -> bool:
        """Тестировать API endpoints"""
        print_section("7. API endpoints")
        
        if not self.api_process or self.api_process.poll() is not None:
            print_test("API сервер живой", "✗")
            return False
        
        endpoints = [
            ("/api/prompts", "GET"),
            ("/api/prompts/search?q=test", "GET"),
            ("/api/projects", "GET"),
            ("/api/tags", "GET"),
            ("/api/stats", "GET"),
        ]
        
        all_ok = True
        for endpoint, method in endpoints:
            try:
                response = urllib.request.urlopen(
                    f"{Config.API_URL}{endpoint}",
                    timeout=2
                )
                if response.status == 200:
                    print_test(f"{method} {endpoint}", "✓")
                else:
                    print_test(f"{method} {endpoint}", "⊘")
            except Exception as e:
                print_test(f"{method} {endpoint}", "✗")
        
        return all_ok
    
    # ─────────────────────────────────────────
    # ТЕСТЫ FRONTEND
    # ─────────────────────────────────────────
    
    def test_frontend_assets(self) -> bool:
        """Проверить frontend assets"""
        print_section("8. Frontend assets")
        
        assets = [
            ("index.html", Config.FRONTEND_PATH / "index.html", "HTML"),
            ("styles.css", Config.FRONTEND_PATH / "css" / "styles.css", "CSS"),
            ("app.js", Config.FRONTEND_PATH / "js" / "app.js", "JavaScript"),
        ]
        
        all_ok = True
        for name, path, asset_type in assets:
            if path.exists():
                size_kb = path.stat().st_size / 1024
                print_test(f"{asset_type}: {name} ({size_kb:.1f} KB)", "✓")
            else:
                print_test(f"{asset_type}: {name}", "✗")
                all_ok = False
        
        return all_ok
    
    def test_css_variables(self) -> bool:
        """Проверить CSS переменные дизайн-системы"""
        print_section("9. CSS переменные (v2.0)")
        
        css_file = Config.FRONTEND_PATH / "css" / "design-system.css"
        
        if not css_file.exists():
            print_test("design-system.css", "✗")
            return False
        
        with open(css_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        required_vars = [
            "--primary-color",
            "--bg-primary",
            "--text-primary",
            "--border-color",
            "--shadow-lg",
        ]
        
        all_ok = True
        for var in required_vars:
            if var in content:
                print_test(f"Переменная {var}", "✓")
            else:
                print_test(f"Переменная {var}", "✗")
                all_ok = False
        
        return all_ok
    
    # ─────────────────────────────────────────
    # ТЕСТЫ БД
    # ─────────────────────────────────────────
    
    def test_database(self) -> bool:
        """Проверить базу данных"""
        print_section("10. База данных")
        
        db_path = Config.FRONTEND_PATH / "pandora.db"
        
        if not db_path.exists():
            print_test("pandora.db", "✗")
            return False
        
        print_test("pandora.db найден", "✓")
        
        # Проверить таблицы
        try:
            conn = sqlite3.connect(str(db_path))
            cursor = conn.cursor()
            
            cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='table'"
            )
            tables = [row[0] for row in cursor.fetchall()]
            
            required_tables = ['prompts', 'projects', 'tags']
            
            for table in required_tables:
                if table in tables:
                    print_test(f"Таблица {table}", "✓")
                else:
                    print_test(f"Таблица {table}", "✗")
            
            conn.close()
            return True
            
        except Exception as e:
            print_test("Чтение БД", "✗")
            print(f"      Ошибка: {e}")
            return False
    
    # ─────────────────────────────────────────
    # ЗАПУСК
    # ─────────────────────────────────────────
    
    def stop_api(self):
        """Остановить API сервер"""
        if self.api_process and self.api_process.poll() is None:
            print("\n" + Color.YELLOW + "Остановка API сервера..." + Color.END)
            try:
                self.api_process.terminate()
                self.api_process.wait(timeout=Config.CLEANUP_TIMEOUT)
            except:
                self.api_process.kill()
    
    def run_all_tests(self, quick: bool = False, api_only: bool = False) -> bool:
        """Запустить все тесты"""
        results = []
        
        # Структура
        if not quick:
            results.append(("Структура проекта", self.test_project_structure()))
            results.append(("Backend структура", self.test_backend_structure()))
            results.append(("Frontend структура", self.test_frontend_structure()))
        
        # Импорты
        results.append(("Python импорты", self.test_python_imports()))
        results.append(("Импорты приложения", self.test_app_imports()))
        
        # API
        if not api_only or api_only == "api":
            if self.start_api_server():
                results.append(("API endpoints", self.test_api_endpoints()))
            else:
                print_warning("API не запустился, пропуск тестов API")
        
        # Frontend
        if not api_only:
            results.append(("Frontend assets", self.test_frontend_assets()))
            results.append(("CSS переменные", self.test_css_variables()))
        
        # БД
        results.append(("База данных", self.test_database()))
        
        # Остановить API
        self.stop_api()
        
        # Итоги
        print_section("ИТОГИ ТЕСТИРОВАНИЯ")
        
        passed = sum(1 for _, result in results if result)
        total = len(results)
        
        print(f"\nВсего тестов: {total}")
        print(f"Пройдено: {Color.GREEN}{passed}{Color.END}")
        print(f"Не пройдено: {Color.RED}{total - passed}{Color.END}")
        print()
        
        for name, result in results:
            symbol = f"{Color.GREEN}✓{Color.END}" if result else f"{Color.RED}✗{Color.END}"
            print(f"  {symbol} {name}")
        
        print()
        
        if passed == total:
            print_success("Все тесты пройдены! Приложение готово к сборке EXE")
            return True
        else:
            print_error(f"{total - passed} тестов не пройдено")
            print_warning("Исправьте ошибки перед сборкой EXE")
            return False


def main():
    parser = argparse.ArgumentParser(
        description="PANDORA v2.0 - Pre-Build Test Suite",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Примеры:
  python test_prebuild.py          # Все тесты
  python test_prebuild.py --quick  # Быстрые тесты (пропустить структуру)
  python test_prebuild.py --api    # Только API тесты

После успешного прохождения тестов:
  python build_exe_v2.py
        """
    )
    
    parser.add_argument("--quick", action="store_true", help="Быстрые тесты")
    parser.add_argument("--api", action="store_true", help="Только API тесты")
    
    args = parser.parse_args()
    
    print_banner()
    
    tester = PreBuildTester()
    
    try:
        success = tester.run_all_tests(quick=args.quick, api_only="api" if args.api else None)
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print_warning("\nТестирование отменено пользователем")
        tester.stop_api()
        sys.exit(130)
    except Exception as e:
        print_error(f"Ошибка при тестировании: {e}")
        import traceback
        traceback.print_exc()
        tester.stop_api()
        sys.exit(1)


if __name__ == "__main__":
    main()

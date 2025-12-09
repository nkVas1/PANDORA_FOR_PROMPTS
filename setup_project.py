#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PANDORA v2.0 - Setup & Configuration Script
Скрипт для автоматической настройки проекта и создания всех необходимых файлов

Использование:
    python setup_project.py              # Полная настройка
    python setup_project.py --quick      # Быстрая настройка
    python setup_project.py --check      # Только проверка
    python setup_project.py --help       # Справка
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path
from typing import List, Tuple
from datetime import datetime

# ==================== КОНФИГ ====================
class Config:
    PROJECT_ROOT = Path(__file__).parent
    VENV_PATH = PROJECT_ROOT / "venv"
    BACKEND_PATH = PROJECT_ROOT / "backend"
    FRONTEND_PATH = PROJECT_ROOT / "frontend"
    DOCS_PATH = PROJECT_ROOT / "docs"
    
    FILES_TO_CREATE = [
        (".env.example", ".env", "Пример переменных окружения"),
    ]
    
    ENV_TEMPLATE = """# PANDORA v2.0 - Environment Configuration
# Скопируйте этот файл в .env и заполните значения

# Database
DATABASE_URL=sqlite:///./pandora.db
DATABASE_RESET=false

# API Server
API_HOST=127.0.0.1
API_PORT=8000
API_RELOAD=true

# Security
SECRET_KEY=your-secret-key-here-change-in-production
ALLOWED_HOSTS=localhost,127.0.0.1

# Logging
LOG_LEVEL=INFO
"""


class Color:
    GREEN = '\033[92m'
    BLUE = '\033[94m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    CYAN = '\033[96m'
    END = '\033[0m'
    BOLD = '\033[1m'


def print_banner():
    print(f"""
    {Color.CYAN}{Color.BOLD}╔════════════════════════════════════════╗
    ║     PANDORA v2.0 - Project Setup      ║
    ║    Автоматическая конфигурация       ║
    ╚════════════════════════════════════════╝{Color.END}
    """)


def print_success(msg: str):
    print(f"{Color.GREEN}✅ {msg}{Color.END}")


def print_error(msg: str):
    print(f"{Color.RED}❌ {msg}{Color.END}")


def print_warning(msg: str):
    print(f"{Color.YELLOW}⚠️  {msg}{Color.END}")


def print_info(msg: str):
    print(f"{Color.CYAN}ℹ️  {msg}{Color.END}")


def print_section(title: str):
    print(f"\n{Color.BOLD}{Color.CYAN}▶ {title}{Color.END}")
    print(f"{Color.CYAN}{'─' * 50}{Color.END}")


# ==================== ПРОВЕРКИ ====================
def check_python_version() -> bool:
    """Проверить версию Python"""
    print_section("1. Проверка Python версии")
    
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print_success(f"Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print_error(f"Требуется Python 3.8+, у вас {version.major}.{version.minor}")
        return False


def check_project_structure() -> bool:
    """Проверить структуру проекта"""
    print_section("2. Проверка структуры проекта")
    
    required_dirs = [
        ("backend", Config.BACKEND_PATH),
        ("frontend", Config.FRONTEND_PATH),
        ("docs", Config.DOCS_PATH),
    ]
    
    all_exist = True
    for name, path in required_dirs:
        if path.exists():
            print_success(f"Папка {name}/ найдена")
        else:
            print_error(f"Папка {name}/ НЕ найдена")
            all_exist = False
    
    return all_exist


def check_venv() -> bool:
    """Проверить виртуальное окружение"""
    print_section("3. Проверка виртуального окружения")
    
    if Config.VENV_PATH.exists():
        print_success("Виртуальное окружение найдено")
        return True
    else:
        print_warning("Виртуальное окружение не найдено")
        return False


# ==================== СОЗДАНИЕ ФАЙЛОВ ====================
def create_env_file() -> bool:
    """Создать .env файл"""
    print_section("4. Создание .env файла")
    
    env_path = Config.PROJECT_ROOT / ".env"
    env_example_path = Config.PROJECT_ROOT / ".env.example"
    
    # Создать .env.example если нет
    if not env_example_path.exists():
        with open(env_example_path, 'w', encoding='utf-8') as f:
            f.write(Config.ENV_TEMPLATE)
        print_success(".env.example создан")
    
    # Создать .env из template если нет
    if not env_path.exists():
        with open(env_path, 'w', encoding='utf-8') as f:
            f.write(Config.ENV_TEMPLATE)
        print_success(".env создан из шаблона")
        print_info("⚠️  Пожалуйста, заполните значения в .env")
        return True
    else:
        print_warning(".env уже существует (не перезаписываем)")
        return False


def create_venv() -> bool:
    """Создать виртуальное окружение"""
    print_section("5. Создание виртуального окружения")
    
    if Config.VENV_PATH.exists():
        print_warning("Виртуальное окружение уже существует")
        return True
    
    try:
        print_info("Создание venv...")
        subprocess.run(
            [sys.executable, "-m", "venv", str(Config.VENV_PATH)],
            check=True,
            capture_output=True
        )
        print_success("Виртуальное окружение создано")
        return True
    except Exception as e:
        print_error(f"Не удалось создать venv: {e}")
        return False


def install_dependencies() -> bool:
    """Установить зависимости"""
    print_section("6. Установка зависимостей")
    
    requirements_file = Config.PROJECT_ROOT / "requirements.txt"
    
    if not requirements_file.exists():
        print_error("requirements.txt не найден")
        return False
    
    try:
        # Определить команду pip
        if sys.platform == 'win32':
            pip_cmd = str(Config.VENV_PATH / "Scripts" / "pip.exe")
        else:
            pip_cmd = str(Config.VENV_PATH / "bin" / "pip")
        
        print_info("Обновление pip...")
        subprocess.run(
            [pip_cmd, "install", "--upgrade", "pip"],
            check=True,
            capture_output=True
        )
        
        print_info("Установка зависимостей из requirements.txt...")
        subprocess.run(
            [pip_cmd, "install", "-r", str(requirements_file)],
            check=True,
            capture_output=False
        )
        
        print_success("Зависимости установлены")
        return True
        
    except Exception as e:
        print_error(f"Не удалось установить зависимости: {e}")
        return False


def create_documentation() -> bool:
    """Убедиться что документация на месте"""
    print_section("7. Проверка документации")
    
    required_docs = [
        ("BUILD_AND_DEPLOYMENT_GUIDE.md", Config.DOCS_PATH / "BUILD_AND_DEPLOYMENT_GUIDE.md"),
        ("DESIGN_VISION_v2.0.md", Config.DOCS_PATH / "DESIGN_VISION_v2.0.md"),
    ]
    
    all_exist = True
    for name, path in required_docs:
        if path.exists():
            print_success(f"Документ {name} найден")
        else:
            print_warning(f"Документ {name} НЕ найден")
            all_exist = False
    
    return all_exist


def print_next_steps():
    """Выведи следующие шаги"""
    print_section("СЛЕДУЮЩИЕ ШАГИ")
    
    print(f"""
{Color.BOLD}Поздравляем! Проект настроен.{Color.END}

{Color.GREEN}1. Локальный запуск:{Color.END}
   • Активируйте окружение: .\\venv\\Scripts\\Activate.ps1
   • Запустите: python start_v2.py
   • Откроется http://127.0.0.1:8000

{Color.GREEN}2. Сборка Windows EXE:{Color.END}
   • Активируйте окружение: .\\venv\\Scripts\\Activate.ps1
   • Запустите: python build_exe_v2.py
   • Результат: PANDORA_v2.0.exe (≈200 MB)

{Color.GREEN}3. Тестирование перед сборкой:{Color.END}
   • Активируйте окружение: .\\venv\\Scripts\\Activate.ps1
   • Запустите: python test_prebuild.py
   • Все тесты должны пройти ✅

{Color.GREEN}4. Дополнительная информация:{Color.END}
   • Читайте: QUICK_START_v2.0.md (быстрый старт)
   • Читайте: docs/BUILD_AND_DEPLOYMENT_GUIDE.md (полное руководство)
   • Читайте: docs/DESIGN_VISION_v2.0.md (концепция)

{Color.YELLOW}⚠️  Важно!{Color.END}
   • Заполните значения в .env файле
   • Убедитесь, что порт 8000 свободен
   • Требуется интернет для скачивания зависимостей
    """)


def check_only():
    """Режим только проверки"""
    print_banner()
    
    checks = [
        ("Python версия", check_python_version),
        ("Структура проекта", check_project_structure),
        ("Виртуальное окружение", check_venv),
        ("Документация", create_documentation),
    ]
    
    print_section("ПРОВЕРКА СТАТУСА")
    
    results = []
    for name, check_func in checks:
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print_error(f"{name}: {e}")
            results.append((name, False))
    
    # Итоги
    print_section("ИТОГИ")
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        symbol = f"{Color.GREEN}✓{Color.END}" if result else f"{Color.RED}✗{Color.END}"
        print(f"  {symbol} {name}")
    
    print()
    print(f"Статус: {passed}/{total} проверок пройдено")
    
    if passed == total:
        print_success("Проект готов к использованию!")
    else:
        print_warning(f"{total - passed} проверок не пройдено")


def full_setup():
    """Полная установка"""
    print_banner()
    
    steps = [
        ("Python версия", check_python_version),
        ("Структура проекта", check_project_structure),
        ("Виртуальное окружение", check_venv),
        ("Файл .env", create_env_file),
        ("Зависимости", create_dependencies),
        ("Документация", create_documentation),
    ]
    
    print_section("ПОЛНАЯ УСТАНОВКА")
    
    all_ok = True
    for name, step_func in steps:
        try:
            print()
            if not step_func():
                all_ok = False
        except Exception as e:
            print_error(f"Ошибка в {name}: {e}")
            all_ok = False
    
    print()
    
    if all_ok:
        print_success("✨ Установка завершена успешно!")
        print_next_steps()
    else:
        print_error("⚠️  Некоторые шаги не завершены")
        print_warning("Пожалуйста, исправьте ошибки выше и запустите снова")
        sys.exit(1)


def quick_setup():
    """Быстрая установка (пропусти некоторые шаги)"""
    print_banner()
    
    print_section("БЫСТРАЯ УСТАНОВКА")
    print()
    
    # Проверить основное
    if not check_python_version():
        sys.exit(1)
    
    if not check_project_structure():
        sys.exit(1)
    
    # Создать необходимое
    create_env_file()
    
    # Установить зависимости если есть venv
    if check_venv():
        install_dependencies()
    else:
        print_warning("Виртуальное окружение не найдено")
        print_info("Запустите с флагом --venv для создания")
    
    print_next_steps()


def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description="PANDORA v2.0 - Setup Script",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Примеры:
  python setup_project.py              # Полная установка
  python setup_project.py --quick      # Быстрая установка
  python setup_project.py --check      # Только проверка

После установки:
  .\\venv\\Scripts\\Activate.ps1
  python start_v2.py
        """
    )
    
    parser.add_argument("--quick", action="store_true", help="Быстрая установка")
    parser.add_argument("--check", action="store_true", help="Только проверка")
    parser.add_argument("--venv", action="store_true", help="Создать venv")
    
    args = parser.parse_args()
    
    try:
        if args.check:
            check_only()
        elif args.quick:
            quick_setup()
        else:
            full_setup()
    except KeyboardInterrupt:
        print_warning("\nУстановка отменена пользователем")
        sys.exit(130)
    except Exception as e:
        print_error(f"Ошибка: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

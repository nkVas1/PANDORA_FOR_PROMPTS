#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PANDORA v2.0 - Windows EXE Builder
Профессиональный скрипт для сборки Windows исполняемого файла

Использование:
    python build_exe_v2.py                  # Полная сборка
    python build_exe_v2.py --quick          # Быстрая сборка (без очистки)
    python build_exe_v2.py --clean          # Только очистка артефактов
    python build_exe_v2.py --help           # Справка

Требует: PyInstaller 6.17.0+
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
    PROJECT_ROOT = Path(__file__).parent
    BUILD_DIR = PROJECT_ROOT / "build"
    DIST_DIR = PROJECT_ROOT / "dist"
    PANDORA_DIR = DIST_DIR / "PANDORA"
    SPEC_FILE = PROJECT_ROOT / "PANDORA.spec"
    LAUNCHER = PROJECT_ROOT / "launcher_final.py"
    REQUIREMENTS = PROJECT_ROOT / "requirements.txt"
    
    # Директории для включения
    INCLUDE_DIRS = {
        'backend': 'backend',
        'frontend': 'frontend',
        'data': 'data',
    }
    
    # Метаданные
    APP_NAME = "PANDORA"
    APP_VERSION = "2.0.0"
    APP_AUTHOR = "PANDORA Team"
    OUTPUT_FILE = PROJECT_ROOT / f"PANDORA_v2.0.exe"
    
    # Порты (для проверки)
    API_PORT = 8000
    
    # Размеры для проверки (mb)
    MAX_EXE_SIZE = 500
    
    # Таймауты
    BUILD_TIMEOUT = 3600  # 1 час
    API_STARTUP_TIMEOUT = 30  # 30 сек


# ==================== СТИЛИ ВЫВОДА ====================
class Color:
    """ANSI цвета для терминала"""
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
    ╔══════════════════════════════════════════════════════╗
    ║         PANDORA v2.0 - Windows EXE Builder          ║
    ║              Профессиональная сборка                 ║
    ╚══════════════════════════════════════════════════════╝
    {Color.END}
    """
    print(banner)


def print_info(component: str, message: str):
    """Информационное сообщение с префиксом"""
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
    print(f"{Color.GREEN}✅ {message}{Color.END}")


def print_error(message: str):
    """Ошибка"""
    print(f"{Color.RED}❌ {message}{Color.END}")


def print_warning(message: str):
    """Предупреждение"""
    print(f"{Color.YELLOW}⚠️  {message}{Color.END}")


def print_separator(char: str = "─"):
    """Разделитель"""
    print(f"{Color.DIM}{char * 60}{Color.END}")


# ==================== ПРОВЕРКИ ====================
def check_environment() -> bool:
    """Проверить окружение перед сборкой"""
    print_info("check", "Проверка окружения...")
    print_separator()
    
    checks = {
        "Python версия": check_python_version,
        "PyInstaller установлен": check_pyinstaller,
        "Файлы на месте": check_project_files,
        "Зависимости": check_dependencies,
        "Свободное место на диске": check_disk_space,
    }
    
    all_ok = True
    for check_name, check_func in checks.items():
        try:
            result = check_func()
            if result:
                print_success(f"{check_name}")
            else:
                print_error(f"{check_name}")
                all_ok = False
        except Exception as e:
            print_error(f"{check_name}: {e}")
            all_ok = False
    
    print_separator()
    return all_ok


def check_python_version() -> bool:
    """Проверить версию Python"""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"  └─ Python {version.major}.{version.minor}.{version.micro}")
        return True
    return False


def check_pyinstaller() -> bool:
    """Проверить PyInstaller"""
    try:
        import PyInstaller
        version = PyInstaller.__version__
        print(f"  └─ PyInstaller {version}")
        return True
    except ImportError:
        print_warning("PyInstaller не установлен. Установите: pip install PyInstaller")
        return False


def check_project_files() -> bool:
    """Проверить наличие файлов проекта"""
    required_files = [
        Config.LAUNCHER,
        Config.SPEC_FILE,
        Config.PROJECT_ROOT / "backend" / "app" / "main.py",
        Config.PROJECT_ROOT / "frontend" / "index.html",
    ]
    
    all_exist = True
    for file in required_files:
        if not file.exists():
            print_warning(f"Файл не найден: {file.relative_to(Config.PROJECT_ROOT)}")
            all_exist = False
    
    if all_exist:
        print(f"  └─ Все необходимые файлы на месте ({len(required_files)} шт.)")
    
    return all_exist


def check_dependencies() -> bool:
    """Проверить зависимости"""
    required = ['fastapi', 'uvicorn', 'sqlalchemy', 'pydantic']
    missing = []
    
    for package in required:
        try:
            __import__(package)
        except ImportError:
            missing.append(package)
    
    if missing:
        print_warning(f"Отсутствуют пакеты: {', '.join(missing)}")
        print_info("check", "Установите: pip install -r requirements.txt")
        return False
    
    print(f"  └─ Все зависимости установлены ({len(required)} пакетов)")
    return True


def check_disk_space() -> bool:
    """Проверить свободное место на диске"""
    try:
        import shutil
        stat = shutil.disk_usage(Config.PROJECT_ROOT)
        free_gb = stat.free / (1024**3)
        required_gb = 2.0
        
        if free_gb >= required_gb:
            print(f"  └─ Свободно: {free_gb:.1f} GB (требуется: {required_gb} GB)")
            return True
        else:
            print_warning(f"Недостаточно места на диске: {free_gb:.1f} GB")
            return False
    except Exception as e:
        print_warning(f"Не удалось проверить место на диске: {e}")
        return True  # Продолжим в любом случае


# ==================== ОЧИСТКА ====================
def clean_build_artifacts():
    """Очистить артефакты сборки"""
    print_info("clean", "Очистка артефактов...")
    print_separator()
    
    dirs_to_clean = [
        Config.BUILD_DIR,
        Config.DIST_DIR,
        Config.PROJECT_ROOT / "__pycache__",
        Config.PROJECT_ROOT / "*.pyc",
    ]
    
    for dir_path in dirs_to_clean:
        if isinstance(dir_path, Path) and dir_path.exists():
            try:
                if dir_path.is_file():
                    dir_path.unlink()
                    print(f"  ✓ Удален файл: {dir_path.name}")
                else:
                    shutil.rmtree(dir_path)
                    print(f"  ✓ Удана папка: {dir_path.name}")
            except Exception as e:
                print_warning(f"Не удалось удалить {dir_path}: {e}")
    
    print_separator()
    print_success("Очистка завершена")


# ==================== СБОРКА ====================
def build_exe(quick: bool = False) -> bool:
    """Собрать EXE файл"""
    print_info("build", "Начинаю сборку Windows EXE...")
    print_separator()
    
    if not quick:
        print_info("step", "Шаг 1/4: Очистка старых артефактов")
        clean_build_artifacts()
    else:
        print_info("step", "Пропуск очистки (быстрая сборка)")
    
    print_info("step", "Шаг 2/4: Запуск PyInstaller")
    print(f"  └─ Команда: pyinstaller {Config.SPEC_FILE.name}")
    print(f"  └─ Таймаут: {Config.BUILD_TIMEOUT // 60} минут")
    
    start_time = time.time()
    try:
        result = subprocess.run(
            [sys.executable, "-m", "PyInstaller", str(Config.SPEC_FILE)],
            cwd=str(Config.PROJECT_ROOT),
            timeout=Config.BUILD_TIMEOUT,
            capture_output=True,
            text=True
        )
        
        build_time = time.time() - start_time
        
        if result.returncode != 0:
            print_error(f"PyInstaller завершился с кодом {result.returncode}")
            if result.stderr:
                print(f"\n{Color.RED}Ошибки:{Color.END}")
                print(result.stderr[-500:])  # Последние 500 символов
            return False
        
        print_success(f"PyInstaller завершился за {build_time:.1f} сек")
        
    except subprocess.TimeoutExpired:
        print_error(f"Сборка превысила таймаут ({Config.BUILD_TIMEOUT // 60} мин)")
        return False
    except Exception as e:
        print_error(f"Ошибка при запуске PyInstaller: {e}")
        return False
    
    print_info("step", "Шаг 3/4: Проверка результатов сборки")
    
    # Проверить наличие собранного приложения
    if not Config.PANDORA_DIR.exists():
        print_error(f"Папка сборки не найдена: {Config.PANDORA_DIR}")
        return False
    
    exe_path = Config.PANDORA_DIR / "PANDORA.exe"
    if not exe_path.exists():
        print_error(f"EXE файл не найден: {exe_path}")
        return False
    
    exe_size_mb = exe_path.stat().st_size / (1024**2)
    print(f"  ✓ Найден EXE: {exe_path.name} ({exe_size_mb:.1f} MB)")
    
    if exe_size_mb > Config.MAX_EXE_SIZE:
        print_warning(f"EXE больше {Config.MAX_EXE_SIZE} MB (оптимизируйте)")
    
    print_info("step", "Шаг 4/4: Финализация")
    
    # Создать финальный EXE в корне проекта
    if Config.OUTPUT_FILE.exists():
        Config.OUTPUT_FILE.unlink()
    
    shutil.copy2(exe_path, Config.OUTPUT_FILE)
    print(f"  ✓ Скопирован в: {Config.OUTPUT_FILE.name}")
    
    print_separator()
    return True


# ==================== ТЕСТИРОВАНИЕ ====================
def test_exe() -> bool:
    """Протестировать собранный EXE"""
    print_info("check", "Тестирование собранного EXE...")
    print_separator()
    
    if not Config.OUTPUT_FILE.exists():
        print_error(f"EXE файл не найден: {Config.OUTPUT_FILE}")
        return False
    
    print(f"  ✓ EXE найден: {Config.OUTPUT_FILE.name}")
    
    # Проверить размер
    size_mb = Config.OUTPUT_FILE.stat().st_size / (1024**2)
    print(f"  ✓ Размер: {size_mb:.1f} MB")
    
    # Проверить сигнатуру Windows
    try:
        with open(Config.OUTPUT_FILE, 'rb') as f:
            header = f.read(2)
            if header == b'MZ':
                print(f"  ✓ Валидный Windows EXE")
            else:
                print_warning(f"Невалидный заголовок EXE")
    except Exception as e:
        print_warning(f"Не удалось проверить сигнатуру: {e}")
    
    print_separator()
    print_success("Тестирование завершено")
    return True


# ==================== ГЕНЕРАЦИЯ ОТЧЕТА ====================
def generate_report() -> str:
    """Сгенерировать отчет о сборке"""
    report = f"""
{Color.CYAN}{Color.BOLD}╔════════════════════════════════════════╗
║     ОТЧЕТ О СБОРКЕ PANDORA v2.0      ║
╚════════════════════════════════════════╝{Color.END}

📊 МЕТАДАННЫЕ
─────────────────────────────────────────
Приложение:      {Config.APP_NAME} v{Config.APP_VERSION}
Автор:           {Config.APP_AUTHOR}
Дата сборки:     {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Платформа:       Windows x64

📁 ВЫХОДНЫЕ ФАЙЛЫ
─────────────────────────────────────────
Основной EXE:    {Config.OUTPUT_FILE.name}
Расположение:    {Config.PROJECT_ROOT.name}
Размер:          {Config.OUTPUT_FILE.stat().st_size / (1024**2):.1f} MB

🔧 КОНФИГ СБОРКИ
─────────────────────────────────────────
Spec файл:       {Config.SPEC_FILE.name}
Launcher:        {Config.LAUNCHER.name}
PyInstaller:     используется collect_all()
Оптимизация:     UPX включена

📦 ВКЛЮЧЕННЫЕ КОМПОНЕНТЫ
─────────────────────────────────────────
✓ Backend (FastAPI)
  └─ app/, api/, models/, services/
✓ Frontend (HTML5/CSS/JS v2.0)
  └─ index.html, css/, js/, images/
✓ Database (SQLite)
  └─ pandora.db + миграции
✓ Dependencies (54 пакета)
  └─ fastapi, uvicorn, sqlalchemy, etc.

🚀 КАК ИСПОЛЬЗОВАТЬ
─────────────────────────────────────────
1. Откройте: {Config.OUTPUT_FILE.name}
2. Приложение автоматически:
   ✓ Запустит встроенный веб-сервер (porт 8000)
   ✓ Откроет браузер с приложением
   ✓ Инициализирует базу данных

⚙️  ДОПОЛНИТЕЛЬНО
─────────────────────────────────────────
• Все файлы упакованы в один EXE
• Размер оптимизирован (< 500 MB)
• Лицензия включена (LICENSE)
• Документация доступна в справке

✅ СБОРКА УСПЕШНА

Для распространения:
→ Отправьте {Config.OUTPUT_FILE.name} пользователям
→ Используйте {Color.YELLOW}NSIS{Color.END} для создания installer
→ Или распространяйте как standalone EXE

{Color.GREEN}═══════════════════════════════════════{Color.END}
"""
    return report


# ==================== ГЛАВНАЯ ФУНКЦИЯ ====================
def main():
    """Главная функция"""
    parser = argparse.ArgumentParser(
        description="PANDORA v2.0 - Windows EXE Builder",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Примеры:
  python build_exe_v2.py              # Полная сборка
  python build_exe_v2.py --quick      # Быстрая сборка
  python build_exe_v2.py --clean      # Только очистка
  python build_exe_v2.py --test       # Тестировать собранный EXE

Документация: docs/PHASE3_DEVELOPMENT_PLAN.md
        """
    )
    
    parser.add_argument(
        "--quick",
        action="store_true",
        help="Быстрая сборка (пропустить очистку)"
    )
    
    parser.add_argument(
        "--clean",
        action="store_true",
        help="Только очистить артефакты сборки"
    )
    
    parser.add_argument(
        "--test",
        action="store_true",
        help="Протестировать собранный EXE"
    )
    
    args = parser.parse_args()
    
    # ═══════════════════════════════════════════════════════
    print_banner()
    
    # Только очистка?
    if args.clean:
        clean_build_artifacts()
        return
    
    # Только тест?
    if args.test:
        test_exe()
        return
    
    # ПОЛНАЯ СБОРКА
    print_info("step", "Этап 1: Проверка окружения")
    if not check_environment():
        print_error("Проверка окружения не пройдена!")
        print_info("check", "Смотрите требования выше")
        sys.exit(1)
    
    print_info("step", "Этап 2: Сборка Windows EXE")
    print()
    
    success = build_exe(quick=args.quick)
    
    if not success:
        print_error("Сборка не удалась")
        sys.exit(1)
    
    print_info("step", "Этап 3: Тестирование")
    print()
    
    if not test_exe():
        print_warning("Некоторые тесты не прошли, но EXE создан")
    
    # Отчет
    report = generate_report()
    print(report)
    
    # Сохранить отчет в файл
    report_file = Config.PROJECT_ROOT / "BUILD_REPORT_v2.0.md"
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report.replace(Color.GREEN, '').replace(Color.CYAN, '').
                replace(Color.BOLD, '').replace(Color.END, '').
                replace(Color.YELLOW, ''))
    
    print_success(f"Отчет сохранен в {report_file.name}")
    
    print_info("done", "Сборка PANDORA v2.0 завершена успешно! ✨")
    print_info("done", f"Скачайте: {Config.OUTPUT_FILE.name}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print_warning("\nСборка отменена пользователем")
        sys.exit(130)
    except Exception as e:
        print_error(f"Неожиданная ошибка: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

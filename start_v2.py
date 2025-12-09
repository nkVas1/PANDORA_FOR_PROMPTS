#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PANDORA v2.0 - Professional Starter Script
Профессиональный стартовый скрипт для локального запуска приложения

Использование:
    python start.py                  # Полный запуск (бот + API)
    python start.py --api-only       # Только API
    python start.py --ngrok          # С HTTPS туннелем
    python start.py --help           # Справка

Преимущества:
    ✓ Правильная обработка Ctrl+C на Windows
    ✓ Проверка окружения перед запуском
    ✓ Цветные логи с префиксами компонентов
    ✓ Отображение информации о запуске
    ✓ Автоматический открытие приложения
"""

import os
import sys
import signal
import threading
import time
import subprocess
import socket
import logging
import webbrowser
import argparse
from pathlib import Path
from typing import Optional, Dict
from datetime import datetime
from dotenv import load_dotenv

# ==================== КОНФИГ ====================
class Config:
    """Конфигурация приложения"""
    PROJECT_ROOT = Path(__file__).parent
    VENV_PATH = PROJECT_ROOT / "venv"
    BACKEND_PATH = PROJECT_ROOT / "backend"
    FRONTEND_PATH = PROJECT_ROOT / "frontend"
    
    # Сервера
    API_HOST = "127.0.0.1"
    API_PORT = 8000
    API_URL = f"http://{API_HOST}:{API_PORT}"
    
    # Переменные окружения
    ENV_FILE = PROJECT_ROOT / ".env"
    
    # Таймауты
    API_STARTUP_TIMEOUT = 15
    HEALTH_CHECK_INTERVAL = 1


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
    ╔════════════════════════════════════════╗
    ║       PANDORA v2.0 - Local Runner     ║
    ║    Профессиональное приложение        ║
    ╚════════════════════════════════════════╝
    {Color.END}
    """
    print(banner)


def print_info(component: str, message: str):
    """Информационное сообщение с префиксом компонента"""
    prefix_map = {
        "api": f"{Color.BLUE}[API]{Color.END}",
        "check": f"{Color.CYAN}[CHECK]{Color.END}",
        "info": f"{Color.CYAN}[INFO]{Color.END}",
        "start": f"{Color.MAGENTA}[START]{Color.END}",
        "sys": f"{Color.WHITE}[SYS]{Color.END}",
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
def check_env_file() -> bool:
    """Проверить файл .env"""
    if not Config.ENV_FILE.exists():
        print_error(".env файл не найден!")
        print_info("info", "Создайте .env с переменными окружения")
        print_info("info", "Используйте как шаблон: .env.example")
        return False
    
    load_dotenv(Config.ENV_FILE)
    print_success(".env загружен")
    return True


def check_dependencies() -> bool:
    """Проверить pip пакеты"""
    required = ['fastapi', 'uvicorn', 'sqlalchemy', 'pydantic']
    missing = []
    
    for package in required:
        try:
            __import__(package)
        except ImportError:
            missing.append(package)
    
    if missing:
        print_error(f"Отсутствуют пакеты: {', '.join(missing)}")
        print_info("info", "Выполните: pip install -r requirements.txt")
        return False
    
    print_success(f"Все зависимости установлены ({len(required)} пакетов)")
    return True


def check_port_available(port: int) -> bool:
    """Проверить, свободен ли порт"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        result = sock.connect_ex((Config.API_HOST, port))
        return result != 0
    finally:
        sock.close()


def check_ports() -> bool:
    """Проверить свободные порты"""
    if not check_port_available(Config.API_PORT):
        print_error(f"Порт {Config.API_PORT} уже занят!")
        print_info("info", "Закройте приложение, использующее этот порт")
        return False
    
    print_success(f"Порт {Config.API_PORT} свободен")
    return True


def check_environment() -> bool:
    """Полная проверка окружения"""
    print_info("check", "Проверка окружения...")
    print_separator()
    
    checks = [
        ("Файл .env", check_env_file),
        ("Зависимости Python", check_dependencies),
        ("Свободные порты", check_ports),
    ]
    
    all_ok = True
    for check_name, check_func in checks:
        try:
            result = check_func()
            if not result:
                all_ok = False
        except Exception as e:
            print_error(f"{check_name}: {e}")
            all_ok = False
    
    print_separator()
    return all_ok


# ==================== МЕНЕДЖЕР ПРОЦЕССОВ ====================
class ProcessManager:
    """Менеджер для запуска и управления процессами"""
    
    def __init__(self):
        self.processes: Dict[str, subprocess.Popen] = {}
        self.outputs: Dict[str, list] = {}
        
    def start_api(self) -> bool:
        """Запустить FastAPI сервер"""
        print_info("start", "Запускаю FastAPI сервер...")
        
        # Команда для запуска Uvicorn
        cmd = [
            sys.executable,
            "-m", "uvicorn",
            "app.main:app",
            f"--host={Config.API_HOST}",
            f"--port={Config.API_PORT}",
            "--reload"
        ]
        
        try:
            process = subprocess.Popen(
                cmd,
                cwd=str(Config.BACKEND_PATH),
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                encoding='utf-8',
                errors='replace'
            )
            self.processes['api'] = process
            self.outputs['api'] = []
            
            print_success(f"API запущен (PID: {process.pid})")
            return True
            
        except Exception as e:
            print_error(f"Не удалось запустить API: {e}")
            return False
    
    def health_check(self, timeout: int = Config.API_STARTUP_TIMEOUT) -> bool:
        """Проверить здоровье API"""
        print_info("check", f"Ожидание запуска API (макс. {timeout}с)...")
        
        start = time.time()
        while time.time() - start < timeout:
            if not check_port_available(Config.API_PORT):
                print_success(f"API доступен на {Config.API_URL}")
                return True
            
            time.sleep(Config.HEALTH_CHECK_INTERVAL)
            print(".", end="", flush=True)
        
        print()
        print_error(f"API не запустился за {timeout} секунд")
        return False
    
    def read_output(self):
        """Читать вывод процессов в реальном времени"""
        for name, process in list(self.processes.items()):
            if process and process.poll() is None:  # Процесс живой
                try:
                    # Неблокирующий read с timeout
                    import select
                    if sys.platform != 'win32':
                        # Unix-like
                        ready, _, _ = select.select([process.stdout], [], [], 0)
                        if ready:
                            line = process.stdout.readline()
                    else:
                        # Windows - просто пытаемся читать
                        line = process.stdout.readline()
                    
                    if line:
                        line = line.rstrip('\n\r')
                        prefix = f"{Color.BLUE}[API]{Color.END}"
                        print(f"{prefix} {line}")
                        self.outputs[name].append(line)
                except:
                    pass
    
    def shutdown(self, signum=None, frame=None):
        """Корректное завершение всех процессов"""
        print_warning("\nЗавершаю все процессы...")
        
        for name, process in list(self.processes.items()):
            if process:
                print_info("sys", f"Завершаю {name}...")
                try:
                    process.terminate()
                    try:
                        process.wait(timeout=3)
                    except subprocess.TimeoutExpired:
                        process.kill()
                        process.wait(timeout=1)
                    print_success(f"{name} завершен")
                except Exception as e:
                    print_error(f"Ошибка завершения {name}: {e}")
        
        print_success("Все процессы завершены")
        sys.exit(0)


# ==================== ГЛАВНАЯ ФУНКЦИЯ ====================
def main():
    """Главная функция"""
    parser = argparse.ArgumentParser(
        description="PANDORA v2.0 - Local Runner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Примеры:
  python start.py                    # Полный запуск (все компоненты)
  python start.py --api-only         # Только API сервер
  python start.py --browser-only     # Только открыть в браузере
  python start.py --help             # Справка
        """
    )
    
    parser.add_argument(
        "--api-only",
        action="store_true",
        help="Запустить только API сервер"
    )
    
    parser.add_argument(
        "--browser-only",
        action="store_true",
        help="Только открыть приложение в браузере"
    )
    
    args = parser.parse_args()
    
    # ═══════════════════════════════════════════════════════
    print_banner()
    
    # Проверка окружения
    if not args.browser_only:
        if not check_environment():
            print_error("Проверка окружения не пройдена!")
            sys.exit(1)
    
    # Менеджер процессов
    manager = ProcessManager()
    
    # Обработчик сигналов
    signal.signal(signal.SIGINT, manager.shutdown)
    if hasattr(signal, 'SIGTERM'):
        signal.signal(signal.SIGTERM, manager.shutdown)
    
    print()
    
    # Запуск компонентов
    if not args.browser_only:
        if not manager.start_api():
            print_error("Не удалось запустить API")
            sys.exit(1)
        
        # Здоровье проверка
        print()
        if not manager.health_check():
            print_error("API не запустился")
            manager.shutdown()
            sys.exit(1)
    
    # Открыть браузер
    print()
    print_info("info", "=" * 60)
    print_success("Все компоненты запущены!")
    print()
    
    if not args.api_only:
        print_info("api", f"🌐 Приложение доступно: {Config.API_URL}")
        print_info("api", f"   → Нажмите Ctrl+C для остановки")
        
        # Попытка открыть в браузере
        try:
            print_info("info", "Открываю браузер...")
            time.sleep(1)
            webbrowser.open(Config.API_URL)
            print_success("Браузер открыт")
        except Exception as e:
            print_warning(f"Не удалось открыть браузер: {e}")
            print_info("info", f"Откройте вручную: {Config.API_URL}")
    
    print_info("info", "=" * 60)
    print()
    
    # Главный цикл
    try:
        while True:
            manager.read_output()
            time.sleep(0.1)
    except KeyboardInterrupt:
        manager.shutdown()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print_error(f"Неожиданная ошибка: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

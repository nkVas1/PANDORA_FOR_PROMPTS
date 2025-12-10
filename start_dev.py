#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PANDORA v2.0 - Development Server Starter
Запускает FastAPI backend + открывает браузер с фронтенд приложением

Usage:
    python start_dev.py
    
Features:
    - Запуск FastAPI с hot reload
    - Автоматическое открытие браузера
    - Красивый вывод логов
    - Graceful shutdown на Ctrl+C
"""

import subprocess
import sys
import time
import webbrowser
import os
from pathlib import Path
import signal


class Colors:
    """ANSI color codes for terminal output"""
    GREEN = '\033[92m'
    BLUE = '\033[94m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    CYAN = '\033[96m'
    END = '\033[0m'
    BOLD = '\033[1m'


def print_banner():
    """Вывести красивый заголовок"""
    print(f"\n{Colors.CYAN}{'='*70}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}🎨 PANDORA v2.0 - Development Server{Colors.END}")
    print(f"{Colors.CYAN}{'='*70}{Colors.END}\n")


def print_info(message: str, prefix: str = "ℹ"):
    """Вывести информационное сообщение"""
    print(f"{Colors.BLUE}[{prefix}]{Colors.END} {message}")


def print_success(message: str):
    """Вывести успешное сообщение"""
    print(f"{Colors.GREEN}[✓]{Colors.END} {message}")


def print_warning(message: str):
    """Вывести предупреждение"""
    print(f"{Colors.YELLOW}[⚠]{Colors.END} {message}")


def print_error(message: str):
    """Вывести ошибку"""
    print(f"{Colors.RED}[✗]{Colors.END} {message}")


def get_project_root():
    """Получить корневую папку проекта"""
    return Path(__file__).parent


def start_backend():
    """Запустить FastAPI backend с hot reload"""
    print_info("Starting FastAPI backend with hot reload...")
    
    project_root = get_project_root()
    backend_dir = project_root / 'backend'
    
    # Убедимся что backend существует
    if not backend_dir.exists():
        print_error(f"Backend directory not found: {backend_dir}")
        return None
    
    # Запускаем uvicorn с hot reload
    try:
        process = subprocess.Popen(
            [
                sys.executable, '-m', 'uvicorn',
                'app.main:app',
                '--reload',
                '--host', '127.0.0.1',
                '--port', '8000'
            ],
            cwd=str(backend_dir),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )
        
        print_success("Backend process started")
        return process
    
    except Exception as e:
        print_error(f"Failed to start backend: {e}")
        return None


def wait_for_backend(max_wait: int = 30, interval: float = 0.5):
    """Дождаться пока backend запустится"""
    import socket
    
    print_info("Waiting for backend to be ready...")
    
    start_time = time.time()
    while time.time() - start_time < max_wait:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex(('127.0.0.1', 8000))
            sock.close()
            
            if result == 0:
                print_success("Backend is ready!")
                return True
        
        except Exception:
            pass
        
        time.sleep(interval)
    
    print_error(f"Backend did not start within {max_wait} seconds")
    return False


def open_browser():
    """Открыть браузер с фронтенд приложением"""
    print_info("Opening browser...")
    
    url = 'http://127.0.0.1:8000'
    try:
        webbrowser.open(url)
        print_success(f"Browser opened at {url}")
    except Exception as e:
        print_warning(f"Could not open browser automatically: {e}")
        print_info(f"Please open manually: {Colors.CYAN}{url}{Colors.END}")


def main():
    """Главная функция"""
    print_banner()
    
    # Запускаем backend
    backend = start_backend()
    if not backend:
        sys.exit(1)
    
    # Ждем пока backend запустится
    if not wait_for_backend():
        backend.terminate()
        sys.exit(1)
    
    # Открываем браузер
    time.sleep(1)  # Даем еще секунду для полной инициализации
    open_browser()
    
    # Выводим информацию
    print()
    print_info("Backend:        http://127.0.0.1:8000", "🚀")
    print_info("API Docs:       http://127.0.0.1:8000/docs", "📚")
    print_info("ReDoc:          http://127.0.0.1:8000/redoc", "📖")
    print()
    print_warning("Press Ctrl+C to stop the server")
    print()
    
    # Обработчик сигналов для graceful shutdown
    def signal_handler(signum, frame):
        print("\n\n" + "="*70)
        print_warning("Stopping server...")
        
        try:
            backend.terminate()
            backend.wait(timeout=5)
            print_success("Backend stopped")
        except subprocess.TimeoutExpired:
            print_warning("Forcing backend shutdown...")
            backend.kill()
        except Exception as e:
            print_error(f"Error stopping backend: {e}")
        
        print_success("Server stopped")
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Читаем логи из backend в реальном времени
    try:
        while True:
            line = backend.stdout.readline()
            if line:
                # Добавляем префикс к логам
                print(f"{Colors.CYAN}[API]{Colors.END} {line.rstrip()}")
            else:
                time.sleep(0.1)
    
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()

if sys.platform == 'win32':
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    try:
        if sys.stdout:
            sys.stdout.reconfigure(encoding='utf-8')
        if sys.stderr:
            sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass


def print_header():
    """Print application header"""
    print("\n" + "=" * 70)
    print("  PANDORA v2.0 - Professional Prompt Manager")
    print("  Development Mode Starter")
    print("=" * 70 + "\n")


def main():
    """Main entry point"""
    print_header()
    
    # Import and run launcher
    try:
        desktop_launcher_path = PROJECT_ROOT / "desktop" / "launcher.py"
        
        if not desktop_launcher_path.exists():
            print(f"ERROR: desktop/launcher.py not found at {desktop_launcher_path}")
            return False
        
        print(f"✓ Using launcher: {desktop_launcher_path}")
        print()
        
        # Import the launcher module
        sys.path.insert(0, str(PROJECT_ROOT / "desktop"))
        from launcher import main as launcher_main
        
        # Run launcher
        launcher_main()
        return True
        
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

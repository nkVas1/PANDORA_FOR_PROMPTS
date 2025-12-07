#!/usr/bin/env python3
"""
PANDORA Prompts Manager - Starter Script
Запуск приложения с управлением процессами backend и frontend
"""

import sys
import os
import subprocess
import signal
import time
from pathlib import Path
from dotenv import load_dotenv
import socket
import platform

# ================ Configuration ================

class Config:
    """Конфигурация приложения"""
    PROJECT_ROOT = Path(__file__).parent
    BACKEND_DIR = PROJECT_ROOT / "backend"
    FRONTEND_DIR = PROJECT_ROOT / "frontend"
    VENV_DIR = PROJECT_ROOT / "venv"
    
    # Используем Python из виртуального окружения
    if VENV_DIR.exists():
        if platform.system() == "Windows":
            PYTHON_CMD = str(VENV_DIR / "Scripts" / "python.exe")
        else:
            PYTHON_CMD = str(VENV_DIR / "bin" / "python")
    else:
        PYTHON_CMD = sys.executable
    
    # Ports
    API_PORT = int(os.getenv("API_PORT", "8000"))
    FRONTEND_PORT = 3000
    
    # API Settings
    API_HOST = "127.0.0.1"
    API_URL = f"http://{API_HOST}:{API_PORT}"
    FRONTEND_URL = f"http://127.0.0.1:{FRONTEND_PORT}"


# ================ Color Output ================

class Color:
    """Цвета для вывода"""
    GREEN = '\033[92m'
    BLUE = '\033[94m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    CYAN = '\033[96m'
    MAGENTA = '\033[95m'
    END = '\033[0m'
    BOLD = '\033[1m'


# ================ Output Functions ================

def print_banner():
    """Красивый заголовок"""
    print(f"""
{Color.CYAN}{Color.BOLD}
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║           🚀 PANDORA PROMPTS MANAGER 🚀                ║
║                                                          ║
║      Professional Prompt Management System v1.0.0       ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
{Color.END}
""")


def print_info(component: str, message: str):
    """Информационное сообщение"""
    if component == "bot":
        prefix = "🤖 BACKEND"
        color = Color.BLUE
    elif component == "frontend":
        prefix = "🌐 FRONTEND"
        color = Color.GREEN
    elif component == "check":
        prefix = "✓ CHECK"
        color = Color.CYAN
    else:
        prefix = "ℹ INFO"
        color = Color.BLUE
    
    print(f"{color}[{prefix}]{Color.END} {message}")


def print_success(message: str):
    """Успешное сообщение"""
    print(f"{Color.GREEN}✅ {message}{Color.END}")


def print_error(message: str):
    """Ошибка"""
    print(f"{Color.RED}❌ {message}{Color.END}")


def print_warning(message: str):
    """Предупреждение"""
    print(f"{Color.YELLOW}⚠️  {message}{Color.END}")


# ================ Pre-launch Checks ================

def check_env():
    """Проверить файл .env"""
    env_file = Config.PROJECT_ROOT / ".env"
    if not env_file.exists():
        env_example = Config.PROJECT_ROOT / ".env.example"
        if env_example.exists():
            # Copy .env.example to .env
            with open(env_example) as f:
                content = f.read()
            with open(env_file, 'w') as f:
                f.write(content)
            print_info("check", "Создан файл .env из .env.example")
        else:
            print_warning(".env файл не найден и не может быть создан")
    
    load_dotenv(env_file)
    print_success(".env файл загружен")


def check_dependencies():
    """Проверить зависимости Python"""
    print_info("check", "Проверка зависимостей Python...")
    
    required_packages = {
        'fastapi': 'FastAPI (Backend API)',
        'sqlalchemy': 'SQLAlchemy (Database ORM)',
        'pydantic': 'Pydantic (Data validation)',
    }
    
    missing = []
    for package, name in required_packages.items():
        try:
            __import__(package)
            print_info("check", f"✓ {name} установлен")
        except ImportError:
            missing.append(package)
            print_error(f"✗ {name} не установлен")
    
    if missing:
        print_warning(f"\nДля установки зависимостей запустите:")
        print(f"  {Color.CYAN}cd {Config.BACKEND_DIR}{Color.END}")
        print(f"  {Color.CYAN}pip install -r requirements.txt{Color.END}")
        return False
    
    print_success("Все зависимости Python установлены")
    return True


def check_ports():
    """Проверить свободные порты"""
    print_info("check", "Проверка доступных портов...")
    
    ports = {
        "API": Config.API_PORT,
        "Frontend": Config.FRONTEND_PORT,
    }
    
    for name, port in ports.items():
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            result = sock.connect_ex(('127.0.0.1', port))
            if result == 0:
                print_error(f"✗ Port {port} ({name}) занят")
                return False
            else:
                print_info("check", f"✓ Port {port} ({name}) свободен")
        finally:
            sock.close()
    
    print_success("Все порты свободны")
    return True


# ================ Process Manager ================

class ProcessManager:
    """Менеджер процессов"""
    
    def __init__(self):
        self.processes = {}
        self.output_threads = {}
    
    def start_backend(self):
        """Запустить backend API"""
        print_info("bot", "Запуск Backend API...")
        
        try:
            # Use uvicorn module instead of run.py for better reload support
            cmd = [
                Config.PYTHON_CMD,
                "-m",
                "uvicorn",
                "app.main:app",
                "--host", "127.0.0.1",
                "--port", str(Config.API_PORT),
                "--reload"
            ]
            
            process = subprocess.Popen(
                cmd,
                cwd=str(Config.BACKEND_DIR),
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
            )
            
            self.processes['backend'] = process
            
            # Wait for API to start
            time.sleep(2)
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            for attempt in range(10):
                try:
                    result = sock.connect_ex(('127.0.0.1', Config.API_PORT))
                    if result == 0:
                        print_success(f"Backend запущен на {Config.API_URL}")
                        sock.close()
                        return True
                except:
                    pass
                time.sleep(0.5)
            
            print_error("Backend не смог запуститься")
            return False
            
        except Exception as e:
            print_error(f"Ошибка запуска Backend: {e}")
            return False
    
    def start_frontend(self):
        """Запустить frontend"""
        print_info("frontend", "Запуск Frontend...")
        
        try:
            # Check if npm is available
            try:
                subprocess.run(["npm", "--version"], capture_output=True, check=True, timeout=5)
            except (FileNotFoundError, subprocess.CalledProcessError):
                print_warning("npm не найден. Frontend недоступен.")
                print_info("frontend", "Установите Node.js для использования Frontend")
                return False
            
            # Check if node_modules exists
            node_modules = Config.FRONTEND_DIR / "node_modules"
            if not node_modules.exists():
                print_warning("node_modules не найден. Установка зависимостей...")
                try:
                    install_cmd = ["npm", "install"]
                    subprocess.run(install_cmd, cwd=str(Config.FRONTEND_DIR), check=True)
                except Exception as e:
                    print_error(f"Ошибка установки npm зависимостей: {e}")
                    return False
            
            cmd = ["npm", "run", "dev"]
            
            process = subprocess.Popen(
                cmd,
                cwd=str(Config.FRONTEND_DIR),
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
            )
            
            self.processes['frontend'] = process
            
            # Wait for frontend to start
            time.sleep(3)
            print_success(f"Frontend запущен на {Config.FRONTEND_URL}")
            return True
            
        except Exception as e:
            print_error(f"Ошибка запуска Frontend: {e}")
            return False
    
    def read_output(self):
        """Читать вывод процессов"""
        for name, process in list(self.processes.items()):
            if process and not process.poll():
                try:
                    line = process.stdout.readline()
                    if line:
                        line = line.rstrip('\n\r')
                        if "error" in line.lower() or "exception" in line.lower():
                            print_error(f"[{name.upper()}] {line}")
                        elif "warning" in line.lower():
                            print_warning(f"[{name.upper()}] {line}")
                        else:
                            print_info(name, line)
                except:
                    pass
    
    def shutdown(self, signum=None, frame=None):
        """Корректное завершение"""
        print_warning("\nЗавершение всех процессов...")
        
        for name, process in list(self.processes.items()):
            if process:
                print_info("check", f"Завершаю {name}...")
                try:
                    if platform.system() == 'Windows':
                        process.terminate()
                        try:
                            process.wait(timeout=3)
                        except subprocess.TimeoutExpired:
                            process.kill()
                    else:
                        process.terminate()
                        try:
                            process.wait(timeout=3)
                        except subprocess.TimeoutExpired:
                            process.kill()
                except Exception as e:
                    print_error(f"Ошибка завершения {name}: {e}")
        
        print_success("Все процессы завершены")
        sys.exit(0)


# ================ Main ================

def main():
    """Главная функция"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="PANDORA Prompts Manager Starter",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Примеры использования:
  python start.py                 # Запуск всего (backend + frontend)
  python start.py --backend-only  # Только backend API
  python start.py --frontend-only # Только frontend
        """
    )
    
    parser.add_argument(
        "--backend-only",
        action="store_true",
        help="Запустить только Backend API"
    )
    
    parser.add_argument(
        "--frontend-only",
        action="store_true",
        help="Запустить только Frontend"
    )
    
    parser.add_argument(
        "--skip-checks",
        action="store_true",
        help="Пропустить проверки перед запуском"
    )
    
    args = parser.parse_args()
    
    # Print banner
    print_banner()
    
    # Pre-launch checks
    if not args.skip_checks:
        check_env()
        if not check_dependencies():
            print_error("Установите зависимости и попробуйте снова")
            sys.exit(1)
        if not check_ports():
            print_error("Освободите необходимые порты и попробуйте снова")
            sys.exit(1)
    
    print()
    
    # Start services
    manager = ProcessManager()
    signal.signal(signal.SIGINT, manager.shutdown)
    signal.signal(signal.SIGTERM, manager.shutdown)
    
    run_backend = not args.frontend_only
    run_frontend = not args.backend_only
    
    if run_backend:
        if not manager.start_backend():
            manager.shutdown()
    
    if run_frontend:
        if not manager.start_frontend():
            manager.shutdown()
    
    # Print info
    print()
    print_info("info", "=" * 60)
    print_success("Все компоненты запущены!")
    print()
    
    if run_backend:
        print_info("bot", "Backend API доступен на:")
        print_info("bot", f"  HTTP: {Config.API_URL}")
        print_info("bot", f"  Docs: {Config.API_URL}/docs")
    
    if run_frontend:
        print_info("frontend", "Frontend доступен на:")
        print_info("frontend", f"  {Config.FRONTEND_URL}")
    
    print()
    print_info("info", "=" * 60)
    print_warning("Нажмите Ctrl+C для остановки всех процессов")
    print()
    
    # Keep running and read output
    try:
        while True:
            manager.read_output()
            time.sleep(0.1)
    except KeyboardInterrupt:
        manager.shutdown()


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PANDORA v2.0 Desktop Launcher (Version 4)
Запускает FastAPI backend в отдельном потоке и PyWebView UI с полным управлением процессами
Интегрирован профессиональный splash screen с логированием и прогресс-баром

АРХИТЕКТУРА:
- Splash screen показывает прогресс загрузки
- UvicornBackend запускает FastAPI напрямую в daemon-потоке (БЕЗ subprocess)
- atexit handlers + signal handlers гарантируют cleanup
- _shutdown_event guard предотвращает множественные вызовы cleanup
- Поддержка FROZEN (exe) и DEV (Python) режимов
- Правильное определение путей для обоих режимов
- Лучшая обработка ошибок подключения

КРИТИЧНО:
✓ Одно окно (не множественные)
✓ Splash screen с логами
✓ Гарантированный cleanup
✓ Корректная работа с путями в exe
✓ Полное управление процессами
✓ Обработка ошибок подключения
"""

import sys
import os
import time
import signal
import threading
import logging
import atexit
from pathlib import Path
from typing import Optional
from threading import Thread, Event
from datetime import datetime

# ==================== КОНФИГУРАЦИЯ ЛОГИРОВАНИЯ ====================
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s'
)
logger = logging.getLogger(__name__)

# ==================== UTF-8 ENCODING (Windows) ====================
if sys.platform == 'win32':
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    try:
        if sys.stdout:
            sys.stdout.reconfigure(encoding='utf-8')
        if sys.stderr:
            sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

# ==================== ИМПОРТЫ ====================
try:
    import webview
    HAS_WEBVIEW = True
except ImportError:
    HAS_WEBVIEW = False
    logger.warning("[WARN] PyWebView not installed. Install: pip install pywebview")

try:
    import requests
except ImportError:
    requests = None
    logger.warning("[WARN] requests not installed. Install: pip install requests")

try:
    from splash_screen_v3 import create_splash_and_manager
    HAS_SPLASH = True
except ImportError:
    HAS_SPLASH = False
    logger.warning("[WARN] Splash screen module not available")

# ==================== ПУТИ И КОНФИГ ====================
FROZEN = getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS')
IS_DEV = not FROZEN

if FROZEN:
    # Запускается из exe (PyInstaller)
    # В этом режиме _MEIPASS содержит распакованные файлы:
    # _MEI*/ (это APP_ROOT)
    #   ├── app/              (backend app модуль)
    #   ├── frontend/         
    #   ├── data/
    APP_ROOT = Path(sys._MEIPASS)
    BACKEND_DIR = APP_ROOT  # Сам _MEIPASS содержит app модуль
    FRONTEND_DIST = APP_ROOT / 'frontend' / 'dist'
    DATA_DIR = APP_ROOT / 'data'
else:
    # Запускается из Python напрямо
    # Структура: project_root/desktop/launcher.py
    LAUNCHER_ROOT = Path(__file__).parent
    APP_ROOT = LAUNCHER_ROOT.parent
    BACKEND_DIR = APP_ROOT / 'backend'
    FRONTEND_DIST = APP_ROOT / 'frontend' / 'dist'
    DATA_DIR = APP_ROOT / 'data'

# Backend
BACKEND_HOST = '127.0.0.1'
BACKEND_PORT = 8000
BACKEND_URL = f'http://{BACKEND_HOST}:{BACKEND_PORT}'

# PyWebView
APP_NAME = 'PANDORA v2.0 - Professional Prompt Manager'
WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 900
MIN_WIDTH = 1000
MIN_HEIGHT = 700

# ==================== ГЛОБАЛЬНОЕ СОСТОЯНИЕ ====================
_shutdown_event = Event()
_app_running = False
_splash = None
_manager = None

# ==================== CLEANUP HANDLERS ====================
def cleanup_on_exit():
    """Гарантированно вызывается при выходе из приложения (atexit)"""
    global _shutdown_event
    
    # Предотвращение множественных вызовов
    if _shutdown_event.is_set():
        return
    
    _shutdown_event.set()
    logger.info('Shutting down PANDORA...')
    time.sleep(0.5)
    logger.info('✓ Shutdown complete')


# Регистрируем cleanup при выходе
atexit.register(cleanup_on_exit)


# ==================== BACKEND MANAGER ====================
class UvicornBackend:
    """
    Запускает FastAPI backend напрямую в потоке Uvicorn (не через subprocess)
    
    КРИТИЧНО: Это НЕ subprocess! Uvicorn запускается в daemon потоке.
    Это предотвращает проблемы с множественными процессами на Windows.
    """
    
    def __init__(self, splash=None, manager=None):
        self.thread: Optional[Thread] = None
        self.is_running = False
        self.exception: Optional[Exception] = None
        self.splash = splash
        self.manager = manager
    
    def _log(self, message: str, status: str = "info"):
        """Логировать с поддержкой splash screen"""
        if self.manager:
            # Доступные методы: log_info, log_success, log_warning, log_error
            # Если status неизвестен, используем log_info
            valid_statuses = ['info', 'success', 'warning', 'error']
            method_name = f'log_{status}' if status in valid_statuses else 'log_info'
            getattr(self.manager, method_name)(message)
        else:
            logger.info(message)
    
    def run_server(self):
        """Запустить Uvicorn server в этом потоке"""
        try:
            import uvicorn
            
            self._log("=" * 70)
            self._log("Initializing FastAPI Backend", "info")
            self._log("=" * 70)
            self._log(f"Backend directory: {BACKEND_DIR}")
            self._log(f"Data directory: {DATA_DIR}")
            self._log(f"Frozen (exe): {FROZEN}")
            
            # Убедимся что директории существуют
            BACKEND_DIR.mkdir(parents=True, exist_ok=True)
            DATA_DIR.mkdir(parents=True, exist_ok=True)
            self._log(f"✓ Directories created/verified", "success")
            
            # Проверим структуру - app модуль должен быть где-то в BACKEND_DIR
            # В FROZEN режиме: PyInstaller может распаковать файлы в разные подкаталоги
            # поэтому ищем папку 'app' в нескольких типичных местах.
            if FROZEN:
                candidates = [
                    APP_ROOT / 'app',
                    APP_ROOT / 'backend' / 'app',
                    APP_ROOT / '_internal' / 'app',
                    APP_ROOT / 'PANDORA' / 'app',
                    APP_ROOT / 'backend',
                ]

                app_dir = None
                for cand in candidates:
                    try:
                        if cand.exists():
                            app_dir = cand
                            break
                    except Exception:
                        continue

                if app_dir is None:
                    # Fallback - assume app under BACKEND_DIR/app
                    app_dir = BACKEND_DIR / 'app'
                    self._log(f"✗ App directory not found in common locations. Fallback to {app_dir}", "warning")
                else:
                    # Если мы нашли папку app, убедимся, что sys.path содержит её родителя
                    backend_dir_candidate = app_dir.parent if app_dir.name == 'app' else app_dir
                    # Avoid declaring `global` after using the name in the function
                    # set module-level BACKEND_DIR via globals() so Python's scoping rules are respected
                    globals()['BACKEND_DIR'] = backend_dir_candidate
                    self._log(f"✓ Detected backend app at: {app_dir}", "success")
                    self._log(f"✓ Using BACKEND_DIR={BACKEND_DIR}", "info")

            else:
                app_dir = BACKEND_DIR / 'app'

            if not app_dir.exists():
                # Попробуем найти app через прямой импорт для диагностики
                self._log(f"✗ App directory not found at {app_dir}", "warning")
                self._log(f"  Searching for app.main module via import...", "info")
                try:
                    from app.main import app as test_app
                    self._log(f"✓ Found app via direct import", "success")
                except ImportError:
                    raise FileNotFoundError(f"Backend app directory not found: {app_dir}")
            else:
                self._log(f"✓ Backend app directory found at {app_dir}", "success")
            
            # Добавим backend в Python path
            if str(BACKEND_DIR) not in sys.path:
                sys.path.insert(0, str(BACKEND_DIR))
                self._log(f"✓ Added to path: {BACKEND_DIR}", "success")
            
            # Импортируем FastAPI app
            try:
                self._log("Importing FastAPI app from app.main...", "info")
                from app.main import app
                self._log("✓ FastAPI app imported successfully", "success")
            except ImportError as e:
                self._log(f"✗ Import error: {e}", "error")
                self._log(f"  Trying to diagnose...", "warning")
                # Пробуем импортировать app.config отдельно для диагностики
                try:
                    from app.config import settings
                    self._log(f"  - app.config OK", "info")
                except ImportError as e2:
                    self._log(f"  - app.config FAILED: {e2}", "error")
                raise
            except Exception as e:
                self._log(f"✗ Unexpected error importing app: {e}", "error")
                import traceback
                self._log(f"  Traceback: {traceback.format_exc()}", "error")
                raise
            
            # Конфигурируем Uvicorn
            self._log(f"Configuring Uvicorn server...", "info")
            self._log(f"  - Host: {BACKEND_HOST}", "info")
            self._log(f"  - Port: {BACKEND_PORT}", "info")
            
            try:
                config = uvicorn.Config(
                    app=app,
                    host=BACKEND_HOST,
                    port=BACKEND_PORT,
                    log_level="error",
                    access_log=False,
                    reload=False,
                )
                self._log("✓ Uvicorn config created", "success")
            except Exception as e:
                self._log(f"✗ Failed to create Uvicorn config: {e}", "error")
                raise
            
            # Создаём server
            try:
                server = uvicorn.Server(config)
                self._log("✓ Uvicorn server created", "success")
            except Exception as e:
                self._log(f"✗ Failed to create Uvicorn server: {e}", "error")
                raise
            
            # Запускаем server (блокирующий вызов)
            self._log("=" * 70)
            self._log("Starting Uvicorn server (blocking call)...", "info")
            self._log("=" * 70)
            self.is_running = True
            
            try:
                server.run()
            except Exception as e:
                self._log(f"✗ Server runtime error: {e}", "error")
                raise
            
        except Exception as e:
            self._log(f"✗ Backend error: {type(e).__name__}: {e}", "error")
            import traceback
            logger.error(f"Backend exception:\n{traceback.format_exc()}")
            self.exception = e
            self.is_running = False
    
    def start(self) -> bool:
        """Запустить backend в daemon потоке"""
        try:
            if self.is_running:
                self._log("Backend is already running")
                return True
            
            self._log("Starting PANDORA Backend...", "info")
            
            # Запускаем в daemon потоке
            self.thread = Thread(target=self.run_server, daemon=True)
            self.thread.start()
            
            # Ждём когда backend будет готов
            self._log("Waiting for backend initialization...", "info")
            
            for attempt in range(80):  # 80 * 0.25 сек = 20 сек максимум
                try:
                    if requests:
                        try:
                            response = requests.get(f"{BACKEND_URL}/health", timeout=1)
                            if response.status_code < 500:
                                health_data = response.json() if response.status_code == 200 else {}
                                self._log("Backend is ready!", "success")
                                self._log(f"URL: {BACKEND_URL}", "info")
                                if health_data:
                                    prompts_count = health_data.get('total_prompts', '?')
                                    self._log(f"Prompts loaded: {prompts_count}", "info")
                                return True
                        except requests.exceptions.ConnectionError:
                            pass
                        except Exception:
                            pass
                except Exception:
                    pass
                
                if attempt % 8 == 0 and attempt > 0:
                    self._log(f"Initializing... {attempt*0.25:.1f}s")
                
                time.sleep(0.25)
            
            self._log("Backend health check timeout, continuing anyway...", "warning")
            self._log(f"Try opening {BACKEND_URL}/ manually if needed", "warning")
            return True
        
        except Exception as e:
            self._log(f"Error starting backend: {e}", "error")
            import traceback
            logger.error(traceback.format_exc())
            return False
    
    def stop(self):
        """Остановить backend"""
        self.is_running = False
        self._log("Backend will stop when app closes (daemon thread)")


# ==================== APPLICATION LAUNCHER ====================
class AppLauncher:
    """Главное приложение - запускает backend и PyWebView"""
    
    def __init__(self, splash=None, manager=None):
        self.backend = UvicornBackend(splash, manager)
        self.window = None
        self.splash = splash
        self.manager = manager
    
    def _log(self, message: str, status: str = "info"):
        """Логировать с поддержкой splash screen"""
        if self.manager:
            # Доступные методы: log_info, log_success, log_warning, log_error
            # Если status неизвестен, используем log_info
            valid_statuses = ['info', 'success', 'warning', 'error']
            method_name = f'log_{status}' if status in valid_statuses else 'log_info'
            getattr(self.manager, method_name)(message)
        else:
            logger.info(message)
    
    def _get_frontend_url(self) -> Optional[str]:
        """Определить URL для загрузки фронтенда"""
        if FROZEN:
            # В exe режиме - пытаемся загрузить из dist
            index_html = FRONTEND_DIST / 'index.html'
            if index_html.exists():
                try:
                    # Используем Path.as_uri() для правильной работы на Windows
                    return index_html.as_uri()
                except Exception:
                    # Fallback
                    p = str(index_html).replace('\\', '/')
                    return f'file:///{p.lstrip("/")}'
        
        # Fallback - всегда можно использовать backend как сервер фронтенда
        return f'{BACKEND_URL}/'
    
    def run(self):
        """Главный метод - запуск приложения"""
        global _app_running
        
        if _app_running:
            self._log("Application is already running!", "error")
            return False
        
        _app_running = True
        
        if self.splash:
            self.splash.show()
        
        print("=" * 70)
        print("  PANDORA v2.0 - Professional Prompt Manager")
        print(f"  {'[FROZEN - EXE MODE]' if FROZEN else '[DEV MODE]'}")
        print("=" * 70)
        print(f"Platform: {sys.platform}")
        print(f"Python: {sys.version.split()[0]}")
        print()
        
        # Signal handlers для graceful shutdown
        def signal_handler(signum, frame):
            self._log("Signal received, shutting down...", "warning")
            if self.window:
                try:
                    self.window.destroy()
                except:
                    pass
            if self.backend:
                self.backend.stop()
            sys.exit(0)
        
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
        
        try:
            # Запускаем backend
            try:
                if self.manager:
                    self.manager.step(0, "Starting Backend")
            except Exception as e:
                logger.error(f"Manager step error: {e}", exc_info=True)
            
            self._log("=" * 70)
            self._log("Starting Backend initialization...", "info")
            self._log("=" * 70)
            
            if not self.backend.start():
                self._log("Failed to start backend", "error")
                if self.splash:
                    self.splash.close(error_delay=True)
                return False
            
            time.sleep(0.5)
            
            # Определяем URL фронтенда
            if self.manager:
                self.manager.step(1, "Loading Frontend")
            
            frontend_url = self._get_frontend_url()
            if not frontend_url:
                self._log("Cannot determine frontend URL", "error")
                if self.splash:
                    self.splash.close(error_delay=True)
                self.backend.stop()
                return False
            
            self._log(f"Loading UI from: {frontend_url}", "info")
            
            if not HAS_WEBVIEW:
                self._log("PyWebView is required. Install: pip install pywebview", "error")
                if self.splash:
                    self.splash.close(error_delay=True)
                return False
            
            # Создаём окно - ОДИН РАЗ
            if self.manager:
                self.manager.step(2, "Creating Window")
            
            self._log("Creating application window...", "info")
            try:
                self.window = webview.create_window(
                    APP_NAME,
                    frontend_url,
                    width=WINDOW_WIDTH,
                    height=WINDOW_HEIGHT,
                    min_size=(MIN_WIDTH, MIN_HEIGHT),
                    background_color='#ffffff',
                    text_select=True,
                )
                self._log("Window created", "success")
                self._log(f"Frontend URL: {frontend_url}", "info")
                
                # Скрыть splash перед запуском UI
                if self.splash:
                    try:
                        self.splash.close()
                    except Exception as e:
                        logger.warning(f"Failed to close splash: {e}")
                
                # Запускаем event loop - блокирующий вызов
                self._log("Starting UI event loop...", "info")
                self._log("=" * 70)
                webview.start(debug=False, http_server=False)
                
                # После webview.start() - программа завершается
                self._log("UI event loop closed", "info")
                return True
                
            except Exception as e:
                self._log(f"Failed to create window: {e}", "error")
                import traceback
                error_msg = traceback.format_exc()
                logger.error(error_msg)
                self._log(f"Traceback: {error_msg}", "error")
                if self.splash:
                    self.splash.close(error_delay=True)
                return False
            
            return True
        
        except Exception as e:
            self._log(f"Error: {e}", "error")
            import traceback
            error_msg = traceback.format_exc()
            logger.error(error_msg)
            self._log(f"Traceback: {error_msg}", "error")
            if self.splash:
                self.splash.close(error_delay=True)
            return False
        
        finally:
            # Гарантируем остановку backend
            try:
                if self.backend:
                    self.backend.stop()
                self._log("Backend stopped", "info")
            except Exception as e:
                logger.error(f"Error stopping backend: {e}", exc_info=True)
            
            # Закрываем splash если открыта
            try:
                if self.splash:
                    self.splash.is_running = False
            except:
                pass


# ==================== MAIN ====================
def main():
    """Entry point for PANDORA application
    
    Initializes splash screen if available and starts the application.
    Logs all errors to file for debugging.
    """
    global _splash, _manager
    
    try:
        # Инициализируем splash screen если доступен
        if HAS_SPLASH:
            try:
                from splash_screen_pro import create_splash_and_manager
                _splash, _manager = create_splash_and_manager()
                
                # Убедимся что окно видимо
                _splash.window.deiconify()
                _splash.window.update()
                
                # Добавляем шаги инициализации
                _manager.add_step("Starting Backend Server", "Initializing API and loading prompts")
                _manager.add_step("Loading Frontend", "Preparing UI components")
                _manager.add_step("Creating Window", "Launching application window")
                
                # Выводим начальное сообщение
                _manager.log_info("=" * 70)
                _manager.log_info("PANDORA v2.0 Initialization Started")
                _manager.log_info("=" * 70)
                
                # Запускаем приложение в контексте splash
                launcher = AppLauncher(_splash, _manager)
                success = launcher.run()
                
            except Exception as e:
                logger.error(f"Splash screen error: {e}", exc_info=True)
                logger.warning("Falling back to standard startup without splash")
                
                # Если splash создана, закрыть её с задержкой
                if _splash:
                    try:
                        _splash.close(error_delay=True)
                    except:
                        pass
                
                _splash = None
                _manager = None
                launcher = AppLauncher()
                success = launcher.run()
        else:
            # Без splash screen
            logger.info("Splash screen not available (splash_screen_pro module missing)")
            launcher = AppLauncher()
            success = launcher.run()
        
        sys.exit(0 if success else 1)
    
    except Exception as e:
        logger.error(f"Critical error in main: {e}", exc_info=True)
        if _splash:
            try:
                _splash.close(error_delay=True)
            except:
                pass
        sys.exit(1)


if __name__ == "__main__":
    main()

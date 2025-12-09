#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PANDORA Desktop Application - Final Launcher
Полноценное desktop приложение для Windows 11 с встроенным браузером

КРИТИЧНО: Этот файл запускается НЕПОСРЕДСТВЕННО из exe. Он НЕ должен вызывать
другие Python скрипты через subprocess (это вызывает циклические запуски).
Вместо этого, мы напрямую запускаем Uvicorn в отдельном потоке.
"""

import sys
import os
import threading
import time
import atexit
import signal
import logging
from pathlib import Path
from typing import Optional

# Try to import splash screen
try:
    import tkinter as tk
    from splash_screen import PandoraSplashScreen
    HAS_SPLASH = True
except ImportError:
    HAS_SPLASH = False

# Ensure UTF-8 on Windows
if sys.platform == 'win32':
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    # Only reconfigure if stdout/stderr exist (not in GUI context)
    try:
        if sys.stdout is not None:
            sys.stdout.reconfigure(encoding='utf-8')
        if sys.stderr is not None:
            sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass  # Silently ignore if not applicable

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s'
)
logger = logging.getLogger(__name__)

# Get application root directory
if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    # Running from PyInstaller exe
    APP_ROOT = Path(sys._MEIPASS)
    IS_FROZEN = True
else:
    # Running from Python directly
    APP_ROOT = Path(__file__).parent
    IS_FROZEN = False

BACKEND_DIR = APP_ROOT / "backend"
FRONTEND_DIR = APP_ROOT / "frontend"
BACKEND_PORT = 8000
BACKEND_URL = f"http://127.0.0.1:{BACKEND_PORT}"

# Configuration
CONFIG = {
    'app_name': 'PANDORA - Prompt Manager',
    'app_icon': str(APP_ROOT / 'ICON.ico') if (APP_ROOT / 'ICON.ico').exists() else None,
    'window_width': 1400,
    'window_height': 900,
    'min_width': 1000,
    'min_height': 700,
    'debug': False,
}

try:
    import webview
    HAS_WEBVIEW = True
except ImportError:
    HAS_WEBVIEW = False
    logger.warning("PyWebView not found, will try to open browser instead")

try:
    import requests
except ImportError:
    requests = None


class UvicornBackend:
    """Run FastAPI backend directly in a thread (NOT as subprocess)"""
    
    def __init__(self):
        self.thread: Optional[threading.Thread] = None
        self.is_running = False
        self.app = None
    
    def run_server(self):
        """Run Uvicorn server in this thread"""
        try:
            import uvicorn
            
            logger.info("=" * 70)
            logger.info("  FastAPI Backend Initialization")
            logger.info("=" * 70)
            logger.info(f"Backend directory: {BACKEND_DIR}")
            logger.info(f"Is frozen (PyInstaller): {IS_FROZEN}")
            logger.info(f"App root: {APP_ROOT}")
            
            # Add backend to Python path
            sys.path.insert(0, str(BACKEND_DIR))
            logger.info(f"Added to Python path: {BACKEND_DIR}")
            
            # Import the FastAPI app
            try:
                logger.info("Importing FastAPI app...")
                from app.main import app
                logger.info("✓ FastAPI app imported successfully")
            except ImportError as e:
                logger.error(f"✗ Failed to import FastAPI app: {e}")
                logger.error("Make sure all dependencies are installed")
                raise
            
            # Configure Uvicorn
            logger.info(f"Configuring Uvicorn server (port {BACKEND_PORT})...")
            config = uvicorn.Config(
                app=app,
                host="127.0.0.1",
                port=BACKEND_PORT,
                log_level="info",
                access_log=False,
                reload=False,
            )
            
            server = uvicorn.Server(config)
            
            # Run the server
            logger.info("Starting Uvicorn server...")
            server.run()
            
        except Exception as e:
            logger.error(f"✗ Error in backend server: {e}")
            import traceback
            logger.error(traceback.format_exc())
            self.is_running = False
    
    def start(self) -> bool:
        """Start backend in a daemon thread"""
        try:
            if self.is_running:
                logger.warning("Backend is already running")
                return True
            
            logger.info("=" * 70)
            logger.info("  🚀 Initializing PANDORA Backend...")
            logger.info("=" * 70)
            
            # Start backend in daemon thread
            self.thread = threading.Thread(target=self.run_server, daemon=True)
            self.thread.start()
            
            # Wait for backend to be ready
            self.is_running = True
            logger.info("⏳ Waiting for backend to be ready...")
            logger.info("   (This may take 30-60+ seconds on first run with large database import)")
            
            # Increased timeout for DB initialization (can take 60+ sec with 1500+ prompts)
            for attempt in range(40):  # 20 seconds max (40 * 0.5)
                try:
                    if requests:
                        response = requests.get(f"{BACKEND_URL}/health", timeout=1)
                        if response.status_code == 200:
                            try:
                                health_data = response.json()
                                logger.info(f"✓ Backend is ready!")
                                logger.info(f"   URL: {BACKEND_URL}")
                                logger.info(f"   DB Path: {health_data.get('db_path', 'unknown')}")
                                logger.info(f"   DB Size: {health_data.get('db_size', 0) / (1024*1024):.2f} MB")
                                logger.info(f"   Prompts: {health_data.get('total_prompts', 0)}")
                                return True
                            except:
                                pass
                except:
                    pass
                
                if attempt % 4 == 0:
                    logger.info(f"   Initializing... {attempt+1}/40")
                time.sleep(0.5)
            
            logger.warning("⚠️  Backend might not be responding, continuing anyway...")
            logger.warning(f"   Try opening {BACKEND_URL}/ in your browser manually")
            return True
        
        except Exception as e:
            logger.error(f"✗ Error starting backend: {e}")
            import traceback
            logger.error(traceback.format_exc())
            self.is_running = False
            return False
    
    def stop(self):
        """Stop backend"""
        self.is_running = False
        logger.info("Backend will stop when window closes")


class DesktopApp:
    """Main desktop application using PyWebView"""
    
    def __init__(self):
        self.backend = UvicornBackend()
        self.webview_window = None
    
    def on_close(self):
        """Handle window close"""
        logger.info("Closing PANDORA...")
        self.backend.stop()
        return True
    
    def run(self):
        """Run the desktop application"""
        # Initialize splash screen if available
        splash = None
        try:
            if HAS_SPLASH:
                root = tk.Tk()
                splash = PandoraSplashScreen(root)
                logger.info("✓ Splash screen initialized")
        except Exception as e:
            logger.warning(f"Could not initialize splash screen: {e}")
        
        try:
            # Update splash with initialization info
            if splash:
                splash.update_progress(5, "Инициализация приложения...")
                splash.show()
            
            logger.info("=" * 70)
            logger.info("  PANDORA - Professional Prompt Management System")
            logger.info("  v1.2.0 | Desktop Edition")
            logger.info("=" * 70)
            logger.info(f"Platform: {sys.platform}")
            logger.info(f"Python: {sys.version.split()[0]}")
            logger.info(f"Frozen (exe): {IS_FROZEN}")
            logger.info(f"App Root: {APP_ROOT}")
            logger.info("")
            
            # Update splash screen
            if splash:
                splash.update_progress(10, "Запуск backend сервера", "FastAPI инициализация")
                splash.show()
            
            # Start backend first
            if not self.backend.start():
                logger.error("✗ Failed to start backend. Exiting.")
                if splash:
                    splash.update_progress(0, "Ошибка инициализации", "Backend не запустился")
                    splash.show()
                    time.sleep(3)
                    splash.close()
                return False
            
            time.sleep(1)
            
            # Update splash with backend ready
            if splash:
                splash.update_progress(30, "Backend готов", "Инициализация UI...")
                splash.show()
            
            # Check if PyWebView is available
            if not HAS_WEBVIEW:
                logger.warning("⚠️  PyWebView not available, attempting to open in browser...")
                if splash:
                    splash.update_progress(50, "PyWebView не найден", "Открываю браузер...")
                    splash.show()
                try:
                    import webbrowser
                    webbrowser.open(f"{BACKEND_URL}/")
                    logger.info(f"✓ Opened {BACKEND_URL}/ in default browser")
                    
                    # Close splash
                    if splash:
                        splash.update_progress(100, "Готово!")
                        splash.show()
                        time.sleep(1)
                        splash.close()
                    
                    # Keep the application running
                    logger.info("📌 Application is running. Press Ctrl+C to quit.")
                    while True:
                        time.sleep(1)
                except Exception as e:
                    logger.error(f"✗ Error opening browser: {e}")
                    if splash:
                        splash.close()
                    return False
            
            # Create PyWebView window
            logger.info("=" * 70)
            logger.info("  Creating Application Window...")
            logger.info("=" * 70)
            
            # Update splash
            if splash:
                splash.update_progress(70, "Создание окна приложения...")
                splash.show()
            
            try:
                # Try to create webview window with native backend
                logger.info("🔧 Attempting to create PyWebView window...")
                
                # Prepare webview parameters
                webview_params = {
                    'title': CONFIG['app_name'],
                    'url': f"{BACKEND_URL}/",
                    'width': CONFIG['window_width'],
                    'height': CONFIG['window_height'],
                    'min_size': (CONFIG['min_width'], CONFIG['min_height']),
                    'background_color': '#ffffff',
                    'text_select': True,
                    'fullscreen': False,
                    'frameless': False,
                    'easy_drag': True,
                    'transparent': False,
                    'on_close': self.on_close,
                    'icon': CONFIG['app_icon'],
                }
                
                # Force native webview backend (not browser fallback)
                if sys.platform == 'win32':
                    # Windows: use EdgeHTML/WebView2
                    webview_params['webview_type'] = 'edgehtml'
                    logger.info("🔧 Windows: Setting webview_type='edgehtml' for native EdgeHTML backend")
                else:
                    # Linux: use GTK WebView
                    webview_params['webview_type'] = 'gtk'
                    logger.info("🔧 Linux: Setting webview_type='gtk' for native GTK backend")
                
                self.webview_window = webview.create_window(**webview_params)
                logger.info("✓ PyWebView window created successfully")
                
                # Log platform info
                if sys.platform == 'win32':
                    logger.info("💻 Running on Windows - Using EdgeHTML WebView2")
                else:
                    logger.info("🐧 Running on Linux - Using GTK WebView")
                    
            except Exception as e:
                logger.error(f"✗ Failed to create PyWebView window: {e}")
                import traceback
                logger.error(traceback.format_exc())
                raise
            
            logger.info("✓ Application window created successfully")
            logger.info(f"📍 Frontend URL: {BACKEND_URL}/")
            logger.info("=" * 70)
            
            # Update splash - almost done
            if splash:
                splash.update_progress(90, "Запуск интерфейса", "Полная загрузка")
                splash.show()
                time.sleep(0.3)
            
            # CRITICAL: Close splash BEFORE webview.start() to prevent hang
            if splash:
                splash.close()
                splash = None
                # Give splash window time to close
                time.sleep(0.2)
            
            # Show window and start event loop
            webview.start(debug=CONFIG['debug'], http_server=False)
            
            return True
        
        except Exception as e:
            logger.error(f"✗ Error: {e}")
            import traceback
            logger.error(traceback.format_exc())
            if splash:
                splash.close()
            return False
        
        finally:
            self.backend.stop()


def main():
    """Main entry point"""
    app = DesktopApp()
    
    # Handle signals for graceful shutdown
    def signal_handler(sig, frame):
        logger.info("\n🛑 Received signal, shutting down...")
        app.backend.stop()
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Run application
    success = app.run()
    
    if not success:
        sys.exit(1)


if __name__ == "__main__":
    main()

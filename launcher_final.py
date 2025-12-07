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
            
            logger.info("Starting FastAPI Backend in main process...")
            
            # Add backend to Python path
            sys.path.insert(0, str(BACKEND_DIR))
            
            # Import the FastAPI app
            try:
                from app.main import app
            except ImportError as e:
                logger.error(f"Failed to import FastAPI app: {e}")
                logger.error("Make sure all dependencies are installed")
                raise
            
            # Configure Uvicorn
            config = uvicorn.Config(
                app=app,
                host="127.0.0.1",
                port=BACKEND_PORT,
                log_level="error",
                access_log=False,
            )
            
            server = uvicorn.Server(config)
            
            # Run the server
            server.run()
            
        except Exception as e:
            logger.error(f"Error in backend server: {e}")
            import traceback
            logger.error(traceback.format_exc())
            self.is_running = False
    
    def start(self) -> bool:
        """Start backend in a daemon thread"""
        try:
            if self.is_running:
                logger.warning("Backend is already running")
                return True
            
            logger.info("🚀 Initializing PANDORA Backend...")
            
            # Start backend in daemon thread
            self.thread = threading.Thread(target=self.run_server, daemon=True)
            self.thread.start()
            
            # Wait for backend to be ready
            self.is_running = True
            logger.info("⏳ Waiting for backend to be ready...")
            
            for attempt in range(30):
                try:
                    if requests:
                        response = requests.get(f"{BACKEND_URL}/", timeout=1)
                        if response.status_code in [200, 404]:
                            logger.info(f"✓ Backend is ready at {BACKEND_URL}")
                            return True
                except:
                    pass
                time.sleep(0.5)
            
            logger.warning("⚠️  Backend might not be responding, continuing anyway...")
            return True
        
        except Exception as e:
            logger.error(f"❌ Error starting backend: {e}")
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
        logger.info("=" * 70)
        logger.info("  PANDORA - Professional Prompt Management System")
        logger.info("=" * 70)
        
        # Start backend first
        if not self.backend.start():
            logger.error("Failed to start backend. Exiting.")
            return False
        
        time.sleep(1)
        
        # Check if PyWebView is available
        if not HAS_WEBVIEW:
            logger.warning("⚠️  PyWebView not available, attempting to open in browser...")
            try:
                import webbrowser
                webbrowser.open(f"{BACKEND_URL}/")
                logger.info(f"Opened {BACKEND_URL}/ in default browser")
                
                # Keep the application running
                logger.info("Application is running. Press Ctrl+C to quit.")
                while True:
                    time.sleep(1)
            except Exception as e:
                logger.error(f"Error opening browser: {e}")
                return False
        
        try:
            # Create PyWebView window
            logger.info("🪟 Creating application window...")
            
            self.webview_window = webview.create_window(
                title=CONFIG['app_name'],
                url=f"{BACKEND_URL}/",
                width=CONFIG['window_width'],
                height=CONFIG['window_height'],
                min_size=(CONFIG['min_width'], CONFIG['min_height']),
                background_color='#ffffff',
                text_select=True,
                fullscreen=False,
            )
            
            logger.info("✓ Application window created")
            logger.info(f"📍 Frontend: {BACKEND_URL}/")
            logger.info("=" * 70)
            
            # Show window and start event loop
            webview.start(debug=CONFIG['debug'], http_server=False)
            
            return True
        
        except Exception as e:
            logger.error(f"❌ Error creating window: {e}")
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

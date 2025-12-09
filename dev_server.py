#!/usr/bin/env python3
"""
Скрипт для локального тестирования приложения (имитирует exe запуск)
"""

import sys
import os
from pathlib import Path

# Добавить backend в PYTHONPATH
sys.path.insert(0, str(Path(__file__).parent / "backend"))

# Установить environ для разработки
os.environ['APP_ENV'] = 'development'
os.environ['DEBUG'] = '1'

# Запустить основной скрипт
if __name__ == "__main__":
    from app.main import app
    import uvicorn
    
    print("[INFO] ═══════════════════════════════════════════════")
    print("[INFO] PANDORA v2.0 - DEV TEST SERVER")
    print("[INFO] ═══════════════════════════════════════════════")
    print()
    print("[INFO] FastAPI server starting on http://127.0.0.1:8000")
    print("[INFO] Open your browser and navigate to the URL")
    print("[INFO] Press Ctrl+C to stop")
    print()
    
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000,
        log_level="info"
    )

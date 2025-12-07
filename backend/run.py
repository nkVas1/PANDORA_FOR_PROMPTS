#!/usr/bin/env python3
"""
Backend application startup script
Скрипт для запуска backend сервера
"""

import uvicorn
import os

if __name__ == "__main__":
    host = os.getenv("API_HOST", "127.0.0.1")
    port = int(os.getenv("API_PORT", "8000"))
    
    # Use module string format for uvicorn to enable reload
    # This allows watching the app.main:app module for changes
    uvicorn.run(
        "app.main:app",
        host=host,
        port=port,
        reload=True,
        log_level="info"
    )

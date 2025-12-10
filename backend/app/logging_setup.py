"""
Backend Logging Configuration
Централизованная система логирования для PANDORA backend
"""

import logging
import sys
from pathlib import Path
from datetime import datetime
import os

def setup_logging():
    """
    Настроить логирование для приложения
    Логи сохраняются в LOCALAPPDATA/PANDORA/logs/app.log
    """
    
    # Определяем директорию логов
    if os.name == 'nt':  # Windows
        logs_dir = Path(os.getenv('LOCALAPPDATA')) / 'PANDORA' / 'logs'
    else:  # Linux/Mac
        logs_dir = Path.home() / '.pandora' / 'logs'
    
    # Создаем директорию если не существует
    logs_dir.mkdir(parents=True, exist_ok=True)
    
    log_file = logs_dir / 'app.log'
    
    # Форматер логов
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # File Handler - все логи
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    
    # Console Handler - только WARNING и выше
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.WARNING)
    console_handler.setFormatter(formatter)
    
    # Root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)
    
    # Log initial info
    logger = logging.getLogger(__name__)
    logger.info(f"Logging initialized. Log file: {log_file}")
    logger.info(f"Python version: {sys.version}")
    logger.info(f"Platform: {sys.platform}")
    
    return logger

# Инициализируем логирование при импорте
logger = setup_logging()

"""
Structured logging configuration for PANDORA
JSON-formatted structured logging для удобного анализа логов
"""

import logging
import json
from datetime import datetime
from pathlib import Path
from typing import Optional


class JSONFormatter(logging.Formatter):
    """Форматирует логи в JSON для структурированного логирования"""
    
    def format(self, record: logging.LogRecord) -> str:
        """Преобразует запись лога в JSON"""
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }
        
        # Добавить дополнительную информацию если есть
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
        
        # Добавить произвольные поля если они в record
        if hasattr(record, "extra_data"):
            log_data.update(record.extra_data)
        
        return json.dumps(log_data, ensure_ascii=False)


class PlainFormatter(logging.Formatter):
    """Форматирует логи в обычный текстовый вид для консоли"""
    
    COLORS = {
        "DEBUG": "\033[36m",      # Cyan
        "INFO": "\033[32m",       # Green
        "WARNING": "\033[33m",    # Yellow
        "ERROR": "\033[31m",      # Red
        "CRITICAL": "\033[35m",   # Magenta
        "RESET": "\033[0m",       # Reset
    }
    
    def format(self, record: logging.LogRecord) -> str:
        """Форматирует лог с цветами для консоли"""
        color = self.COLORS.get(record.levelname, self.COLORS["RESET"])
        
        log_message = (
            f"{color}[{record.levelname:8}]{self.COLORS['RESET']} "
            f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} "
            f"{record.name}:{record.funcName}:{record.lineno} "
            f"→ {record.getMessage()}"
        )
        
        if record.exc_info:
            log_message += f"\n{self.formatException(record.exc_info)}"
        
        return log_message


def setup_logging(
    log_dir: Optional[Path] = None,
    level: int = logging.INFO,
    console_format: str = "plain"
) -> logging.Logger:
    """
    Настраивает логирование для приложения
    
    Args:
        log_dir: Директория для логов (если None, логирует только в консоль)
        level: Уровень логирования (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        console_format: Формат вывода в консоль ('plain' или 'json')
    
    Returns:
        Configured logger instance
    """
    
    # Создаём директорию логов если её нет
    if log_dir:
        log_dir = Path(log_dir)
        log_dir.mkdir(parents=True, exist_ok=True)
    
    # Получаем root logger
    logger = logging.getLogger("pandora")
    logger.setLevel(level)
    
    # Удаляем существующие обработчики чтобы избежать дублей
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    
    if console_format == "json":
        console_handler.setFormatter(JSONFormatter())
    else:
        console_handler.setFormatter(PlainFormatter())
    
    logger.addHandler(console_handler)
    
    # File handlers (если указана директория)
    if log_dir:
        # Основной лог файл
        main_log_handler = logging.FileHandler(
            log_dir / "app.log",
            encoding="utf-8"
        )
        main_log_handler.setLevel(logging.INFO)
        main_log_handler.setFormatter(JSONFormatter())
        logger.addHandler(main_log_handler)
        
        # Лог ошибок
        error_log_handler = logging.FileHandler(
            log_dir / "errors.log",
            encoding="utf-8"
        )
        error_log_handler.setLevel(logging.ERROR)
        error_log_handler.setFormatter(JSONFormatter())
        logger.addHandler(error_log_handler)
    
    return logger


# Кэшированный логгер
_logger: Optional[logging.Logger] = None


def get_logger(name: Optional[str] = None) -> logging.Logger:
    """Получить логгер для модуля"""
    global _logger
    
    if _logger is None:
        from pathlib import Path
        log_dir = Path(__file__).parent.parent.parent / "logs"
        _logger = setup_logging(log_dir=log_dir, level=logging.INFO)
    
    if name:
        return _logger.getChild(name)
    return _logger


# Пример использования в коде:
# from logging_config import get_logger
# logger = get_logger(__name__)
# logger.info("Это информационное сообщение")
# logger.error("Это сообщение об ошибке", exc_info=True)

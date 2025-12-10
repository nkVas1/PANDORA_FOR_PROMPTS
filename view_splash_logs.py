#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
View PANDORA splash screen logs
Скрипт для просмотра логов splash screen
"""

import sys
from pathlib import Path

def view_splash_logs():
    """View the latest splash screen logs"""
    # Логи находятся рядом с EXE в папке dist/logs
    # или в папке с исходным кодом если запущен скрипт
    
    # Пытаемся найти папку dist
    dist_path = Path.cwd().parent / "dist" / "PANDORA"
    
    # Если не найдена, пытаемся относительно текущей папки
    if not dist_path.exists():
        dist_path = Path.cwd() / "build" / "PANDORA"
    
    # Если всё ещё не найдена, используем абсолютный путь
    if not dist_path.exists():
        dist_path = Path(__file__).parent / "dist" / "PANDORA"
    
    log_file = dist_path / "logs" / "splash.log"
    
    print("=" * 80)
    print("PANDORA Splash Screen Logs")
    print("=" * 80)
    print(f"\nLooking for log file at: {log_file}")
    print(f"Exists: {log_file.exists()}")
    
    if not log_file.exists():
        print("\n⚠ No log file found yet. Run PANDORA.exe first.")
        return False
    
    print("\n" + "-" * 80)
    print("LOGS:")
    print("-" * 80 + "\n")
    
    try:
        with open(log_file, "r", encoding="utf-8") as f:
            content = f.read()
        
        print(content)
        
        print("\n" + "-" * 80)
        print(f"Total lines: {len(content.split(chr(10)))}")
        print(f"File size: {len(content)} bytes")
        
        return True
        
    except Exception as e:
        print(f"Error reading log file: {e}")
        return False


if __name__ == "__main__":
    success = view_splash_logs()
    sys.exit(0 if success else 1)

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
    log_file = Path.home() / "AppData" / "Roaming" / "PANDORA" / "logs" / "splash.log"
    
    print("=" * 80)
    print("PANDORA Splash Screen Logs")
    print("=" * 80)
    print(f"\nLog file: {log_file}")
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

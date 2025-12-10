#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PANDORA v2.0 - Development Mode Starter
Запускает backend и desktop приложение в режиме разработки

Использует:
- desktop/launcher.py для запуска desktop приложения
- backend/run.py для запуска FastAPI сервера
"""

import sys
import os
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

# Ensure UTF-8
if sys.platform == 'win32':
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    try:
        if sys.stdout:
            sys.stdout.reconfigure(encoding='utf-8')
        if sys.stderr:
            sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass


def print_header():
    """Print application header"""
    print("\n" + "=" * 70)
    print("  PANDORA v2.0 - Professional Prompt Manager")
    print("  Development Mode Starter")
    print("=" * 70 + "\n")


def main():
    """Main entry point"""
    print_header()
    
    # Import and run launcher
    try:
        desktop_launcher_path = PROJECT_ROOT / "desktop" / "launcher.py"
        
        if not desktop_launcher_path.exists():
            print(f"ERROR: desktop/launcher.py not found at {desktop_launcher_path}")
            return False
        
        print(f"✓ Using launcher: {desktop_launcher_path}")
        print()
        
        # Import the launcher module
        sys.path.insert(0, str(PROJECT_ROOT / "desktop"))
        from launcher import main as launcher_main
        
        # Run launcher
        launcher_main()
        return True
        
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

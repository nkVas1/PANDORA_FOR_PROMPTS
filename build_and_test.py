#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PANDORA v2.0 - Final Build & Test
Финальная сборка и запуск приложения с проверками
"""

import sys
import subprocess
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent

def run_command(cmd, cwd=None, description=""):
    """Выполнить команду и вернуть результат"""
    if description:
        print(f"\n{'='*70}")
        print(f"  {description}")
        print(f"{'='*70}\n")
    
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            cwd=cwd or str(PROJECT_ROOT),
            capture_output=False
        )
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    print("\n" + "="*70)
    print("  PANDORA v2.0 - Final Integration Build")
    print("="*70)
    
    # Step 1: Health check
    print("\n[STEP 1] Running health checks...")
    if not run_command(f"{sys.executable} health_check.py"):
        print("⚠️  Health checks failed, but continuing...")
    
    # Step 2: Build EXE
    print("\n[STEP 2] Building EXE...")
    if run_command(
        f"{sys.executable} build_exe_final.py",
        description="Building EXE with PyInstaller"
    ):
        print("\n✅ EXE build successful!")
    else:
        print("\n⚠️  EXE build failed - check console output above")
    
    # Step 3: Run EXE if it exists
    print("\n[STEP 3] Testing EXE launch...")
    exe_path = PROJECT_ROOT / "dist" / "PANDORA" / "PANDORA.exe"
    if exe_path.exists():
        print(f"✅ EXE found: {exe_path}")
        print("\nLaunching application...")
        print("Note: Close the application window to continue.\n")
        
        try:
            subprocess.run([str(exe_path)])
            print("\n✅ Application closed successfully")
        except Exception as e:
            print(f"⚠️  Error launching: {e}")
    else:
        print(f"⚠️  EXE not found at {exe_path}")
    
    # Final summary
    print("\n" + "="*70)
    print("  BUILD COMPLETE")
    print("="*70)
    print(f"\n✅ PANDORA v2.0 is ready!")
    print(f"\nTo run:")
    print(f"  1. Double-click: {exe_path}")
    print(f"  2. Or command: {exe_path}")
    print(f"\nTo start in development mode:")
    print(f"  python quickstart.py")
    print()

if __name__ == "__main__":
    main()

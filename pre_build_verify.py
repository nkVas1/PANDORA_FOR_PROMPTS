#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pre-Build Verification Script
Скрипт проверки перед сборкой exe
"""

import sys
import subprocess
from pathlib import Path

def run_test(name: str, command: list) -> bool:
    """Run a test command and report result"""
    print(f"\n{'='*70}")
    print(f"[TEST] {name}")
    print('='*70)
    
    try:
        result = subprocess.run(command, capture_output=False)
        if result.returncode == 0:
            print(f"✓ {name} PASSED")
            return True
        else:
            print(f"✗ {name} FAILED (exit code: {result.returncode})")
            return False
    except Exception as e:
        print(f"✗ {name} ERROR: {e}")
        return False


def main():
    """Run all pre-build checks"""
    print("\n" + "="*70)
    print("PANDORA PRE-BUILD VERIFICATION")
    print("="*70)
    
    root = Path(__file__).parent
    tests_passed = []
    tests_failed = []
    
    # Test 1: Syntax check splash_screen_pro.py
    test1 = run_test(
        "Syntax: splash_screen_pro.py",
        [sys.executable, "-m", "py_compile", "desktop/splash_screen_pro.py"]
    )
    (tests_passed if test1 else tests_failed).append("Syntax: splash_screen_pro.py")
    
    # Test 2: Syntax check launcher.py
    test2 = run_test(
        "Syntax: launcher.py",
        [sys.executable, "-m", "py_compile", "desktop/launcher.py"]
    )
    (tests_passed if test2 else tests_failed).append("Syntax: launcher.py")
    
    # Test 3: Import splash_screen_pro
    test3 = run_test(
        "Import: splash_screen_pro",
        [sys.executable, "-c", "import sys; sys.path.insert(0, 'desktop'); from splash_screen_pro import create_splash_and_manager; print('✓ Module loaded')"]
    )
    (tests_passed if test3 else tests_failed).append("Import: splash_screen_pro")
    
    # Test 4: Import launcher
    test4 = run_test(
        "Import: launcher",
        [sys.executable, "-c", "import sys; sys.path.insert(0, 'desktop'); from launcher import main; print('✓ Module loaded')"]
    )
    (tests_passed if test4 else tests_failed).append("Import: launcher")
    
    # Test 5: Test logging
    test5 = run_test(
        "Test: Splash Screen Logging",
        [sys.executable, "test_splash_logging.py"]
    )
    (tests_passed if test5 else tests_failed).append("Test: Splash Screen Logging")
    
    # Summary
    print(f"\n\n{'='*70}")
    print("VERIFICATION SUMMARY")
    print('='*70)
    
    print(f"\n✓ PASSED ({len(tests_passed)}):")
    for test in tests_passed:
        print(f"  • {test}")
    
    if tests_failed:
        print(f"\n✗ FAILED ({len(tests_failed)}):")
        for test in tests_failed:
            print(f"  • {test}")
    
    total = len(tests_passed) + len(tests_failed)
    print(f"\n{'='*70}")
    print(f"Result: {len(tests_passed)}/{total} tests passed")
    
    if tests_failed:
        print("⚠ Please fix failed tests before building exe!")
        return False
    else:
        print("✓ All tests passed! Ready to build exe.")
        print("\nNext step:")
        print("  python desktop/build_exe_final.py")
        return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

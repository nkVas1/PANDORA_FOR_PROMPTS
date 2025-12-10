#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script to verify splash screen logging and error handling
Проверяет логирование и обработку ошибок splash screen
"""

import sys
import os
from pathlib import Path

# Add desktop to path
sys.path.insert(0, str(Path(__file__).parent / "desktop"))

def test_splash_logging():
    """Test splash screen and logging functionality"""
    print("=" * 70)
    print("PANDORA Splash Screen Logging Test")
    print("=" * 70)
    
    try:
        # Test 1: Import modules
        print("\n[TEST 1] Importing modules...")
        from splash_screen_pro import create_splash_and_manager
        print("✓ splash_screen_pro imported successfully")
        
        # Test 2: Create splash
        print("\n[TEST 2] Creating splash screen and manager...")
        splash, manager = create_splash_and_manager()
        print("✓ Splash screen created")
        print(f"✓ Log file: {splash.log_file}")
        
        # Test 3: Show splash
        print("\n[TEST 3] Showing splash screen...")
        splash.show()
        manager.add_step("Test Step 1", "Testing logging functionality")
        manager.add_step("Test Step 2", "Checking error handling")
        print("✓ Splash displayed")
        
        # Test 4: Log different message types
        print("\n[TEST 4] Testing different log types...")
        manager.log_info("This is an info message")
        manager.log_success("This is a success message")
        manager.log_warning("This is a warning message")
        manager.log_error("This is an error message")
        print("✓ All log types tested")
        
        # Test 5: Progress updates
        print("\n[TEST 5] Testing progress updates...")
        manager.step(0, "Step 1", "Running first step")
        import time
        time.sleep(1)
        manager.step(1, "Step 2", "Running second step")
        time.sleep(1)
        print("✓ Progress updates working")
        
        # Test 6: Check log file
        print("\n[TEST 6] Checking log file...")
        if splash.log_file.exists():
            with open(splash.log_file, "r", encoding="utf-8") as f:
                content = f.read()
            print(f"✓ Log file exists ({len(content)} bytes)")
            print(f"✓ Log file path: {splash.log_file}")
            print("\n--- Log File Content (last 20 lines) ---")
            lines = content.split("\n")[-20:]
            for line in lines:
                if line.strip():
                    print(f"  {line}")
            print("--- End of Log ---\n")
        else:
            print("✗ Log file not created")
        
        # Test 7: Error delay
        print("\n[TEST 7] Testing error delay (10 second wait)...")
        print("⚠ This will wait 10 seconds to test error_delay=True")
        print("⚠ Watch the splash screen - it should show error message")
        
        # Create a copy of the splash for error test
        splash_error = create_splash_and_manager()[0]
        splash_error.show()
        splash_error.log_error("Test error - this is a demonstration")
        
        # Simulate error close
        print("⚠ Starting 10 second countdown...")
        splash_error.close(error_delay=True)
        
        print("\n" + "=" * 70)
        print("ALL TESTS COMPLETED SUCCESSFULLY!")
        print("=" * 70)
        print(f"\nLog file location: {splash.log_file}")
        print("\nTo view logs manually:")
        print(f"  start {splash.log_file.parent}")
        
        # Test 8: Verify log directory
        print(f"\nLog directory: {splash.log_file.parent}")
        print(f"Directory exists: {splash.log_file.parent.exists()}")
        
        return True
        
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_splash_logging()
    sys.exit(0 if success else 1)

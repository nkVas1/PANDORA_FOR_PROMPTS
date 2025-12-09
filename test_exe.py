#!/usr/bin/env python3
"""
Скрипт для тестирования собранного exe с выводом логов и возможностью отладки
"""

import subprocess
import sys
import time
import threading
from pathlib import Path

class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_header(msg):
    print(f"{Colors.HEADER}{Colors.BOLD}{'='*60}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{msg}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'='*60}{Colors.ENDC}")

def print_info(msg):
    print(f"{Colors.OKBLUE}[INFO] {msg}{Colors.ENDC}")

def print_success(msg):
    print(f"{Colors.OKGREEN}[OK] {msg}{Colors.ENDC}")

def print_warning(msg):
    print(f"{Colors.WARNING}[WARN] {msg}{Colors.ENDC}")

def print_error(msg):
    print(f"{Colors.FAIL}[ERROR] {msg}{Colors.ENDC}")

def test_exe():
    """Тестировать собранный exe файл"""
    
    print_header("TEST PANDORA v2.0 - EXE Testing")
    
    # Найти exe файл
    exe_path = Path("PANDORA_v2.0.exe")
    if not exe_path.exists():
        print_error(f"EXE file not found: {exe_path.absolute()}")
        print_info("Make sure you ran build_exe_v2.py before testing")
        return False
    
    print_success(f"EXE file found: {exe_path.absolute()}")
    print_info(f"Size: {exe_path.stat().st_size / (1024*1024):.1f} MB")
    
    print()
    print_header("LAUNCHING EXE")
    
    try:
        # Запустить exe с перенаправлением вывода
        print_info("Launching PANDORA.exe...")
        print_warning("Application should open in browser in a few seconds")
        print()
        
        process = subprocess.Popen(
            [str(exe_path.absolute())],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            encoding='utf-8',
            errors='replace'
        )
        
        print_info("Process started, reading logs:")
        print(f"{Colors.OKCYAN}{'─'*60}{Colors.ENDC}")
        
        # Читать вывод в реальном времени
        for line in process.stdout:
            line = line.rstrip('\n\r')
            if line:
                if 'ERROR' in line or 'Failed' in line or 'error' in line:
                    print(f"{Colors.FAIL}{line}{Colors.ENDC}")
                elif 'Successfully' in line or 'mounted' in line or '[OK]' in line:
                    print(f"{Colors.OKGREEN}{line}{Colors.ENDC}")
                elif '[STATIC]' in line or '[API]' in line:
                    print(f"{Colors.OKCYAN}{line}{Colors.ENDC}")
                else:
                    print(line)
        
        # Дождаться завершения процесса
        return_code = process.wait()
        
        print(f"{Colors.OKCYAN}{'─'*60}{Colors.ENDC}")
        print()
        
        if return_code == 0:
            print_success("Application terminated normally")
        else:
            print_warning(f"Application terminated with code: {return_code}")
        
        return return_code == 0
        
    except KeyboardInterrupt:
        print()
        print_warning("Testing interrupted by user")
        try:
            process.terminate()
            time.sleep(1)
            process.kill()
        except:
            pass
        return False
    except Exception as e:
        print_error(f"Error running exe: {e}")
        return False

def main():
    """Главная функция"""
    success = test_exe()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()

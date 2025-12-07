#!/usr/bin/env python3
"""
Reinitialize virtual environment
Переинициализировать виртуальную среду проекта
"""

import subprocess
import sys
import os
from pathlib import Path
import shutil

# Colors for output
class Color:
    GREEN = '\033[92m'
    BLUE = '\033[94m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    CYAN = '\033[96m'
    END = '\033[0m'

def print_info(message: str):
    print(f"{Color.BLUE}ℹ️  {message}{Color.END}")

def print_success(message: str):
    print(f"{Color.GREEN}✅ {message}{Color.END}")

def print_error(message: str):
    print(f"{Color.RED}❌ {message}{Color.END}")

def print_warning(message: str):
    print(f"{Color.YELLOW}⚠️  {message}{Color.END}")

def main():
    """Main reinit function"""
    print()
    print("╔" + "=" * 68 + "╗")
    print("║" + " " * 68 + "║")
    print("║" + "  PANDORA - Virtual Environment Reinitialization".center(68) + "║")
    print("║" + " " * 68 + "║")
    print("╚" + "=" * 68 + "╝")
    print()
    
    root_dir = Path(__file__).parent
    venv_dir = root_dir / "venv"
    backend_dir = root_dir / "backend"
    
    # Step 1: Check if venv exists
    print_info("Checking virtual environment...")
    
    if venv_dir.exists():
        print_warning(f"Virtual environment exists at {venv_dir}")
        response = input(f"{Color.YELLOW}Delete and recreate? (y/n): {Color.END}")
        
        if response.lower() == 'y':
            print_info("Removing old virtual environment...")
            try:
                shutil.rmtree(venv_dir)
                print_success("Old venv removed")
            except Exception as e:
                print_error(f"Failed to remove venv: {e}")
                return False
        else:
            print_info("Using existing virtual environment")
    
    # Step 2: Create virtual environment
    print()
    print_info("Creating virtual environment...")
    try:
        subprocess.run([sys.executable, "-m", "venv", str(venv_dir)], check=True)
        print_success("Virtual environment created")
    except Exception as e:
        print_error(f"Failed to create venv: {e}")
        return False
    
    # Get Python executable from venv
    if sys.platform == "win32":
        venv_python = str(venv_dir / "Scripts" / "python.exe")
    else:
        venv_python = str(venv_dir / "bin" / "python")
    
    # Step 3: Upgrade pip
    print()
    print_info("Upgrading pip, setuptools, wheel...")
    try:
        subprocess.run(
            [venv_python, "-m", "pip", "install", "--upgrade", "pip", "setuptools", "wheel"],
            check=True,
            capture_output=True
        )
        print_success("Pip upgraded")
    except Exception as e:
        print_error(f"Failed to upgrade pip: {e}")
        return False
    
    # Step 4: Install backend dependencies
    print()
    print_info("Installing backend dependencies...")
    try:
        req_file = backend_dir / "requirements.txt"
        if req_file.exists():
            subprocess.run(
                [venv_python, "-m", "pip", "install", "-r", str(req_file)],
                check=True,
                capture_output=True
            )
            print_success("Backend dependencies installed")
        else:
            print_error(f"requirements.txt not found at {req_file}")
            return False
    except Exception as e:
        print_error(f"Failed to install dependencies: {e}")
        return False
    
    # Summary
    print()
    print_info("=" * 68)
    print_success("Virtual environment reinitialized successfully!")
    print()
    print_info("Next steps:")
    print_info("  1. Run the application:")
    print(f"     {Color.CYAN}python start.py{Color.END}")
    print_info("  2. Or build an executable:")
    print(f"     {Color.CYAN}python build.py{Color.END}")
    print()
    print_info("Virtual environment details:")
    print(f"  Location: {Color.CYAN}{venv_dir}{Color.END}")
    print(f"  Python: {Color.CYAN}{venv_python}{Color.END}")
    print()
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print()
        print_warning("Cancelled by user")
        sys.exit(1)
    except Exception as e:
        print()
        print_error(f"Unexpected error: {e}")
        sys.exit(1)

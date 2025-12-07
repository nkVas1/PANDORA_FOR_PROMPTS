#!/usr/bin/env python3
"""
Build script for creating executable from PANDORA application
Скрипт для сборки exe файла
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

ROOT_DIR = Path(__file__).parent
BACKEND_DIR = ROOT_DIR / "backend"
FRONTEND_DIR = ROOT_DIR / "frontend"
BUILD_DIR = ROOT_DIR / "dist"


def print_section(title):
    """Print section header"""
    print()
    print("=" * 70)
    print(f"  {title}")
    print("=" * 70)
    print()


def build_frontend():
    """Build Next.js frontend"""
    print_section("Building Frontend")
    
    try:
        os.chdir(str(FRONTEND_DIR))
        print("Installing dependencies...")
        subprocess.run(["npm", "install"], check=True)
        
        print("Building Next.js application...")
        subprocess.run(["npm", "run", "build"], check=True)
        
        print("✓ Frontend built successfully")
        return True
    except Exception as e:
        print(f"✗ Error building frontend: {e}")
        return False
    finally:
        os.chdir(str(ROOT_DIR))


def install_backend_deps():
    """Install backend dependencies"""
    print_section("Installing Backend Dependencies")
    
    try:
        os.chdir(str(BACKEND_DIR))
        print("Installing Python packages...")
        
        # Install additional packages for exe building
        required_packages = [
            'PyInstaller>=6.0',
            'flask>=2.0',  # Alternative to FastAPI for exe packaging
        ]
        
        subprocess.run([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ], check=True)
        
        for package in required_packages:
            subprocess.run([
                sys.executable, "-m", "pip", "install", package
            ], check=True)
        
        print("✓ Backend dependencies installed")
        return True
    except Exception as e:
        print(f"✗ Error installing dependencies: {e}")
        return False
    finally:
        os.chdir(str(ROOT_DIR))


def create_exe():
    """Create executable using PyInstaller"""
    print_section("Creating Executable")
    
    try:
        # Create a simple launcher script
        launcher_script = ROOT_DIR / "launcher.py"
        launcher_code = '''#!/usr/bin/env python3
import subprocess
import sys
import os
from pathlib import Path

ROOT_DIR = Path(__file__).parent
BACKEND_DIR = ROOT_DIR / "backend"
FRONTEND_DIR = ROOT_DIR / "frontend"

# Run the main starter script
starter_script = ROOT_DIR / "start.py"
subprocess.run([sys.executable, str(starter_script)], cwd=str(ROOT_DIR))
'''
        
        with open(launcher_script, 'w') as f:
            f.write(launcher_code)
        
        # Create exe using PyInstaller
        print("Building executable with PyInstaller...")
        
        subprocess.run([
            sys.executable, "-m", "PyInstaller",
            "--onedir",  # Package as directory
            "--windowed",  # No console window
            "--add-data", f"{BACKEND_DIR}:backend",
            "--add-data", f"{FRONTEND_DIR}:frontend",
            "--hidden-import=fastapi",
            "--hidden-import=sqlalchemy",
            "--hidden-import=pydantic",
            "--collect-all=fastapi",
            "--collect-all=sqlalchemy",
            "--collect-all=pydantic",
            "--name", "PANDORA",
            str(launcher_script)
        ], check=True)
        
        print("✓ Executable created successfully")
        
        # Move to dist
        exe_path = ROOT_DIR / "dist" / "PANDORA"
        if exe_path.exists():
            print(f"Executable location: {exe_path}")
        
        return True
    except Exception as e:
        print(f"✗ Error creating executable: {e}")
        return False


def build_all():
    """Build complete application"""
    print()
    print("╔" + "=" * 68 + "╗")
    print("║" + " " * 68 + "║")
    print("║" + "  PANDORA Prompts Manager - Build Script".center(68) + "║")
    print("║" + " " * 68 + "║")
    print("╚" + "=" * 68 + "╝")
    print()
    
    # Step 1: Install backend dependencies
    if not install_backend_deps():
        print("✗ Build failed at backend dependencies")
        sys.exit(1)
    
    # Step 2: Build frontend
    if not build_frontend():
        print("✗ Build failed at frontend build")
        sys.exit(1)
    
    # Step 3: Create executable
    if not create_exe():
        print("✗ Build failed at executable creation")
        sys.exit(1)
    
    # Summary
    print_section("Build Summary")
    print("✓ All components built successfully!")
    print()
    print("Next steps:")
    print("  1. The executable is located in: dist/PANDORA/")
    print("  2. Run: dist/PANDORA/PANDORA")
    print("  3. Or create a Windows shortcut to the exe")
    print()
    print("Note: The current build method requires Python to be installed")
    print("      on the target machine. For standalone exe, use PyInstaller")
    print("      with UPX or similar tools.")
    print()


if __name__ == "__main__":
    try:
        build_all()
    except KeyboardInterrupt:
        print("\n✗ Build cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        sys.exit(1)

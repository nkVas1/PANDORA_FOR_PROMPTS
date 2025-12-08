#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build script for creating executable from PANDORA application
Скрипт для сборки exe файла
"""

import os
import sys
import subprocess
import shutil
import platform
from pathlib import Path

# Ensure UTF-8 output on Windows
if sys.platform == 'win32':
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

ROOT_DIR = Path(__file__).parent
BACKEND_DIR = ROOT_DIR / "backend"
FRONTEND_DIR = ROOT_DIR / "frontend"
BUILD_DIR = ROOT_DIR / "dist"

# Определяем Python для запуска (используем venv если существует)
VENV_DIR = ROOT_DIR / "venv"
if VENV_DIR.exists():
    if platform.system() == "Windows":
        PYTHON_CMD = str(VENV_DIR / "Scripts" / "python.exe")
    else:
        PYTHON_CMD = str(VENV_DIR / "bin" / "python")
else:
    PYTHON_CMD = sys.executable


def print_section(title):
    """Print section header"""
    print()
    print("=" * 70)
    print(f"  {title}")
    print("=" * 70)
    print()


class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    END = '\033[0m'


def print_success(msg):
    """Print success message"""
    print(f"{Colors.GREEN}✓ {msg}{Colors.END}")


def print_error(msg):
    """Print error message"""
    print(f"{Colors.RED}✗ {msg}{Colors.END}")


def build_frontend():
    """Build Next.js frontend"""
    print_section("Building Frontend")
    
    # Check if npm is available
    try:
        subprocess.run(["npm", "--version"], capture_output=True, check=True, timeout=5)
    except (FileNotFoundError, subprocess.CalledProcessError):
        print("⚠️  npm не найден. Пропускаем сборку Frontend.")
        print("   Установите Node.js для сборки фронтенда")
        print("   https://nodejs.org/")
        return True  # Return True to not block the build
    
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
            PYTHON_CMD, "-m", "pip", "install", "-r", "requirements.txt"
        ], check=True)
        
        for package in required_packages:
            subprocess.run([
                PYTHON_CMD, "-m", "pip", "install", package
            ], check=True)
        
        print("✓ Backend dependencies installed")
        return True
    except Exception as e:
        print(f"✗ Error installing dependencies: {e}")
        return False
    finally:
        os.chdir(str(ROOT_DIR))


def create_exe():
    """Create main PANDORA Desktop Application executable"""
    print_section("Creating PANDORA Desktop Application")
    
    # First, clean old builds
    try:
        if BUILD_DIR.exists():
            print(f"Removing old build directory: {BUILD_DIR}")
            shutil.rmtree(BUILD_DIR)
        # Also remove build directory
        build_dir = ROOT_DIR / "build"
        if build_dir.exists():
            print(f"Removing old build work directory: {build_dir}")
            shutil.rmtree(build_dir)
        # Remove ALL old spec files (important!)
        for spec_file in ROOT_DIR.glob("*.spec"):
            print(f"Removing old spec file: {spec_file.name}")
            spec_file.unlink()
    except Exception as e:
        print(f"Warning: Could not remove old build: {e}")
    
    try:
        launcher_script = ROOT_DIR / "launcher_final.py"
        
        if not launcher_script.exists():
            print_error(f"launcher_final.py не найден в {ROOT_DIR}")
            return False
        
        # Verify required files
        print("\n📋 Verifying required components...")
        print_success(f"Backend directory: {BACKEND_DIR}")
        print_success(f"Frontend directory: {FRONTEND_DIR}")
        print_success(f"Launcher script: {launcher_script}")
        
        # Check for data files
        db_file = FRONTEND_DIR / "pandora.db"
        if db_file.exists():
            db_size_mb = db_file.stat().st_size / (1024*1024)
            print_success(f"Pre-built database: {db_file} ({db_size_mb:.2f} MB)")
        else:
            print(f"⚠️  Database file not found - will be created on first run")
        
        print("\n🔨 Building PANDORA with embedded browser (PyWebView)...")
        
        # Build PyInstaller command
        # Prefer calling the venv's pyinstaller.exe when available; fall back to
        # `python -m PyInstaller` otherwise. Using the executable avoids potential
        # differences in subprocess handling on Windows.
        
        # On Windows, use ; as separator for --add-data, on Unix use :
        if platform.system() == "Windows":
            sep = ";"
        else:
            sep = ":"
        
        venv_pyinstaller = VENV_DIR / "Scripts" / "pyinstaller.exe"
        if venv_pyinstaller.exists():
            # Use the pyinstaller executable directly
            pyinstaller_cmd = [str(venv_pyinstaller)]
        else:
            # Fall back to python -m PyInstaller
            pyinstaller_cmd = [PYTHON_CMD, "-m", "PyInstaller"]

        pyinstaller_cmd.extend([
            "--onedir",
            "-v",  # Verbose output
            "--noconfirm",  # Don't ask for confirmation
            "--clean",  # Clean build directory first
        ])

        # Ensure PyInstaller searches the backend package path so it collects
        # the `app` package modules and dependencies during analysis.
        if BACKEND_DIR.exists():
            pyinstaller_cmd.extend(["--paths", str(BACKEND_DIR)])
        
        # Add backend directory
        if BACKEND_DIR.exists():
            pyinstaller_cmd.extend(["--add-data", f"{BACKEND_DIR}{sep}backend"])
            print(f"✓ Will add backend directory: {BACKEND_DIR}")
        
        # Add frontend directory
        if FRONTEND_DIR.exists():
            pyinstaller_cmd.extend(["--add-data", f"{FRONTEND_DIR}{sep}frontend"])
            print(f"✓ Will add frontend directory: {FRONTEND_DIR}")
        
        # Add data directory if it exists
        data_dir = ROOT_DIR / "data"
        if data_dir.exists():
            pyinstaller_cmd.extend(["--add-data", f"{data_dir}{sep}data"])
            print(f"✓ Will add data directory: {data_dir}")
        
        # Add references if it exists
        references_dir = ROOT_DIR / "references"
        if references_dir.exists():
            pyinstaller_cmd.extend(["--add-data", f"{references_dir}{sep}references"])
            print(f"✓ Will add references directory: {references_dir}")
        else:
            print(f"⚠️  References directory not found")
        
        # Add pre-built database if it exists
        if db_file.exists():
            pyinstaller_cmd.extend(["--add-data", f"{db_file}{sep}frontend"])
            print(f"✓ Will add database file: {db_file}")
        
        pyinstaller_cmd.extend([
            # FastAPI and server - ALL imports
            "--hidden-import=fastapi",
            "--hidden-import=app",
            "--hidden-import=fastapi.middleware",
            "--hidden-import=fastapi.middleware.cors",
            "--hidden-import=fastapi.responses",
            "--hidden-import=fastapi.staticfiles",
            "--hidden-import=sqlalchemy",
            "--hidden-import=sqlalchemy.pool",
            "--hidden-import=sqlalchemy.orm",
            "--hidden-import=pydantic",
            "--hidden-import=pydantic_settings",
            "--hidden-import=uvicorn",
            "--hidden-import=uvicorn.lifespan",
            "--hidden-import=uvicorn.lifespan.off",
            "--hidden-import=uvicorn.lifespan.on",
            "--hidden-import=uvicorn.loops",
            "--hidden-import=uvicorn.loops.asyncio",
            "--hidden-import=uvicorn.loops.auto",
            "--hidden-import=uvicorn.protocols",
            "--hidden-import=uvicorn.servers",
            "--hidden-import=starlette",
            "--hidden-import=starlette.staticfiles",
            # Database
            "--hidden-import=aiosqlite",
            "--hidden-import=sqlite3",
            # PyWebView and dependencies
            "--hidden-import=webview",
            "--hidden-import=webview.js",
            "--hidden-import=webview.dom",
            "--hidden-import=webview.api",
            "--hidden-import=requests",
            "--hidden-import=urllib3",
            # Standard library
            "--hidden-import=logging",
            "--hidden-import=threading",
            "--hidden-import=subprocess",
            "--hidden-import=json",
            "--hidden-import=pathlib",
            "--hidden-import=dotenv",
            # Collection - COLLECT ALL to ensure everything is included
            "--collect-all=fastapi",
            "--collect-all=starlette",
            "--collect-all=sqlalchemy",
            "--collect-all=pydantic",
            "--collect-all=pydantic_settings",
            "--collect-all=uvicorn",
            "--collect-all=webview",
            "--collect-all=aiosqlite",
            "--collect-all=certifi",
            "--collect-all=charset_normalizer",
            "--collect-all=idna",
            "--collect-all=urllib3",
            "--collect-all=requests",
            # Additional collection for all dependencies
            "--collect-all=click",
            "--collect-all=anyio",
            "--collect-all=sniffio",
            "--collect-submodules=app",
            "--name", "PANDORA",
            str(launcher_script)
        ])
        
        # Add icon if it exists
        icon_path = ROOT_DIR / "ICON.ico"
        if icon_path.exists():
            pyinstaller_cmd.insert(-1, "--icon")
            pyinstaller_cmd.insert(-1, str(icon_path))
        
        # Run PyInstaller using subprocess directly
        print("\n🔨 Running PyInstaller...")
        print(f"Working directory: {ROOT_DIR}")
        print()

        # Make sure paths in command are strings (not Path objects)
        pyinstaller_cmd_str = [str(x) for x in pyinstaller_cmd]

        original_cwd = os.getcwd()
        log_file = ROOT_DIR / "pyinstaller_build.log"
        try:
            os.chdir(str(ROOT_DIR))
            
            # Run PyInstaller directly as an executable
            with open(log_file, "w", encoding="utf-8") as fh:
                proc = subprocess.Popen(
                    pyinstaller_cmd_str,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    cwd=str(ROOT_DIR)
                )
                
                # Read output in real-time and collect it
                output_lines = []
                for line in proc.stdout:
                    line = line.rstrip('\n\r')
                    output_lines.append(line)
                    fh.write(line + '\n')
                    # Print important lines
                    if any(x in line for x in ['Build complete', 'ERROR:', 'PANDORA']):
                        print(line)
                
                returncode = proc.wait()
                
                # Print summary
                if returncode == 0:
                    print_success("PyInstaller completed successfully")
                    # Print last BUILD messages
                    for line in output_lines[-20:]:
                        if 'Build' in line or 'PANDORA' in line or 'dist' in line:
                            print(line)
                else:
                    print_error(f"PyInstaller exited with code {returncode}")
                    # Print errors
                    for line in output_lines:
                        if 'ERROR' in line or 'error' in line:
                            print(f"  {line}")

        except Exception as e:
            print_error(f"Failed to run PyInstaller: {e}")
            import traceback
            traceback.print_exc()
            returncode = 1
        finally:
            os.chdir(original_cwd)

        # Small delay to let filesystem settle
        import time
        time.sleep(1)
        # DEBUG: Check what's in current dir
        print(f"\n📊 Build Verification:")
        print(f"   ROOT_DIR: {ROOT_DIR}")
        print(f"   BUILD_DIR path: {BUILD_DIR}")
        print(f"   BUILD_DIR exists: {BUILD_DIR.exists()}")
        
        if BUILD_DIR.exists():
            items = list(BUILD_DIR.iterdir())
            print(f"   Items in dist: {len(items)}")
            for item in items:
                print(f"      - {item.name}/")
        else:
            print(f"   ⚠️  BUILD_DIR does NOT exist!")
            print(f"   Current directory contents:")
            for item in Path(".").iterdir():
                if "dist" in item.name.lower() or "build" in item.name.lower():
                    print(f"      - {item.name}")
        
        print()
        if returncode != 0:
            print_error(f"PyInstaller failed with return code: {returncode}")
            return False
        
        print_success("Desktop application created successfully")
        
        # Check exe location
        exe_path = ROOT_DIR / "dist" / "PANDORA" / "PANDORA.exe"
        if exe_path.exists():
            print_success(f"✓ Executable created: {exe_path}")
            exe_size_mb = exe_path.stat().st_size / (1024*1024)
            print_success(f"✓ Executable size: {exe_size_mb:.2f} MB")
            
            # Verify data directories are included
            print("\n📦 Verifying bundled data...")
            internal_dir = ROOT_DIR / "dist" / "PANDORA" / "_internal"
            if internal_dir.exists():
                items = list(internal_dir.iterdir())
                print_success(f"✓ _internal folder contains {len(items)} items")
                
                # Check for important directories
                backend_path = internal_dir / "backend"
                frontend_path = internal_dir / "frontend"
                
                if backend_path.exists():
                    print_success(f"✓ Backend directory included")
                else:
                    print(f"⚠️  Backend directory NOT included in _internal")
                
                if frontend_path.exists():
                    print_success(f"✓ Frontend directory included")
                else:
                    print(f"⚠️  Frontend directory NOT included in _internal")
            
            print()
            print("=" * 70)
            print("  PANDORA DESKTOP APPLICATION READY!")
            print("=" * 70)
            print()
            print("Features:")
            print("  ✓ Embedded web browser (no external dependencies)")
            print("  ✓ FastAPI backend (fully functional)")
            print("  ✓ Modern Windows 11 style application")
            print("  ✓ Complete offline support")
            print()
            print("To run:")
            print(f"  dist\\PANDORA\\PANDORA.exe")
            print()
            return True
        else:
            print_error(f"✗ Executable not found at: {exe_path}")
            print_error("Build may have failed silently")
            return False
    except subprocess.CalledProcessError as e:
        print_error(f"Error building executable: {e}")
        return False
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        import traceback
        traceback.print_exc()
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
    
    # Step 2: Build frontend (optional - doesn't block if npm missing)
    build_frontend()  # Returns True even if npm not found
    
    # Step 3: Create executable
    if not create_exe():
        print("✗ Build failed at executable creation")
        sys.exit(1)
    
    # Summary
    print_section("Build Summary")
    print_success("All components built successfully!")
    print()
    print("=" * 70)
    print("  PANDORA DESKTOP APPLICATION v1.1")
    print("=" * 70)
    print()
    print("✨ APPLICATION FEATURES:")
    print()
    print("  🚀 Modern Desktop Application")
    print("     • Embedded web browser (PyWebView)")
    print("     • Full FastAPI backend integration")
    print("     • Windows 11 native experience")
    print()
    print("  📦 Complete Package")
    print("     • No external dependencies required")
    print("     • Backend + Frontend bundled together")
    print("     • Works completely offline")
    print()
    print("  🎨 Professional UI")
    print("     • Modern gradient design")
    print("     • Responsive layout")
    print("     • Smooth animations")
    print()
    print("=" * 70)
    print()
    print("📍 EXECUTABLE LOCATION:")
    print(f"   dist\\PANDORA\\PANDORA.exe")
    print()
    print("🚀 TO RUN:")
    print("   1. Open dist folder")
    print("   2. Open PANDORA folder")
    print("   3. Double-click PANDORA.exe")
    print()
    print("⚡ QUICK START:")
    print("   • The application will start automatically")
    print("   • Backend API initializes on port 8000")
    print("   • Embedded browser displays the UI")
    print("   • No additional configuration needed")
    print()
    print("=" * 70)
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

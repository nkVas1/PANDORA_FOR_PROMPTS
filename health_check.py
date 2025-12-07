#!/usr/bin/env python3
"""
Health check script for PANDORA application
Скрипт для проверки состояния PANDORA приложения
"""

import sys
import subprocess
import socket
import os
from pathlib import Path
import json

class Color:
    GREEN = '\033[92m'
    BLUE = '\033[94m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    CYAN = '\033[96m'
    END = '\033[0m'

def print_header(title):
    print()
    print(f"{Color.BLUE}{'=' * 70}{Color.END}")
    print(f"{Color.BLUE}{title.center(70)}{Color.END}")
    print(f"{Color.BLUE}{'=' * 70}{Color.END}")
    print()

def print_check(name, status, detail=""):
    icon = f"{Color.GREEN}✅{Color.END}" if status else f"{Color.RED}❌{Color.END}"
    detail_str = f" - {detail}" if detail else ""
    print(f"{icon} {name}{detail_str}")

def main():
    root_dir = Path(__file__).parent
    
    print_header("🏥 PANDORA Health Check")
    
    all_ok = True
    
    # 1. Check virtual environment
    print(f"{Color.CYAN}1. Virtual Environment{Color.END}")
    venv_dir = root_dir / "venv"
    venv_exists = venv_dir.exists()
    print_check("venv directory exists", venv_exists, str(venv_dir))
    
    if venv_exists:
        if sys.platform == "win32":
            venv_python = venv_dir / "Scripts" / "python.exe"
        else:
            venv_python = venv_dir / "bin" / "python"
        
        venv_python_exists = venv_python.exists()
        print_check("venv Python executable", venv_python_exists, str(venv_python))
        all_ok &= venv_python_exists
    else:
        print_check("venv directory exists", False, "Run: python reinit_venv.py")
        all_ok = False
    
    # 2. Check backend structure
    print()
    print(f"{Color.CYAN}2. Backend Structure{Color.END}")
    
    backend_dir = root_dir / "backend"
    print_check("backend directory", backend_dir.exists(), str(backend_dir))
    
    app_dir = backend_dir / "app"
    print_check("app directory", app_dir.exists(), str(app_dir))
    
    requirements = backend_dir / "requirements.txt"
    print_check("requirements.txt", requirements.exists(), str(requirements))
    
    run_py = backend_dir / "run.py"
    print_check("run.py", run_py.exists(), str(run_py))
    
    all_ok &= backend_dir.exists() and app_dir.exists() and requirements.exists()
    
    # 3. Check frontend structure
    print()
    print(f"{Color.CYAN}3. Frontend Structure{Color.END}")
    
    frontend_dir = root_dir / "frontend"
    print_check("frontend directory", frontend_dir.exists(), str(frontend_dir))
    
    package_json = frontend_dir / "package.json"
    print_check("package.json", package_json.exists(), str(package_json))
    
    # Check for Next.js app directory (modern) or src directory (older)
    app_dir = frontend_dir / "app"
    src_dir = frontend_dir / "src"
    has_source = app_dir.exists() or src_dir.exists()
    
    if app_dir.exists():
        print_check("app directory (Next.js 13+)", app_dir.exists(), str(app_dir))
    elif src_dir.exists():
        print_check("src directory", src_dir.exists(), str(src_dir))
    else:
        print_check("source directory", False, "Neither app/ nor src/ found")
    
    all_ok &= frontend_dir.exists() and package_json.exists() and has_source
    
    # 4. Check main scripts
    print()
    print(f"{Color.CYAN}4. Main Scripts{Color.END}")
    
    start_py = root_dir / "start.py"
    print_check("start.py", start_py.exists(), str(start_py))
    
    build_py = root_dir / "build.py"
    print_check("build.py", build_py.exists(), str(build_py))
    
    reinit_venv_py = root_dir / "reinit_venv.py"
    print_check("reinit_venv.py", reinit_venv_py.exists(), str(reinit_venv_py))
    
    all_ok &= start_py.exists() and build_py.exists() and reinit_venv_py.exists()
    
    # 5. Check environment file
    print()
    print(f"{Color.CYAN}5. Configuration{Color.END}")
    
    env_file = root_dir / ".env"
    env_exists = env_file.exists()
    print_check(".env file", env_exists, str(env_file) if env_exists else "using .env.example")
    
    # 6. Check dependencies (if venv exists)
    print()
    print(f"{Color.CYAN}6. Python Dependencies (in venv){Color.END}")
    
    if venv_exists and venv_python_exists:
        required_packages = [
            'fastapi',
            'uvicorn',
            'sqlalchemy',
            'pydantic',
        ]
        
        for package in required_packages:
            try:
                result = subprocess.run(
                    [str(venv_python), "-m", "pip", "show", package],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                package_installed = result.returncode == 0
                print_check(package, package_installed)
                all_ok &= package_installed
            except Exception as e:
                print_check(package, False, f"Error: {e}")
                all_ok = False
    else:
        print_check("Python packages", False, "venv not found - run: python reinit_venv.py")
        all_ok = False
    
    # 7. Check ports
    print()
    print(f"{Color.CYAN}7. Required Ports{Color.END}")
    
    ports = {
        "API (backend)": 8000,
        "Frontend": 3000,
    }
    
    for name, port in ports.items():
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            result = sock.connect_ex(('127.0.0.1', port))
            available = result != 0
            print_check(f"Port {port} ({name}) available", available)
        except:
            print_check(f"Port {port} ({name}) available", False)
        finally:
            sock.close()
    
    # 8. Summary
    print()
    print_header("Summary")
    
    if all_ok:
        print(f"{Color.GREEN}✅ All checks passed! Your project is ready.{Color.END}")
        print()
        print(f"Next steps:")
        print(f"  1. Start the application:")
        print(f"     {Color.CYAN}python start.py{Color.END}")
        print(f"  2. Or start backend only:")
        print(f"     {Color.CYAN}python start.py --backend-only{Color.END}")
        print()
        return 0
    else:
        print(f"{Color.RED}❌ Some checks failed. Please review above.{Color.END}")
        print()
        if not venv_exists:
            print(f"Quick fix:")
            print(f"  {Color.CYAN}python reinit_venv.py{Color.END}")
        print()
        return 1

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print()
        print(f"{Color.YELLOW}Cancelled by user{Color.END}")
        sys.exit(1)
    except Exception as e:
        print()
        print(f"{Color.RED}Error: {e}{Color.END}")
        sys.exit(1)

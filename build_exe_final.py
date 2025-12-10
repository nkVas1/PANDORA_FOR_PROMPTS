#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PANDORA v2.0 - Simple EXE Builder
Простой builder без Unicode символов, работает напрямую с PyInstaller
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

# Ensure UTF-8
if sys.platform == 'win32':
    os.environ['PYTHONIOENCODING'] = 'utf-8'

PROJECT_ROOT = Path(__file__).parent
LAUNCHER = PROJECT_ROOT / "desktop" / "launcher.py"
SPEC_FILE = PROJECT_ROOT / "PANDORA.spec"
DIST_DIR = PROJECT_ROOT / "dist"
BUILD_DIR = PROJECT_ROOT / "build"
OUTPUT_FILE = PROJECT_ROOT / "PANDORA_v2.0.exe"

def run_command(cmd, description=""):
    """Run command and handle errors"""
    if description:
        print(f"\n[STEP] {description}")
        print("=" * 70)
    
    try:
        result = subprocess.run(cmd, shell=True, cwd=str(PROJECT_ROOT))
        if result.returncode != 0:
            print(f"[ERROR] Command failed with code {result.returncode}")
            return False
        return True
    except Exception as e:
        print(f"[ERROR] {e}")
        return False

def main():
    print("\n" + "=" * 70)
    print("  PANDORA v2.0 - Simple Windows EXE Builder")
    print("=" * 70)
    
    # Check launcher exists
    if not LAUNCHER.exists():
        print(f"[ERROR] Launcher not found: {LAUNCHER}")
        return False
    
    print(f"[OK] Launcher found: {LAUNCHER.name}")
    
    # Create spec if not exists
    if not SPEC_FILE.exists():
        print("\n[STEP] Generating PANDORA.spec")
        print("=" * 70)
        
        spec_content = f'''# -*- mode: python ; coding: utf-8 -*-
a = Analysis(
    ['{LAUNCHER}'],
    pathex=[],
    binaries=[],
    datas=[
        ('{PROJECT_ROOT / "backend"}', 'backend'),
        ('{PROJECT_ROOT / "frontend"}', 'frontend'),
        ('{PROJECT_ROOT / "data"}', 'data'),
    ],
    hiddenimports=[
        'app',
        'fastapi',
        'uvicorn',
        'sqlalchemy',
        'pydantic',
        'aiosqlite',
        'webview',
    ],
    hookspath=[],
    hooksconfig={{}},
    runtime_hooks=[],
    excludedimports=[],
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=None)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='PANDORA',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
'''
        
        SPEC_FILE.write_text(spec_content)
        print(f"[OK] Created: {SPEC_FILE.name}")
    else:
        print(f"[OK] Using existing: {SPEC_FILE.name}")
    
    # Clean old builds
    print("\n[STEP] Cleaning old build artifacts")
    print("=" * 70)
    
    for path in [BUILD_DIR, DIST_DIR]:
        if path.exists():
            shutil.rmtree(path)
            print(f"[OK] Cleaned: {path.name}")
    
    # Run PyInstaller
    print("\n[STEP] Running PyInstaller")
    print("=" * 70)
    
    cmd = f"pyinstaller {SPEC_FILE} --distpath {DIST_DIR} --workpath {BUILD_DIR} --noconfirm"
    
    if not run_command(cmd):
        return False
    
    # Copy exe to project root
    print("\n[STEP] Finalizing EXE")
    print("=" * 70)
    
    exe_in_dist = DIST_DIR / "PANDORA" / "PANDORA.exe"
    
    if exe_in_dist.exists():
        shutil.copy(exe_in_dist, OUTPUT_FILE)
        size_mb = OUTPUT_FILE.stat().st_size / (1024 * 1024)
        print(f"[OK] EXE created: {OUTPUT_FILE.name}")
        print(f"[OK] Size: {size_mb:.1f} MB")
        
        if size_mb > 600:
            print(f"[WARN] EXE size exceeds 600 MB: {size_mb:.1f} MB")
        
        print("\n" + "=" * 70)
        print("  [SUCCESS] Build completed!")
        print("=" * 70)
        print(f"\nExecutable: {OUTPUT_FILE}")
        print(f"Size: {size_mb:.1f} MB")
        print(f"\nTo run: {OUTPUT_FILE.name}")
        print("=" * 70 + "\n")
        
        return True
    else:
        print(f"[ERROR] EXE not found: {exe_in_dist}")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

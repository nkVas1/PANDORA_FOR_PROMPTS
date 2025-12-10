# -*- mode: python ; coding: utf-8 -*-
"""
PANDORA v2.0 - PyInstaller Specification File
Собирает полнофункциональное Windows приложение с встроенным backend и frontend
"""

from PyInstaller.utils.hooks import collect_data_files, collect_submodules
from pathlib import Path
import os

# Get the absolute path to the project root
PROJECT_ROOT = Path(os.getcwd())

# ==================== CONFIGURATION ====================
block_cipher = None

# Основной скрипт (launcher)
launcher_script = str(PROJECT_ROOT / "desktop" / "launcher.py")

# Дополнительные модули для включения
hidden_modules = [
    # FastAPI ecosystem
    'fastapi',
    'fastapi.middleware',
    'fastapi.staticfiles',
    'fastapi.responses',
    'uvicorn',
    'uvicorn.config',
    'uvicorn.server',
    'uvicorn.protocols.http.auto',
    'uvicorn.protocols.websocket.auto',
    
    # Database
    'sqlalchemy',
    'sqlalchemy.orm',
    'sqlalchemy.ext',
    'sqlalchemy.dialects.sqlite',
    
    # Pydantic (FastAPI validation)
    'pydantic',
    'pydantic_core',
    # Pydantic v2 settings package
    'pydantic_settings',
    
    # Additional dependencies
    'aiofiles',
    'click',
    'h11',
    'starlette',
    'typing_extensions',
    'starlette.middleware.cors',
    'fastapi.middleware.cors',
    
    # Custom modules
    'app',
    'app.main',
    'app.api',
    'app.api.routes',
    'app.db',
    'app.db.database',
    'app.db.models',
    'app.models',
    'app.models.schemas',
    'app.services',
    'app.services.database',
    'app.services.db_initializer',
    'app.services.references_importer',
    'app.config',
    'app.utils',
    'app.logging_config',
]

# ==================== BUILD ANALYSIS ====================
a = Analysis(
    [launcher_script],
    pathex=[str(PROJECT_ROOT)],
    binaries=[],
    datas=[
        # Backend files
        (str(PROJECT_ROOT / "backend" / "app"), "app"),
        
        # Frontend files
        (str(PROJECT_ROOT / "frontend" / "css"), "frontend/css"),
        (str(PROJECT_ROOT / "frontend" / "js"), "frontend/js"),
        (str(PROJECT_ROOT / "frontend" / "index.html"), "frontend"),
        (str(PROJECT_ROOT / "frontend" / "src"), "frontend/src"),
        (str(PROJECT_ROOT / "frontend" / "styles"), "frontend/styles"),
        (str(PROJECT_ROOT / "frontend" / "lib"), "frontend/lib"),
        
        # Data files
        (str(PROJECT_ROOT / "data"), "data"),
    ],
    hiddenimports=hidden_modules,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludedimports=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# ==================== Build PYZ ====================
pyz = PYZ(
    a.pure,
    a.zipped_data,
    cipher=block_cipher
)

# ==================== Build EXE ====================
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
    console=False,  # No console window
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # Could add icon later
)

# ==================== Build COLLECT ====================
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='PANDORA'
)

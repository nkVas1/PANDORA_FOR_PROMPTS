#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from pathlib import Path

print(f"CWD: {os.getcwd()}")
print(f"__file__: {__file__}")
print(f"sys.executable: {sys.executable}")

# Проверим, где находится pyrootdir для exe
import pyinstaller_getpath
print(f"PyInstaller root: {pyinstaller_getpath.PyInstaller}")

# Проверим, где ищется папка references
from pathlib import Path
current = Path.cwd()
print(f"\n--- Checking from CWD ({current}) ---")
while current != current.parent:
    references_dir = current / "references"
    if references_dir.exists():
        print(f"Found references at: {references_dir}")
        break
    print(f"Checked: {current} - no references")
    current = current.parent

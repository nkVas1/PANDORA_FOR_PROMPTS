#!/usr/bin/env python3
"""Минимальный тест PyInstaller"""
import subprocess
import os
import sys
from pathlib import Path

ROOT = Path(__file__).parent
VENV = ROOT / "venv" / "Scripts" / "python.exe"

print(f"Root: {ROOT}")
print(f"VENV: {VENV}")
print(f"Current dir: {os.getcwd()}")

cmd = [
    str(VENV), "-m", "PyInstaller",
    "--onedir",
    "--clean",
    "--name", "TEST",
    str(ROOT / "launcher_final.py")
]

print(f"Command: {cmd}")
print(f"Running from: {ROOT}")

# Method 1: with cwd
result = subprocess.run(cmd, cwd=str(ROOT))
print(f"Return code: {result.returncode}")

print(f"\nChecking for dist/TEST...")
if (ROOT / "dist" / "TEST").exists():
    print("✓ dist/TEST exists!")
    files = list((ROOT / "dist" / "TEST").iterdir())
    print(f"  Contains {len(files)} items")
else:
    print("✗ dist/TEST does NOT exist")

# Check current directory  
print(f"\nCurrent dir after build: {os.getcwd()}")
print(f"dist folder exists: {(ROOT / 'dist').exists()}")
if (ROOT / "dist").exists():
    print(f"dist contents: {list((ROOT / 'dist').iterdir())}")

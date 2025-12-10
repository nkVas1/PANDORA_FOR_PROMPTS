#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PANDORA v2.0 Quick Development Test Script
Быстрое тестирование структуры проекта перед запуском
"""

import os
import sys
from pathlib import Path

# ==================== АНСИ ЦВЕТА ====================
class Color:
    GREEN = '\033[92m'
    BLUE = '\033[94m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    CYAN = '\033[96m'
    END = '\033[0m'

def print_header(text):
    print(f"\n{Color.CYAN}{'='*60}{Color.END}")
    print(f"{Color.CYAN}{text:^60}{Color.END}")
    print(f"{Color.CYAN}{'='*60}{Color.END}\n")

def print_ok(text):
    print(f"{Color.GREEN}✓ {text}{Color.END}")

def print_error(text):
    print(f"{Color.RED}✗ {text}{Color.END}")

def print_warn(text):
    print(f"{Color.YELLOW}⚠ {text}{Color.END}")

def print_info(text):
    print(f"{Color.BLUE}ℹ {text}{Color.END}")

# ==================== ПРОВЕРКИ ====================

def check_project_structure():
    """Проверить структуру проекта"""
    print_header("Проверка структуры проекта")
    
    required_files = {
        'desktop/launcher.py': 'Desktop launcher',
        'desktop/build.py': 'Build script',
        'frontend/dist/index.html': 'HTML entry point',
        'frontend/src/core/app.js': 'Application bootstrap',
        'frontend/src/core/router.js': 'Router module',
        'frontend/src/views/Dashboard.js': 'Dashboard view',
        'frontend/src/views/PromptsView.js': 'Prompts view',
        'frontend/src/views/ProjectsView.js': 'Projects view',
        'frontend/src/views/EditorView.js': 'Editor view',
        'frontend/src/views/AnalyticsView.js': 'Analytics view',
        'frontend/src/css/tokens.css': 'Design tokens',
        'frontend/src/css/components.css': 'Components styles',
        'frontend/src/css/views.css': 'Views styles',
        'frontend/src/css/animations.css': 'Animations',
    }
    
    root = Path(__file__).parent.absolute()
    issues = []
    
    for file_path, description in required_files.items():
        full_path = root / file_path
        if full_path.exists():
            size = full_path.stat().st_size
            if size > 0:
                print_ok(f"{description:40} ({size:>6} bytes)")
            else:
                print_error(f"{description:40} (EMPTY FILE)")
                issues.append(f"{description} is empty")
        else:
            print_error(f"{description:40} (MISSING)")
            issues.append(f"{description} not found")
    
    return len(issues) == 0, issues

def check_file_contents():
    """Проверить содержимое ключевых файлов"""
    print_header("Проверка содержимого файлов")
    
    root = Path(__file__).parent.absolute()
    checks = {
        'frontend/dist/index.html': ['<div id="app">', '<script', 'app.js'],
        'frontend/src/core/app.js': ['initApp', 'Router', 'import'],
        'frontend/src/views/PromptsView.js': ['PromptsView', 'prompts-list', '/api/prompts'],
        'frontend/src/views/ProjectsView.js': ['ProjectsView', 'projects-container', '/api/projects'],
        'frontend/src/views/EditorView.js': ['EditorView', 'editor-preview', 'auto-save'],
        'frontend/src/views/AnalyticsView.js': ['AnalyticsView', 'analytics-dashboard', '/api/analytics'],
        'frontend/src/css/tokens.css': ['--color-primary', '--font-family-base', '--spacing'],
        'frontend/src/css/components.css': ['.btn', '.card', '.form-input'],
        'frontend/src/css/views.css': ['.prompts-', '.projects-', '.editor-', '.analytics-'],
        'frontend/src/css/animations.css': ['@keyframes', 'slideInUp', 'fadeIn'],
    }
    
    issues = []
    
    for file_path, required_strings in checks.items():
        full_path = root / file_path
        
        if not full_path.exists():
            print_error(f"{file_path:40} (NOT FOUND)")
            issues.append(f"{file_path} doesn't exist")
            continue
        
        with open(full_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        file_ok = True
        for required in required_strings:
            if required not in content:
                print_warn(f"  Missing: {required}")
                file_ok = False
                issues.append(f"{file_path} missing '{required}'")
        
        if file_ok:
            print_ok(f"{file_path:40} (all checks passed)")
        else:
            print_error(f"{file_path:40} (some checks failed)")
    
    return len(issues) == 0, issues

def check_git_status():
    """Проверить git статус"""
    print_header("Проверка Git статуса")
    
    root = Path(__file__).parent.absolute()
    os.chdir(root)
    
    # Проверить последний коммит
    import subprocess
    
    try:
        result = subprocess.run(['git', 'log', '--oneline', '-1'], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            commit = result.stdout.strip()
            print_ok(f"Last commit: {commit}")
            return True
        else:
            print_error("Failed to get git log")
            return False
    except Exception as e:
        print_warn(f"Git check failed: {e}")
        return False

def check_python_dependencies():
    """Проверить Python зависимости"""
    print_header("Проверка Python зависимостей")
    
    required = ['fastapi', 'uvicorn', 'sqlalchemy', 'pywebview']
    missing = []
    
    for package in required:
        try:
            __import__(package)
            print_ok(f"{package:30} installed")
        except ImportError:
            print_error(f"{package:30} NOT INSTALLED")
            missing.append(package)
    
    if missing:
        print_warn(f"\nInstall missing packages with:")
        print(f"  pip install {' '.join(missing)}")
    
    return len(missing) == 0, missing

def generate_report(structure_ok, structure_issues, 
                   content_ok, content_issues,
                   git_ok, deps_ok, deps_missing):
    """Генерировать финальный отчет"""
    print_header("Финальный отчет")
    
    if structure_ok and content_ok and git_ok and deps_ok:
        print(f"{Color.GREEN}✓ ВСЕ ПРОВЕРКИ ПРОЙДЕНЫ{Color.END}\n")
        print_info("Проект готов к запуску:")
        print("  1. python start.py          # Запустить dev сервер")
        print("  2. python desktop/build.py  # Собрать EXE")
        return 0
    else:
        print(f"{Color.RED}✗ ОБНАРУЖЕНЫ ПРОБЛЕМЫ:{Color.END}\n")
        
        if not structure_ok:
            print(f"{Color.RED}Структура проекта:{Color.END}")
            for issue in structure_issues:
                print(f"  • {issue}")
        
        if not content_ok:
            print(f"{Color.RED}Содержимое файлов:{Color.END}")
            for issue in content_issues[:5]:  # Max 5 issues
                print(f"  • {issue}")
            if len(content_issues) > 5:
                print(f"  ... and {len(content_issues) - 5} more")
        
        if not git_ok:
            print(f"{Color.YELLOW}Git:{Color.END}")
            print("  • Failed to get git status")
        
        if not deps_ok:
            print(f"{Color.YELLOW}Dependencies:{Color.END}")
            for pkg in deps_missing:
                print(f"  • {pkg} not installed")
        
        return 1

# ==================== ГЛАВНАЯ ФУНКЦИЯ ====================

def main():
    print(f"\n{Color.CYAN}PANDORA v2.0 - Development Test Script{Color.END}")
    print(f"{Color.CYAN}Testing project structure and readiness{Color.END}\n")
    
    # Проверки
    structure_ok, structure_issues = check_project_structure()
    content_ok, content_issues = check_file_contents()
    git_ok = check_git_status()
    deps_ok, deps_missing = check_python_dependencies()
    
    # Отчет
    exit_code = generate_report(
        structure_ok, structure_issues,
        content_ok, content_issues,
        git_ok, deps_ok, deps_missing
    )
    
    return exit_code

if __name__ == '__main__':
    sys.exit(main())

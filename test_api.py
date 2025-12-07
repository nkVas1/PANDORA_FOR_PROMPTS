#!/usr/bin/env python3
"""
PANDORA API Testing Script
Тестирует все CRUD операции без необходимости запуска GUI
"""

import requests
import json
import time
import sys
from pathlib import Path

API_BASE = "http://127.0.0.1:8000"
API_STATS = f"{API_BASE}/api/stats"
API_PROMPTS = f"{API_BASE}/api/prompts"
API_PROJECTS = f"{API_BASE}/api/projects"
API_TAGS = f"{API_BASE}/api/tags"

# Colors for terminal
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    END = '\033[0m'

def print_header(text):
    print(f"\n{Colors.CYAN}{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}{Colors.END}\n")

def print_success(text):
    print(f"{Colors.GREEN}✅ {text}{Colors.END}")

def print_error(text):
    print(f"{Colors.RED}❌ {text}{Colors.END}")

def print_info(text):
    print(f"{Colors.BLUE}ℹ️  {text}{Colors.END}")

def wait_for_api(max_retries=30):
    """Ожидает пока API будет доступен"""
    print_info("Ожидаю доступности API...")
    for i in range(max_retries):
        try:
            response = requests.get(API_STATS, timeout=2)
            if response.status_code == 200:
                print_success("API доступен!")
                return True
        except requests.exceptions.RequestException:
            sys.stdout.write(f"\r  Попытка {i+1}/{max_retries}...")
            sys.stdout.flush()
            time.sleep(1)
    
    print_error("API недоступен после 30 попыток!")
    return False

def test_stats():
    """Тестирует получение статистики"""
    print_header("Тест 1: Получение статистики")
    try:
        response = requests.get(API_STATS)
        response.raise_for_status()
        data = response.json()
        
        print_success("Статистика загружена")
        print(f"  Промптов: {data.get('total_prompts', 0)}")
        print(f"  Проектов: {data.get('total_projects', 0)}")
        print(f"  Тегов: {data.get('total_tags', 0)}")
        print(f"  Категорий: {data.get('total_categories', 0)}")
        return True
    except Exception as e:
        print_error(f"Ошибка: {e}")
        return False

def test_create_prompt():
    """Тестирует создание промпта"""
    print_header("Тест 2: Создание промпта")
    try:
        prompt_data = {
            "title": "Test Prompt для котов",
            "description": "Описание тестового промпта",
            "content": "Напиши смешную историю про кота который украл пиццу",
            "category": "custom",
            "version": "1.0",
            "tag_ids": []
        }
        
        response = requests.post(API_PROMPTS, json=prompt_data)
        response.raise_for_status()
        data = response.json()
        
        print_success("Промпт создан успешно")
        print(f"  ID: {data.get('id')}")
        print(f"  Название: {data.get('title')}")
        
        return data.get('id')
    except Exception as e:
        print_error(f"Ошибка: {e}")
        return None

def test_read_prompts():
    """Тестирует получение списка промптов"""
    print_header("Тест 3: Получение списка промптов")
    try:
        response = requests.get(API_PROMPTS)
        response.raise_for_status()
        data = response.json()
        
        print_success(f"Получено {len(data)} промптов")
        for prompt in data[:3]:
            print(f"  - {prompt.get('name')}")
        
        return len(data) > 0
    except Exception as e:
        print_error(f"Ошибка: {e}")
        return False

def test_update_prompt(prompt_id):
    """Тестирует обновление промпта"""
    print_header("Тест 4: Обновление промпта")
    try:
        updated_data = {
            "name": "Обновлённый промпт для котов 🐱",
            "description": "Обновлённое описание",
            "content": "Обновлённое содержание промпта",
            "tags": "AI, Кошки, Обновлено"
        }
        
        response = requests.put(f"{API_PROMPTS}/{prompt_id}", json=updated_data)
        response.raise_for_status()
        
        print_success("Промпт обновлён успешно")
        return True
    except Exception as e:
        print_error(f"Ошибка: {e}")
        return False

def test_delete_prompt(prompt_id):
    """Тестирует удаление промпта"""
    print_header("Тест 5: Удаление промпта")
    try:
        response = requests.delete(f"{API_PROMPTS}/{prompt_id}")
        response.raise_for_status()
        
        print_success("Промпт удалён успешно")
        return True
    except Exception as e:
        print_error(f"Ошибка: {e}")
        return False

def test_create_project():
    """Тестирует создание проекта"""
    print_header("Тест 6: Создание проекта")
    try:
        project_data = {
            "name": "AI Assistant Project",
            "description": "Проект по созданию AI ассистента"
        }
        
        response = requests.post(API_PROJECTS, json=project_data)
        response.raise_for_status()
        data = response.json()
        
        print_success("Проект создан успешно")
        print(f"  ID: {data.get('id')}")
        print(f"  Название: {data.get('name')}")
        
        return data.get('id')
    except Exception as e:
        print_error(f"Ошибка: {e}")
        return None

def test_read_projects():
    """Тестирует получение списка проектов"""
    print_header("Тест 7: Получение списка проектов")
    try:
        response = requests.get(API_PROJECTS)
        response.raise_for_status()
        data = response.json()
        
        print_success(f"Получено {len(data)} проектов")
        for project in data[:3]:
            print(f"  - {project.get('name')}")
        
        return len(data) > 0
    except Exception as e:
        print_error(f"Ошибка: {e}")
        return False

def test_read_tags():
    """Тестирует получение списка тегов"""
    print_header("Тест 8: Получение списка тегов")
    try:
        response = requests.get(API_TAGS)
        response.raise_for_status()
        data = response.json()
        
        print_success(f"Получено {len(data)} тегов")
        for tag in data[:5]:
            print(f"  - {tag.get('name')}")
        
        return len(data) >= 0
    except Exception as e:
        print_error(f"Ошибка: {e}")
        return False

def main():
    """Главная функция тестирования"""
    print(f"{Colors.CYAN}")
    print(r"""
    ██████╗  █████╗ ███╗   ██╗██████╗  ██████╗ ██████╗  █████╗ 
    ██╔══██╗██╔══██╗████╗  ██║██╔══██╗██╔═══██╗██╔══██╗██╔══██╗
    ██████╔╝███████║██╔██╗ ██║██║  ██║██║   ██║██████╔╝███████║
    ██╔═══╝ ██╔══██║██║╚██╗██║██║  ██║██║   ██║██╔══██╗██╔══██║
    ██║     ██║  ██║██║ ╚████║██████╔╝╚██████╔╝██║  ██║██║  ██║
    ╚═╝     ╚═╝  ╚═╝╚═╝  ╚═══╝╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝
    
    API TESTING SUITE v1.0
    """)
    print(f"{Colors.END}")
    
    # Ждём пока API будет доступен
    if not wait_for_api():
        return False
    
    results = []
    
    # Тест 1: Статистика
    results.append(("Статистика", test_stats()))
    
    # Тест 2-5: CRUD для промптов
    prompt_id = test_create_prompt()
    results.append(("Создание промпта", prompt_id is not None))
    
    results.append(("Получение промптов", test_read_prompts()))
    
    if prompt_id:
        results.append(("Обновление промпта", test_update_prompt(prompt_id)))
        results.append(("Удаление промпта", test_delete_prompt(prompt_id)))
    
    # Тест 6-7: CRUD для проектов
    project_id = test_create_project()
    results.append(("Создание проекта", project_id is not None))
    
    results.append(("Получение проектов", test_read_projects()))
    
    # Тест 8: Получение тегов
    results.append(("Получение тегов", test_read_tags()))
    
    # Финальный отчёт
    print_header("ИТОГОВЫЙ ОТЧЁТ")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = f"{Colors.GREEN}✅ PASSED{Colors.END}" if result else f"{Colors.RED}❌ FAILED{Colors.END}"
        print(f"  {test_name}: {status}")
    
    print(f"\n  {Colors.CYAN}Пройдено: {passed}/{total}{Colors.END}")
    
    if passed == total:
        print(f"\n{Colors.GREEN}🎉 ВСЕ ТЕСТЫ ПРОЙДЕНЫ!{Colors.END}\n")
        return True
    else:
        print(f"\n{Colors.RED}⚠️  Некоторые тесты не пройдены{Colors.END}\n")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

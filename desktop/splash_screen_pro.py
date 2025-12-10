#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PANDORA v2.0 - Professional Loading Screen
Красивый splash screen с прогресс-баром, анимацией и логами загрузки
Thread-safe версия для безопасного обновления из других потоков
"""

import tkinter as tk
from tkinter import ttk
import threading
import time
from typing import Callable, Optional, List
from datetime import datetime
import sys
import os
from pathlib import Path
import queue


class LoadingScreen:
    """Профессиональный экран загрузки с thread-safe обновлениями"""
    
    def __init__(self, title: str = "PANDORA v2.0", subtitle: str = "Professional Prompt Manager"):
        self.window = tk.Tk()
        self.window.title(title)
        self.window.geometry("700x600")
        self.window.resizable(False, False)
        
        # Center window
        self.window.update_idletasks()
        x = (self.window.winfo_screenwidth() // 2) - (700 // 2)
        y = (self.window.winfo_screenheight() // 2) - (600 // 2)
        self.window.geometry(f"+{x}+{y}")
        
        # Prevent close
        self.window.protocol("WM_DELETE_WINDOW", lambda: None)
        
        # Dark theme
        self.window.configure(bg="#1a1a2e")
        
        # Thread-safe queue для обновлений
        self.update_queue: queue.Queue = queue.Queue()
        self.is_running = True
        
        self.title_text = title
        self.subtitle_text = subtitle
        self.current_step = ""
        self.progress = 0
        self.total_steps = 0
        self.logs: List[str] = []
        
        # Логирование в файл (рядом с EXE в dist/logs)
        # Получаем папку где находится скрипт
        if getattr(sys, 'frozen', False):
            # Если запущен как EXE
            base_dir = Path(sys.executable).parent
        else:
            # Если запущен как скрипт
            base_dir = Path(__file__).parent
        
        self.log_file = base_dir / "logs" / "splash.log"
        self.log_file.parent.mkdir(parents=True, exist_ok=True)
        
        self._write_log_file(f"\n{'='*80}")
        self._write_log_file(f"[{datetime.now()}] PANDORA Splash Screen Started")
        self._write_log_file(f"{'='*80}")
        
        self._create_ui()
        self.window.update()
        
        # Запускаем processing loop для queue
        self._process_queue()
    
    def _write_log_file(self, message: str):
        """Логировать сообщение в файл"""
        try:
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(message + "\n")
        except Exception as e:
            print(f"Failed to write log: {e}", file=sys.stderr)
    
    def _create_ui(self):
        """Создать UI элементы"""
        
        # Главный контейнер
        main_frame = tk.Frame(self.window, bg="#1a1a2e")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=40)
        
        # Logo/Title
        title_label = tk.Label(
            main_frame,
            text=self.title_text,
            font=("Segoe UI", 32, "bold"),
            bg="#1a1a2e",
            fg="#6366f1"
        )
        title_label.pack(pady=(0, 10))
        
        # Subtitle
        subtitle_label = tk.Label(
            main_frame,
            text=self.subtitle_text,
            font=("Segoe UI", 12),
            bg="#1a1a2e",
            fg="#94a3b8"
        )
        subtitle_label.pack(pady=(0, 30))
        
        # Current step
        self.step_label = tk.Label(
            main_frame,
            text="Инициализация...",
            font=("Segoe UI", 11),
            bg="#1a1a2e",
            fg="#cbd5e1"
        )
        self.step_label.pack(pady=(0, 15))
        
        # Progress bar
        progress_frame = tk.Frame(main_frame, bg="#0f172a", height=8)
        progress_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.progress_bar = tk.Canvas(
            progress_frame,
            height=8,
            bg="#0f172a",
            highlightthickness=0
        )
        self.progress_bar.pack(fill=tk.X)
        self.progress_bar.create_rectangle(0, 0, 0, 8, fill="#6366f1", outline="")
        
        # Progress percentage
        self.percent_label = tk.Label(
            main_frame,
            text="0%",
            font=("Segoe UI", 10),
            bg="#1a1a2e",
            fg="#94a3b8"
        )
        self.percent_label.pack(pady=(0, 20))
        
        # Logs section
        logs_label = tk.Label(
            main_frame,
            text="Логи загрузки:",
            font=("Segoe UI", 10, "bold"),
            bg="#1a1a2e",
            fg="#cbd5e1"
        )
        logs_label.pack(anchor=tk.W)
        
        # Log text area
        log_frame = tk.Frame(main_frame, bg="#0f172a", height=150)
        log_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        
        scrollbar = tk.Scrollbar(log_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.log_text = tk.Text(
            log_frame,
            height=8,
            bg="#0f172a",
            fg="#94a3b8",
            font=("Courier New", 9),
            yscrollcommand=scrollbar.set,
            insertwidth=0,
            relief=tk.FLAT,
            borderwidth=1,
            highlightthickness=0
        )
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.log_text.yview)
        
        # Disable editing
        self.log_text.config(state=tk.DISABLED)
    
    def add_log(self, message: str, status: str = "info"):
        """Добавить сообщение в логи (thread-safe через queue)"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        # Color mapping
        colors = {
            "info": "#94a3b8",
            "success": "#10b981",
            "warning": "#f59e0b",
            "error": "#ef4444",
            "step": "#6366f1",
        }
        
        color = colors.get(status, "#94a3b8")
        log_line = f"[{timestamp}] [{status.upper()}] {message}"
        
        # Логировать в файл (безопасно из любого потока)
        self._write_log_file(log_line)
        
        # Добавить в queue для обновления из главного потока
        try:
            self.update_queue.put(("log", {
                "text": log_line,
                "status": status,
                "color": color
            }), block=False)
        except queue.Full:
            pass  # Игнорируем если queue переполнена
        
        self.logs.append(log_line)
    
    def _process_queue(self):
        """Обработать очередь обновлений (thread-safe)"""
        try:
            while self.is_running:
                try:
                    action, data = self.update_queue.get(timeout=0.1)
                    
                    if action == "log" and hasattr(self, 'log_text'):
                        try:
                            text = data.get("text", "")
                            status = data.get("status", "info")
                            color = data.get("color", "#94a3b8")
                            
                            self.log_text.config(state=tk.NORMAL)
                            self.log_text.insert(tk.END, text + "\n", status)
                            self.log_text.tag_configure(status, foreground=color)
                            self.log_text.see(tk.END)
                            self.log_text.config(state=tk.DISABLED)
                        except Exception:
                            pass
                    
                    elif action == "progress" and hasattr(self, 'progress_bar'):
                        try:
                            step = data.get("step", 0)
                            total = data.get("total", 1)
                            step_name = data.get("step_name", "")
                            
                            self.progress = step
                            self.total_steps = total
                            percent = int((step / total) * 100) if total > 0 else 0
                            
                            self.progress_bar['value'] = percent
                            self.step_label.config(text=f"Step {step}/{total}: {step_name}")
                        except Exception:
                            pass
                
                except queue.Empty:
                    pass
                
                # Обновить окно
                try:
                    self.window.update()
                except:
                    break
        
        except:
            pass
        
        if self.window.winfo_exists():
            self.window.after(100, self._process_queue)
    
    def update_progress(self, step: int, total: int, message: str = ""):
        """Обновить прогресс (thread-safe через queue)"""
        try:
            self.update_queue.put(("progress", {
                "step": step,
                "total": total,
                "step_name": message
            }), block=False)
        except queue.Full:
            pass
        
        # Update progress bar
        width = self.progress_bar.winfo_width()
        if width > 1:
            bar_width = int((percent / 100) * width)
            self.progress_bar.delete("bar")
            self.progress_bar.create_rectangle(0, 0, bar_width, 8, fill="#6366f1", outline="", tags="bar")
        
        # Update percentage
        self.percent_label.config(text=f"{percent}%")
        
        # Update step text
        if message:
            self.current_step = message
            self.step_label.config(text=f"Шаг {step}/{total}: {message}")
        
        self.window.update()
    
    def show(self):
        """Показать окно"""
        self.window.deiconify()
    
    def hide(self):
        """Скрыть окно"""
        self.window.withdraw()
    
    def close(self, error_delay: bool = False):
        """Закрыть окно. Если error_delay=True, ждет 10 секунд"""
        try:
            if error_delay:
                # Если была ошибка, даем время на чтение логов
                self._write_log_file(f"\n[ERROR] Waiting 10 seconds before close...")
                self.add_log("Ошибка при запуске. Закрытие через 10 секунд...", "error")
                self.add_log(f"Логи сохранены: {self.log_file}", "info")
                time.sleep(10)
            self.window.destroy()
        except:
            pass
    
    def run_loading_sequence(self, callback: Callable):
        """Запустить callback в отдельном потоке с обновлением UI"""
        def run_in_thread():
            callback(self)
        
        thread = threading.Thread(target=run_in_thread, daemon=True)
        thread.start()
        
        return thread


class InitializationManager:
    """Менеджер инициализации с красивыми логами"""
    
    def __init__(self, splash: LoadingScreen):
        self.splash = splash
        self.steps = []
        self.current_step = 0
    
    def add_step(self, name: str, description: str = ""):
        """Добавить шаг инициализации"""
        self.steps.append({
            "name": name,
            "description": description,
        })
    
    def step(self, index: int, name: str, message: str = ""):
        """Отметить шаг как выполненный"""
        self.current_step = index + 1
        self.splash.update_progress(
            self.current_step,
            len(self.steps),
            name
        )
        if message:
            self.splash.add_log(message, "step")
    
    def log_info(self, message: str):
        """Логировать информацию"""
        self.splash.add_log(message, "info")
    
    def log_success(self, message: str):
        """Логировать успех"""
        self.splash.add_log(f"✓ {message}", "success")
    
    def log_warning(self, message: str):
        """Логировать предупреждение"""
        self.splash.add_log(f"⚠ {message}", "warning")
    
    def log_error(self, message: str):
        """Логировать ошибку"""
        self.splash.add_log(f"✗ {message}", "error")


def create_splash_and_manager():
    """Создать splash screen и менеджер инициализации"""
    splash = LoadingScreen(
        title="PANDORA v2.0",
        subtitle="Professional Prompt Manager"
    )
    
    manager = InitializationManager(splash)
    
    return splash, manager


if __name__ == "__main__":
    # Пример использования
    splash, manager = create_splash_and_manager()
    
    manager.add_step("Проверка окружения", "Проверка Python и зависимостей")
    manager.add_step("Инициализация backend", "Запуск FastAPI сервера")
    manager.add_step("Загрузка базы данных", "Инициализация SQLite")
    manager.add_step("Подготовка frontend", "Загрузка веб-интерфейса")
    manager.add_step("Финализация", "Подготовка к запуску")
    
    def simulate_loading(manager_obj):
        """Имитация загрузки"""
        time.sleep(0.5)
        
        manager_obj.step(0, "Проверка Python версии")
        manager_obj.log_info("Python 3.10.11 обнаружен")
        time.sleep(0.5)
        manager_obj.log_success("Окружение готово")
        
        time.sleep(0.3)
        manager_obj.step(1, "Запуск FastAPI")
        manager_obj.log_info("Инициализация Uvicorn...")
        time.sleep(1)
        manager_obj.log_info("Загрузка приложения...")
        manager_obj.log_success("Backend готов на http://127.0.0.1:8000")
        
        time.sleep(0.3)
        manager_obj.step(2, "Загрузка БД")
        manager_obj.log_info("Открытие pandora.db...")
        time.sleep(0.8)
        manager_obj.log_success("Загружено 1355 промптов")
        
        time.sleep(0.3)
        manager_obj.step(3, "Подготовка frontend")
        manager_obj.log_info("Подключение к серверу...")
        time.sleep(0.6)
        manager_obj.log_success("Frontend готов")
        
        time.sleep(0.3)
        manager_obj.step(4, "Финализация")
        manager_obj.log_info("Очистка и подготовка...")
        time.sleep(0.4)
        manager_obj.log_success("PANDORA готова к работе!")
    
    thread = splash.run_loading_sequence(
        lambda obj: simulate_loading(manager)
    )
    
    splash.window.mainloop()

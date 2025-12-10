#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PANDORA v2.0 - Professional Loading Screen (v3 - Enhanced)
Анимированный splash screen с красивым градиентным фоном и полностью рабочей консолью логов
Thread-safe версия для безопасного обновления из других потоков

Features:
- Анимированный градиентный фон (вместо прогресс-бара)
- Полностью функциональная консоль логов с цветовой разметкой
- Auto-scroll в консоли логов
- Thread-safe обновления через queue
- Логирование в файл (dist/logs/splash.log)
"""

import tkinter as tk
from tkinter import ttk
import threading
import time
from typing import Callable, Optional, List, Dict, Tuple
from datetime import datetime
import sys
import os
from pathlib import Path
import queue
import math
import random


class AnimatedBackground:
    """Анимированный градиентный фон для splash screen"""
    
    def __init__(self, canvas: tk.Canvas, width: int, height: int):
        self.canvas = canvas
        self.width = width
        self.height = height
        self.frame = 0
        self.particles = self._create_particles()
    
    def _create_particles(self) -> List[Dict]:
        """Создать анимированные частицы (они не видны, но задают градиент)"""
        particles = []
        colors = [
            (139, 92, 246),    # Purple
            (236, 72, 153),    # Pink
            (6, 182, 212),     # Cyan
        ]
        
        for i in range(3):
            particles.append({
                "x": random.randint(0, self.width),
                "y": random.randint(0, self.height),
                "vx": random.uniform(-0.5, 0.5),
                "vy": random.uniform(-0.5, 0.5),
                "color": colors[i % len(colors)],
                "size": random.randint(200, 400),
                "opacity": 0.3
            })
        
        return particles
    
    def update_and_draw(self):
        """Обновить и нарисовать анимацию"""
        self.frame += 1
        self.canvas.delete("all")
        
        # Фоновый чёрный цвет
        self.canvas.create_rectangle(0, 0, self.width, self.height, fill="#1a1a2e", outline="")
        
        # Обновить позиции частиц
        for particle in self.particles:
            particle["x"] += particle["vx"]
            particle["y"] += particle["vy"]
            
            # Bounce at edges
            if particle["x"] < 0 or particle["x"] > self.width:
                particle["vx"] *= -1
            if particle["y"] < 0 or particle["y"] > self.height:
                particle["vy"] *= -1
            
            # Добавить волнообразное движение
            wave = math.sin(self.frame * 0.02 + particle["x"] * 0.01) * 20
            particle["y"] += wave * 0.01
        
        # Нарисовать градиентные круги (размытые)
        for particle in self.particles:
            r, g, b = particle["color"]
            
            # Наружный (размытый) круг
            for i in range(particle["size"], 0, -20):
                opacity = int(particle["opacity"] * (1 - (i / particle["size"])) * 255)
                color = f"#{r:02x}{g:02x}{b:02x}"
                
                try:
                    self.canvas.create_oval(
                        particle["x"] - i, particle["y"] - i,
                        particle["x"] + i, particle["y"] + i,
                        fill=color, outline="", stipple=""
                    )
                except tk.TclError:
                    # Ignore if too many objects
                    pass


class LoadingScreen:
    """Профессиональный экран загрузки v3 с анимированным фоном и консолью"""
    
    def __init__(self, title: str = "PANDORA v2.0", subtitle: str = "Professional Prompt Manager"):
        self.window = tk.Tk()
        self.window.title(title)
        self.window.geometry("800x700")
        self.window.resizable(False, False)
        
        # Центрируем окно
        self.window.update_idletasks()
        x = (self.window.winfo_screenwidth() // 2) - (800 // 2)
        y = (self.window.winfo_screenheight() // 2) - (700 // 2)
        self.window.geometry(f"+{x}+{y}")
        
        # Не разрешаем закрывать кнопкой X (только через .close())
        self.window.protocol("WM_DELETE_WINDOW", self._on_window_close)
        
        # Dark theme
        self.window.configure(bg="#1a1a2e")
        
        # Thread-safe queue для обновлений
        self.update_queue: queue.Queue = queue.Queue()
        self.is_running = True
        
        self.title_text = title
        self.subtitle_text = subtitle
        self.current_step = ""
        self.logs: List[str] = []
        
        # Логирование в файл
        if getattr(sys, 'frozen', False):
            base_dir = Path(sys.executable).parent
        else:
            base_dir = Path(__file__).parent
        
        self.log_file = base_dir / "logs" / "splash.log"
        self.log_file.parent.mkdir(parents=True, exist_ok=True)
        
        self._write_log_file(f"\n{'='*80}")
        self._write_log_file(f"[{datetime.now().isoformat()}] PANDORA Splash Screen Started")
        self._write_log_file(f"{'='*80}")
        
        # Элементы UI (будут инициализированы в _create_ui)
        self.log_text = None
        self.step_label = None
        self.animated_canvas = None
        self.animated_bg = None
        
        self._create_ui()
        
        # Показываем окно
        self.window.deiconify()
        self.window.lift()
        self.window.attributes('-topmost', True)
        self.window.update()
        
        # Запускаем processing loop через after() - не блокирует UI
        self._process_queue()
        self._update_animation()
    
    def _write_log_file(self, message: str):
        """Логировать в файл"""
        try:
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(message + "\n")
                f.flush()
        except Exception as e:
            print(f"Failed to write log: {e}", file=sys.stderr)
    
    def _on_window_close(self):
        """Обработка попытки закрыть окно"""
        self.close()
    
    def _create_ui(self):
        """Создать UI"""
        
        # Главный контейнер
        main_frame = tk.Frame(self.window, bg="#1a1a2e")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # === TOP SECTION: Header + Animated Background ===
        header_frame = tk.Frame(main_frame, bg="#1a1a2e", height=180)
        header_frame.pack(fill=tk.X, side=tk.TOP)
        header_frame.pack_propagate(False)
        
        # Анимированный фон (Canvas)
        self.animated_canvas = tk.Canvas(
            header_frame,
            width=800,
            height=180,
            bg="#1a1a2e",
            highlightthickness=0,
            relief=tk.FLAT
        )
        self.animated_canvas.pack(fill=tk.BOTH, expand=True)
        self.animated_bg = AnimatedBackground(self.animated_canvas, 800, 180)
        
        # Текст поверх анимированного фона
        title_frame = tk.Frame(header_frame, bg="#1a1a2e")
        title_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=700, height=160)
        
        title_label = tk.Label(
            title_frame,
            text=self.title_text,
            font=("Segoe UI", 36, "bold"),
            bg="#1a1a2e",
            fg="#6366f1"
        )
        title_label.pack(pady=(10, 0))
        
        subtitle_label = tk.Label(
            title_frame,
            text=self.subtitle_text,
            font=("Segoe UI", 11),
            bg="#1a1a2e",
            fg="#cbd5e1"
        )
        subtitle_label.pack(pady=(5, 10))
        
        # Current step
        self.step_label = tk.Label(
            title_frame,
            text="Инициализация...",
            font=("Segoe UI", 10),
            bg="#1a1a2e",
            fg="#94a3b8"
        )
        self.step_label.pack(pady=(0, 5))
        
        # === BOTTOM SECTION: Logs Console ===
        logs_container = tk.Frame(main_frame, bg="#0f172a")
        logs_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        logs_header = tk.Label(
            logs_container,
            text="▶ Логи загрузки",
            font=("Segoe UI", 9, "bold"),
            bg="#0f172a",
            fg="#6366f1",
            anchor=tk.W
        )
        logs_header.pack(fill=tk.X, padx=10, pady=(8, 5))
        
        # Logs text area (работает!)
        log_frame = tk.Frame(logs_container, bg="#0f172a", relief=tk.FLAT, borderwidth=1)
        log_frame.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbar
        scrollbar = tk.Scrollbar(log_frame, bg="#1e293b", troughcolor="#0f172a", width=12)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Text widget для логов
        self.log_text = tk.Text(
            log_frame,
            height=12,
            bg="#0f172a",
            fg="#cbd5e1",
            font=("Consolas", 9),
            yscrollcommand=scrollbar.set,
            insertwidth=0,
            relief=tk.FLAT,
            borderwidth=0,
            highlightthickness=0,
            padx=8,
            pady=8
        )
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.log_text.yview)
        
        # Конфигурируем теги для разных типов сообщений
        self.log_text.tag_configure("info", foreground="#94a3b8")
        self.log_text.tag_configure("success", foreground="#10b981", font=("Consolas", 9, "bold"))
        self.log_text.tag_configure("warning", foreground="#f59e0b", font=("Consolas", 9, "bold"))
        self.log_text.tag_configure("error", foreground="#ef4444", font=("Consolas", 9, "bold"))
        self.log_text.tag_configure("step", foreground="#6366f1", font=("Consolas", 9, "bold"))
        
        # Disable direct editing
        self.log_text.config(state=tk.DISABLED)
    
    def add_log(self, message: str, status: str = "info"):
        """Добавить сообщение в логи (thread-safe через queue)"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        # Выбираем иконку по типу
        icons = {
            "info": "[ℹ]",
            "success": "[✓]",
            "warning": "[⚠]",
            "error": "[✗]",
            "step": "[➤]",
        }
        icon = icons.get(status, "[•]")
        
        # Форматированное сообщение
        log_line = f"[{timestamp}] {icon} {message}"
        
        # Логировать в файл
        self._write_log_file(log_line)
        
        # Отправить в очередь для обновления UI из главного потока
        try:
            self.update_queue.put(("log", {
                "text": log_line,
                "status": status
            }), block=False)
        except (queue.Full, AttributeError, RuntimeError):
            pass
        
        self.logs.append(log_line)
    
    def _process_queue(self):
        """Обработать очередь обновлений (вызывается периодически)"""
        try:
            while True:
                try:
                    action, data = self.update_queue.get(timeout=0)
                    
                    if action == "log" and self.log_text:
                        try:
                            text = data.get("text", "")
                            status = data.get("status", "info")
                            
                            # Обновляем Text widget
                            self.log_text.config(state=tk.NORMAL)
                            self.log_text.insert(tk.END, text + "\n", status)
                            self.log_text.see(tk.END)  # Auto-scroll to bottom
                            self.log_text.config(state=tk.DISABLED)
                        except Exception as e:
                            pass
                    
                    elif action == "step" and self.step_label:
                        try:
                            step_text = data.get("text", "")
                            self.step_label.config(text=step_text)
                            self.window.update_idletasks()
                        except Exception as e:
                            pass
                
                except queue.Empty:
                    break
        except Exception:
            pass
        
        # Запланируем следующий вызов через after() (не блокирующий)
        if self.is_running:
            self.window.after(50, self._process_queue)
    
    def _update_animation(self):
        """Обновить анимированный фон (вызывается периодически)"""
        try:
            if self.animated_bg and self.is_running:
                self.animated_bg.update_and_draw()
                self.window.update_idletasks()
        except Exception:
            pass
        
        # Следующее обновление
        if self.is_running:
            self.window.after(30, self._update_animation)  # ~33 FPS
    
    def update_step(self, step_name: str):
        """Обновить текущий шаг (thread-safe)"""
        self.current_step = step_name
        try:
            self.update_queue.put(("step", {"text": f"▶ {step_name}"}), block=False)
        except (queue.Full, AttributeError, RuntimeError):
            pass
    
    def show(self):
        """Показать окно"""
        try:
            self.window.deiconify()
            self.window.lift()
            self.window.attributes('-topmost', True)
            self.window.update()
        except Exception as e:
            pass
    
    def hide(self):
        """Скрыть окно"""
        try:
            self.window.withdraw()
        except Exception:
            pass
    
    def close(self, delay: float = 0):
        """Закрыть splash screen"""
        def _do_close():
            self.is_running = False
            try:
                self.window.quit()
                self.window.destroy()
            except Exception:
                pass
        
        if delay > 0:
            self.window.after(int(delay * 1000), _do_close)
        else:
            _do_close()


class InitializationManager:
    """Менеджер инициализации с поддержкой splash screen"""
    
    def __init__(self, splash: Optional[LoadingScreen] = None):
        self.splash = splash
        self.steps: List[Tuple[str, str]] = []
        self.current_step_index = 0
        
        # Логирование
        if splash:
            self.add_log = splash.add_log
        else:
            self.add_log = lambda msg, status="info": None
    
    def add_step(self, step_name: str, description: str = ""):
        """Добавить шаг инициализации"""
        self.steps.append((step_name, description))
    
    def step(self, index: int, name: str, message: str = ""):
        """Отметить шаг как завершенный"""
        if self.splash:
            self.splash.update_step(name)
        
        if message:
            self.add_log(message, "step")
    
    def log_info(self, message: str):
        """Логировать информационное сообщение"""
        self.add_log(message, "info")
    
    def log_success(self, message: str):
        """Логировать успешное сообщение"""
        self.add_log(message, "success")
    
    def log_warning(self, message: str):
        """Логировать предупреждение"""
        self.add_log(message, "warning")
    
    def log_error(self, message: str):
        """Логировать ошибку"""
        self.add_log(message, "error")


def create_splash_and_manager() -> Tuple[Optional[LoadingScreen], Optional[InitializationManager]]:
    """Создать splash screen и менеджер инициализации"""
    try:
        splash = LoadingScreen()
        manager = InitializationManager(splash)
        return splash, manager
    except Exception as e:
        print(f"Failed to create splash screen: {e}", file=sys.stderr)
        return None, None


if __name__ == "__main__":
    # Demo
    splash, manager = create_splash_and_manager()
    
    if splash and manager:
        splash.show()
        
        manager.log_info("Система инициализируется...")
        splash.update_step("Загрузка конфигурации")
        
        for i in range(5):
            time.sleep(0.5)
            manager.log_info(f"Шаг {i+1}/5 завершён")
        
        manager.log_success("✓ Инициализация завершена успешно!")
        splash.update_step("Готово")
        
        time.sleep(2)
        splash.close()

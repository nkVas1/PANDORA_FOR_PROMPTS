#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PANDORA Splash Screen - Optimized Version
Оптимизированный загрузочный экран с плавной анимацией
"""

import tkinter as tk
import math
import time
from typing import Optional


class PandoraSplashScreen:
    """Оптимизированный загрузочный экран PANDORA"""

    def __init__(self, root_window: Optional[tk.Tk] = None):
        """Инициализация splash screen"""
        self.root = root_window or tk.Tk()
        self.root.attributes('-topmost', True)

        # Цветовая схема (темная тема)
        self.bg_color = "#0a0e27"
        self.primary_color = "#6366f1"
        self.accent_color = "#ec4899"
        self.text_color = "#f1f5f9"
        self.text_dim = "#94a3b8"

        # Параметры окна
        self.width = 600
        self.height = 700

        # Центрируем окно на экране
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - self.width) // 2
        y = (screen_height - self.height) // 2

        self.root.geometry(f"{self.width}x{self.height}+{x}+{y}")
        self.root.config(bg=self.bg_color)
        self.root.overrideredirect(True)

        # Canvas для рисования
        self.canvas = tk.Canvas(
            self.root,
            width=self.width,
            height=self.height,
            bg=self.bg_color,
            highlightthickness=0,
            cursor="wait",
        )
        self.canvas.pack(fill="both", expand=True)

        # Состояние анимации
        self.time_offset = 0.0
        self.progress = 0  # 0-100
        self.status_text = "Инициализация..."
        self.status_details = ""
        self.is_running = True

        # Кэш для элементов (избегаем пересоздания)
        self.animation_frame = 0

        # Первый рендер
        self.render()

        # Запустить цикл анимации
        self.animate_loop()

    def _hex_to_rgb(self, hex_color: str) -> tuple:
        """Конвертирует HEX в RGB"""
        hex_color = hex_color.lstrip("#")
        return tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))

    def _rgb_to_hex(self, r: int, g: int, b: int) -> str:
        """Конвертирует RGB в HEX"""
        return f"#{int(r):02x}{int(g):02x}{int(b):02x}"

    def _interpolate_color(self, color1: str, color2: str, ratio: float) -> str:
        """Интерполирует два цвета"""
        r1, g1, b1 = self._hex_to_rgb(color1)
        r2, g2, b2 = self._hex_to_rgb(color2)

        r = r1 + (r2 - r1) * ratio
        g = g1 + (g2 - g1) * ratio
        b = b1 + (b2 - b1) * ratio

        return self._rgb_to_hex(r, g, b)

    def render(self):
        """Отрисовка всех элементов (вызывается каждый кадр)"""
        # Очищаем canvas
        self.canvas.delete("all")

        # 1. Фоновый градиент (статичный)
        self._draw_background()

        # 2. Анимированные элементы фона (орбы)
        self._draw_animated_orbs()

        # 3. Логотип с пульсацией
        self._draw_logo()

        # 4. Заголовок
        self._draw_title()

        # 5. Прогресс бар
        self._draw_progress_bar()

        # 6. Статус текст
        self._draw_status_text()

    def _draw_background(self):
        """Рисует фоновый градиент"""
        for i in range(self.height):
            ratio = i / self.height
            # Плавный переход от синего к более темному синему
            r = int(10 + (20 - 10) * ratio)
            g = int(14 + (25 - 14) * ratio)
            b = int(39 + (50 - 39) * ratio)
            color = self._rgb_to_hex(r, g, b)
            self.canvas.create_line(0, i, self.width, i, fill=color, width=1)

    def _draw_animated_orbs(self):
        """Рисует анимированные орбы в фоне"""
        # Три парящих сферы с разными скоростями
        orbs = [
            {
                "x": self.width * 0.2,
                "y": self.height * 0.15,
                "size": 120,
                "speed": 3.0,
                "color": self.primary_color,
                "phase": 0,
            },
            {
                "x": self.width * 0.8,
                "y": self.height * 0.7,
                "size": 100,
                "speed": 4.0,
                "color": self.accent_color,
                "phase": math.pi / 2,
            },
            {
                "x": self.width * 0.5,
                "y": self.height * 0.5,
                "size": 80,
                "speed": 2.5,
                "color": self.primary_color,
                "phase": math.pi,
            },
        ]

        for orb in orbs:
            # Плавное движение
            offset_x = math.cos(self.time_offset / orb["speed"] + orb["phase"]) * 40
            offset_y = math.sin(self.time_offset / orb["speed"] * 0.7 + orb["phase"]) * 30

            x = orb["x"] + offset_x
            y = orb["y"] + offset_y
            size = orb["size"]

            # Полупрозрачная сфера с размытием
            opacity_ratio = (math.sin(self.time_offset / (orb["speed"] * 2)) + 1) / 2
            opacity_ratio = 0.05 + opacity_ratio * 0.1  # 5%-15% opacity

            # Рисуем градиентный круг (орба)
            color = orb["color"]
            for i in range(int(size), 0, -2):
                alpha = 1 - (i / size)
                alpha = alpha * opacity_ratio * 255
                # В tkinter нет прямой поддержки прозрачности, используем темные версии цвета
                self.canvas.create_oval(
                    x - i, y - i, x + i, y + i, fill=color, outline="", stipple=""
                )

    def _draw_logo(self):
        """Рисует логотип с анимацией пульсации"""
        logo_y = 120
        logo_size = 60

        # Пульсирующий размер
        pulse = math.sin(self.time_offset / 0.8) * 0.1 + 0.95
        current_size = int(logo_size * pulse)

        # Эмодзи логотип
        self.canvas.create_text(
            self.width / 2,
            logo_y,
            text="🎨",
            font=("Arial", current_size),
            fill=self.text_color,
            anchor="center",
        )

    def _draw_title(self):
        """Рисует заголовок приложения"""
        self.canvas.create_text(
            self.width / 2,
            200,
            text="PANDORA",
            font=("Segoe UI", 32, "bold"),
            fill=self.text_color,
            anchor="center",
        )

        self.canvas.create_text(
            self.width / 2,
            240,
            text="Менеджер промптов",
            font=("Segoe UI", 12),
            fill=self.text_dim,
            anchor="center",
        )

    def _draw_progress_bar(self):
        """Рисует прогресс бар с плавной анимацией"""
        bar_width = 320
        bar_height = 6
        bar_x = (self.width - bar_width) / 2
        bar_y = 340

        # Фон прогресс бара
        self.canvas.create_rectangle(
            bar_x - 2,
            bar_y - 2,
            bar_x + bar_width + 2,
            bar_y + bar_height + 2,
            fill="#1a2349",
            outline="",
        )

        # Граница
        self.canvas.create_rectangle(
            bar_x,
            bar_y,
            bar_x + bar_width,
            bar_y + bar_height,
            fill="#1a2349",
            outline="#334155",
            width=1,
        )

        # Заполненная часть с градиентом
        if self.progress > 0:
            filled_width = (bar_width - 4) * (self.progress / 100)

            # Градиент от primary к accent
            steps = max(2, int(filled_width / 4))
            for i in range(steps):
                x_ratio = i / max(steps, 1)
                color = self._interpolate_color(
                    self.primary_color, self.accent_color, x_ratio
                )
                x = bar_x + 2 + (filled_width * x_ratio)
                line_width = max(1, int(filled_width / steps))

                self.canvas.create_line(
                    x, bar_y + 1, x, bar_y + bar_height - 1, fill=color, width=line_width
                )

            # Светящийся эффект в конце бара
            glow_x = bar_x + 2 + filled_width
            glow_color = self._interpolate_color(
                self.accent_color, self.primary_color,
                (math.sin(self.time_offset * 2) + 1) / 2,
            )
            self.canvas.create_oval(
                glow_x - 6, bar_y - 2, glow_x + 6, bar_y + bar_height + 2,
                fill="", outline=glow_color, width=2
            )

        # Процент текст
        self.canvas.create_text(
            self.width / 2,
            bar_y + 25,
            text=f"{int(self.progress)}%",
            font=("Segoe UI", 11, "bold"),
            fill=self.text_color,
            anchor="center",
        )

    def _draw_status_text(self):
        """Рисует текст статуса"""
        # Основной статус
        self.canvas.create_text(
            self.width / 2,
            420,
            text=self.status_text,
            font=("Segoe UI", 11, "bold"),
            fill=self.text_color,
            anchor="center",
        )

        # Детальная информация
        if self.status_details:
            self.canvas.create_text(
                self.width / 2,
                450,
                text=self.status_details,
                font=("Segoe UI", 9),
                fill=self.text_dim,
                anchor="center",
            )

        # Информация о версии в низу
        self.canvas.create_text(
            self.width / 2,
            self.height - 30,
            text="v2.0.0 | Desktop Edition",
            font=("Segoe UI", 8),
            fill="#64748b",
            anchor="center",
        )

    def update_progress(
        self, progress: int, status_text: str = "", status_details: str = ""
    ):
        """Обновить прогресс и статус"""
        self.progress = min(100, max(0, progress))
        if status_text:
            self.status_text = status_text
        if status_details:
            self.status_details = status_details

    def animate_loop(self):
        """Цикл анимации (30 FPS)"""
        if not self.is_running:
            return

        # Обновить время
        self.time_offset += 0.033  # ~30 FPS

        # Рендер
        self.render()

        # Следующий кадр (33ms = ~30 FPS)
        self.root.after(33, self.animate_loop)

    def close(self):
        """Закрыть splash screen"""
        self.is_running = False
        try:
            self.root.destroy()
        except:
            pass

    def show(self):
        """Показать splash screen"""
        try:
            self.root.update()
        except:
            pass

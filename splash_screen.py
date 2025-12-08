#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PANDORA Splash Screen
Красивый загрузочный экран с анимацией
"""

import tkinter as tk
from tkinter import Canvas
import math
import time
from pathlib import Path
import sys

class PandoraSplashScreen:
    """Загрузочный экран PANDORA с красивыми анимациями"""
    
    def __init__(self, root_window=None):
        """
        Инициализация splash screen
        
        Args:
            root_window: Главное окно приложения (если есть)
        """
        self.root = root_window or tk.Tk()
        self.root.attributes('-topmost', True)
        
        # Стилистика проекта
        self.bg_color = "#0a0e27"  # Темный фон
        self.primary_color = "#6366f1"  # Индиго
        self.secondary_color = "#8b5cf6"  # Фиолетовый
        self.accent_color = "#ec4899"  # Розовый
        self.text_color = "#f1f5f9"  # Светлый текст
        
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
        
        # Убираем декорации окна
        self.root.overrideredirect(True)
        
        # Canvas для рисования
        self.canvas = Canvas(
            self.root,
            width=self.width,
            height=self.height,
            bg=self.bg_color,
            highlightthickness=0,
            cursor="wait"
        )
        self.canvas.pack(fill="both", expand=True)
        
        # Анимация переменные
        self.time_offset = 0
        self.progress = 0  # 0-100
        self.status_text = "Инициализация..."
        self.status_details = ""
        
        # Рисуем фон с градиентом
        self._draw_gradient_background()
        
        # Обновляем анимацию
        self.animate_frame = 0
        self.animate()
    
    def _draw_gradient_background(self):
        """Рисует градиентный фон"""
        # Темный градиент от синего к фиолетовому
        for i in range(self.height):
            ratio = i / self.height
            # Интерполяция цветов
            r = int(10 + (99 - 10) * ratio)
            g = int(14 + (88 - 14) * ratio)
            b = int(39 + (246 - 39) * ratio)
            color = f'#{r:02x}{g:02x}{b:02x}'
            self.canvas.create_line(0, i, self.width, i, fill=color, width=1)
    
    def _hex_to_rgb(self, hex_color):
        """Конвертирует HEX цвет в RGB"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    def _rgb_to_hex(self, r, g, b):
        """Конвертирует RGB в HEX"""
        return f'#{int(r):02x}{int(g):02x}{int(b):02x}'
    
    def _interpolate_color(self, color1, color2, ratio):
        """Интерполирует два цвета"""
        r1, g1, b1 = self._hex_to_rgb(color1)
        r2, g2, b2 = self._hex_to_rgb(color2)
        
        r = r1 + (r2 - r1) * ratio
        g = g1 + (g2 - g1) * ratio
        b = b1 + (b2 - b1) * ratio
        
        return self._rgb_to_hex(r, g, b)
    
    def _draw_liquid_cloud(self):
        """Рисует анимированное жидкостное облако с переливающимся градиентом"""
        center_x = self.width / 2
        center_y = 150
        
        # Основной размер облака
        base_size = 80
        
        # Создаем волнистую форму облака из Безье кривых
        points = []
        segments = 20
        
        for i in range(segments + 1):
            angle = (i / segments) * 2 * math.pi
            
            # Волнистая радиус с анимацией
            wave1 = math.sin(angle * 3 + self.time_offset) * 15
            wave2 = math.sin(angle * 5 + self.time_offset * 0.7) * 10
            
            radius = base_size + wave1 + wave2
            
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle) * 0.6
            
            points.append((x, y))
        
        # Рисуем градиентное облако несколькими слоями
        # Внешний слой - более прозрачный
        for layer in range(1, 0, -1):
            layer_points = []
            shrink_factor = 0.8 + (layer * 0.05)
            
            for x, y in points:
                new_x = center_x + (x - center_x) * shrink_factor
                new_y = center_y + (y - center_y) * shrink_factor
                layer_points.append((new_x, new_y))
            
            # Цвет с переливом
            color_ratio = (math.sin(self.time_offset) + 1) / 2
            color = self._interpolate_color(
                self.primary_color,
                self.accent_color,
                color_ratio
            )
            
            if len(layer_points) > 2:
                # Создаем замкнутый путь
                coords = []
                for x, y in layer_points:
                    coords.extend([x, y])
                
                try:
                    self.canvas.create_polygon(
                        coords,
                        fill=color,
                        outline="",
                        smooth=True
                    )
                except:
                    pass
        
        # Дополнительные волнистые слои для эффекта жидкости
        for wave_layer in range(3):
            wave_points = []
            wave_phase = self.time_offset + (wave_layer * 0.5)
            
            for i in range(segments + 1):
                angle = (i / segments) * 2 * math.pi
                
                wave1 = math.sin(angle * 3 + wave_phase) * 8
                wave2 = math.sin(angle * 5 + wave_phase * 0.7) * 5
                
                radius = base_size * 0.85 + wave1 + wave2
                
                x = center_x + radius * math.cos(angle)
                y = center_y + radius * math.sin(angle) * 0.6
                
                wave_points.append((x, y))
            
            # Цвет с переливом и прозрачностью
            color_shift = (math.sin(wave_phase * 2) + 1) / 2
            color = self._interpolate_color(
                self.secondary_color,
                self.primary_color,
                color_shift
            )
            
            if len(wave_points) > 2:
                coords = []
                for x, y in wave_points:
                    coords.extend([x, y])
                
                try:
                    self.canvas.create_polygon(
                        coords,
                        fill=color,
                        outline="",
                        smooth=True
                    )
                except:
                    pass
    
    def _draw_logo_text(self):
        """Рисует текст логотипа"""
        # Название
        self.canvas.create_text(
            self.width / 2,
            280,
            text="PANDORA",
            font=("Segoe UI", 42, "bold"),
            fill=self.text_color,
            anchor="center"
        )
        
        # Подзаголовок
        self.canvas.create_text(
            self.width / 2,
            320,
            text="Professional Prompt Management System",
            font=("Segoe UI", 12),
            fill="#a0aec0",
            anchor="center"
        )
        
        # Версия
        self.canvas.create_text(
            self.width / 2,
            340,
            text="v1.2.0 • Desktop Edition",
            font=("Segoe UI", 10),
            fill="#64748b",
            anchor="center"
        )
    
    def _draw_progress_bar(self):
        """Рисует плавный прогресс бар с анимацией"""
        bar_width = 400
        bar_height = 8
        bar_x = (self.width - bar_width) / 2
        bar_y = 410
        
        # Фон прогресс бара с тенью
        self.canvas.create_rectangle(
            bar_x - 2,
            bar_y - 2,
            bar_x + bar_width + 2,
            bar_y + bar_height + 2,
            fill="#0f172a",
            outline="",
            width=0
        )
        
        self.canvas.create_rectangle(
            bar_x,
            bar_y,
            bar_x + bar_width,
            bar_y + bar_height,
            fill="#1e293b",
            outline="#334155",
            width=1
        )
        
        # Заполненная часть с плавным градиентом и сверканием
        if self.progress > 0:
            filled_width = (bar_width - 4) * (self.progress / 100)
            
            # Основной градиент заполнения
            steps = max(10, int(filled_width))
            for i in range(steps):
                ratio = i / max(steps, 1)
                color = self._interpolate_color(
                    self.primary_color,
                    self.accent_color,
                    ratio
                )
                x_pos = bar_x + 2 + (filled_width * ratio)
                line_width = max(1, int(filled_width / steps))
                self.canvas.create_line(
                    x_pos,
                    bar_y + 1,
                    x_pos,
                    bar_y + bar_height - 1,
                    fill=color,
                    width=line_width
                )
            
            # Светящийся эффект с волной в конце бара
            glow_x = bar_x + 2 + filled_width
            
            # Волна света
            wave_intensity = (math.sin(self.time_offset * 2) + 1) / 2
            glow_color = self._interpolate_color(
                self.accent_color,
                self.primary_color,
                wave_intensity
            )
            
            for glow_size in [8, 5, 3]:
                alpha_ratio = 1 - (glow_size / 8)
                self.canvas.create_oval(
                    glow_x - glow_size,
                    bar_y - glow_size // 2,
                    glow_x + glow_size,
                    bar_y + bar_height + glow_size // 2,
                    fill="",
                    outline=glow_color,
                    width=max(1, int(2 - alpha_ratio))
                )
        
        # Процент с анимацией
        pct_text = f"{int(self.progress)}%"
        self.canvas.create_text(
            self.width / 2,
            bar_y + 28,
            text=pct_text,
            font=("Segoe UI", 12, "bold"),
            fill=self.text_color,
            anchor="center"
        )
        
        # Градиентные блики вдоль бара (движущиеся)
        if self.progress > 0 and self.progress < 100:
            glide_pos = (self.time_offset % 1) * (bar_width - 20)
            self.canvas.create_rectangle(
                bar_x + 2 + glide_pos,
                bar_y + 1,
                bar_x + 22 + glide_pos,
                bar_y + bar_height - 1,
                fill="#ffffff",
                outline="",
                width=0
            )
    
    def _draw_status(self):
        """Рисует статус информацию с плавной анимацией"""
        # Основной статус с эффектом
        self.canvas.create_text(
            self.width / 2,
            470,
            text=self.status_text,
            font=("Segoe UI", 11, "bold"),
            fill=self.text_color,
            anchor="center"
        )
        
        # Детали с легким свечением
        if self.status_details:
            # Эффект мерцания для деталей
            glow_ratio = (math.sin(self.time_offset) + 1) / 2
            detail_color = self._interpolate_color(
                "#94a3b8",
                "#cbd5e1",
                glow_ratio * 0.3
            )
            
            self.canvas.create_text(
                self.width / 2,
                492,
                text=self.status_details,
                font=("Segoe UI", 9),
                fill=detail_color,
                anchor="center"
            )
        
        # Плавная анимация индикатора загрузки (пульсирующие точки)
        dots_count = (self.animate_frame // 8) % 4
        dots = "●" * dots_count + "○" * (3 - dots_count)
        
        dot_color = self._interpolate_color(
            self.primary_color,
            self.accent_color,
            (math.sin(self.time_offset * 2) + 1) / 2
        )
        
        self.canvas.create_text(
            self.width / 2,
            545,
            text=dots,
            font=("Segoe UI", 12),
            fill=dot_color,
            anchor="center"
        )
    
    def _draw_decorative_elements(self):
        """Рисует декоративные элементы"""
        # Декоративные линии вверху и внизу
        line_width = 100
        line_x = (self.width - line_width) / 2
        
        # Верхняя линия
        self.canvas.create_line(
            line_x,
            380,
            line_x + line_width,
            380,
            fill=self.primary_color,
            width=2
        )
        
        # Нижняя линия
        self.canvas.create_line(
            line_x,
            540,
            line_x + line_width,
            540,
            fill=self.primary_color,
            width=2
        )
        
        # Мерцающие точки вокруг облака
        for i in range(8):
            angle = (i / 8) * 2 * math.pi + self.time_offset
            distance = 120
            
            x = self.width / 2 + distance * math.cos(angle)
            y = 150 + distance * math.sin(angle)
            
            # Размер точки зависит от анимации
            size = 2 + math.sin(self.time_offset + i) * 1.5
            
            brightness = (math.sin(self.time_offset * 2 + i) + 1) / 2
            color = self._interpolate_color(
                self.primary_color,
                self.accent_color,
                brightness
            )
            
            if size > 0:
                self.canvas.create_oval(
                    x - size,
                    y - size,
                    x + size,
                    y + size,
                    fill=color,
                    outline=""
                )
    
    def animate(self):
        """Основной цикл анимации"""
        try:
            # Очищаем холст
            self.canvas.delete("all")
            
            # Рисуем фон
            self._draw_gradient_background()
            
            # Рисуем облако
            self._draw_liquid_cloud()
            
            # Рисуем логотип
            self._draw_logo_text()
            
            # Рисуем декоративные элементы
            self._draw_decorative_elements()
            
            # Рисуем прогресс бар
            self._draw_progress_bar()
            
            # Рисуем статус
            self._draw_status()
            
            # Обновляем время анимации
            self.time_offset += 0.04
            self.animate_frame += 1
            
            # Запланируем следующий кадр
            if self.root.winfo_exists():
                self.root.after(20, self.animate)
        except:
            # Игнорируем ошибки рисования
            if self.root.winfo_exists():
                self.root.after(20, self.animate)
    
    def update_progress(self, progress, status_text="", status_details=""):
        """
        Обновляет прогресс и статус
        
        Args:
            progress: Процент прогресса (0-100)
            status_text: Основной текст статуса
            status_details: Детальная информация
        """
        self.progress = min(100, max(0, progress))
        if status_text:
            self.status_text = status_text
        if status_details:
            self.status_details = status_details
    
    def close(self):
        """Закрывает splash screen"""
        try:
            self.root.destroy()
        except:
            pass
    
    def show(self):
        """Показывает splash screen"""
        try:
            self.root.update()
        except:
            pass


if __name__ == "__main__":
    # Тест splash screen
    root = tk.Tk()
    splash = PandoraSplashScreen(root)
    
    # Симуляция загрузки
    for i in range(0, 101, 5):
        splash.update_progress(
            i,
            "Загружаем PANDORA...",
            f"Инициализация компонента {i//20 + 1}/5"
        )
        time.sleep(0.5)
        splash.show()
    
    time.sleep(1)
    splash.close()

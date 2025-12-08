#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Modern Animated Splash Screen for PANDORA
Современный анимированный загрузочный экран с прогресс-баром
"""

import tkinter as tk
from tkinter import font
import threading
import time
from typing import Optional, Callable


class ModernSplashScreen:
    """Modern splash screen with animated progress, gradient background, and smooth transitions"""
    
    def __init__(self, root: tk.Tk, on_close: Optional[Callable] = None):
        self.root = root
        self.on_close = on_close
        self.root.withdraw()  # Hide default window first
        
        # Window config
        self.width = 600
        self.height = 700
        self.root.geometry(f'{self.width}x{self.height}')
        self.root.resizable(False, False)
        self.root.configure(bg='#0f0f12')
        
        # Remove window decorations
        try:
            self.root.attributes('-topmost', True)
        except:
            pass
        
        # Center window
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (self.width // 2)
        y = (self.root.winfo_screenheight() // 2) - (self.height // 2)
        self.root.geometry(f'{self.width}x{self.height}+{x}+{y}')
        
        # Create canvas for graphics
        self.canvas = tk.Canvas(
            self.root, 
            width=self.width, 
            height=self.height, 
            bg='#0f0f12',
            highlightthickness=0
        )
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Animation state
        self.progress = 0
        self.max_progress = 100
        self.status_text = "Инициализация..."
        self.status_detail = ""
        self.animation_frame = 0
        self.is_running = True
        
        # Fonts
        self.title_font = font.Font(family="Segoe UI", size=28, weight="bold")
        self.status_font = font.Font(family="Segoe UI", size=11)
        self.detail_font = font.Font(family="Segoe UI", size=9)
        self.version_font = font.Font(family="Segoe UI", size=8)
        
        # Colors
        self.primary_color = "#7c3aed"
        self.accent_color = "#a855f7"
        self.secondary_color = "#06b6d4"
        self.text_color = "#e0e0e0"
        self.text_dim = "#808080"
        
        # Start animation loop
        self.animate()
    
    def draw_gradient_background(self):
        """Draw animated gradient background with blobs"""
        # Dark background
        self.canvas.create_rectangle(
            0, 0, self.width, self.height,
            fill='#0f0f12',
            outline=''
        )
        
        # Animated gradient overlay (simulated with rectangles)
        color_intensity = int(20 + 10 * ((self.animation_frame % 60) / 60))
        gradient_color = f'#{color_intensity:02x}{color_intensity:02x}{int(color_intensity * 1.2):02x}'
        
        # Floating gradient shapes
        offset = (self.animation_frame % 360) / 360 * self.width
        self.canvas.create_oval(
            offset - 150, -100, offset + 150, 200,
            fill=self.primary_color,
            outline='',
            stipple='',
            width=0
        )
        
        offset2 = ((self.animation_frame + 180) % 360) / 360 * self.width
        self.canvas.create_oval(
            offset2 - 100, self.height - 200, offset2 + 100, self.height + 100,
            fill=self.secondary_color,
            outline='',
            width=0
        )
    
    def draw_content(self):
        """Draw main content"""
        # Title
        self.canvas.create_text(
            self.width // 2, 80,
            text="✨ PANDORA",
            font=self.title_font,
            fill=self.accent_color,
            anchor='center'
        )
        
        # Subtitle
        self.canvas.create_text(
            self.width // 2, 130,
            text="Professional Prompt Manager",
            font=font.Font(family="Segoe UI", size=12),
            fill=self.text_dim,
            anchor='center'
        )
        
        # Version
        self.canvas.create_text(
            self.width // 2, 155,
            text="v1.2.0 | Desktop Edition",
            font=self.version_font,
            fill=self.text_dim,
            anchor='center'
        )
        
        # Animated loading indicator (spinning dots)
        dot_positions = [150, 210, 270]
        dot_animation = (self.animation_frame // 10) % 3
        for i, pos in enumerate(dot_positions):
            opacity = 255 if i == dot_animation else 100
            dot_color = self.primary_color if i == dot_animation else self.text_dim
            self.canvas.create_oval(
                pos - 8, 300 - 8,
                pos + 8, 300 + 8,
                fill=dot_color,
                outline=''
            )
        
        # Progress bar background
        bar_x1, bar_y1 = 80, 400
        bar_x2, bar_y2 = self.width - 80, 420
        
        # Background bar
        self.canvas.create_rectangle(
            bar_x1, bar_y1, bar_x2, bar_y2,
            fill='#1a1a1f',
            outline='#404050',
            width=1
        )
        
        # Progress fill with gradient effect
        progress_width = (bar_x2 - bar_x1) * (self.progress / self.max_progress)
        
        # Animated gradient in progress bar
        gradient_offset = (self.animation_frame % 30) / 30
        self.canvas.create_rectangle(
            bar_x1, bar_y1, bar_x1 + progress_width, bar_y2,
            fill=self.primary_color,
            outline='',
            width=0
        )
        
        # Glowing effect on progress bar
        if progress_width > 0:
            self.canvas.create_rectangle(
                bar_x1 + progress_width - 20, bar_y1,
                bar_x1 + progress_width, bar_y2,
                fill=self.accent_color,
                outline='',
                width=0
            )
        
        # Progress percentage
        progress_text = f"{self.progress}%"
        self.canvas.create_text(
            self.width // 2, 450,
            text=progress_text,
            font=font.Font(family="Segoe UI", size=10, weight="bold"),
            fill=self.accent_color,
            anchor='center'
        )
        
        # Status text
        self.canvas.create_text(
            self.width // 2, 500,
            text=self.status_text,
            font=self.status_font,
            fill=self.text_color,
            anchor='center',
            width=500
        )
        
        # Detail text
        if self.status_detail:
            self.canvas.create_text(
                self.width // 2, 540,
                text=self.status_detail,
                font=self.detail_font,
                fill=self.text_dim,
                anchor='center',
                width=500
            )
        
        # Bottom info
        self.canvas.create_text(
            self.width // 2, self.height - 40,
            text="⚡ Инициализация вашего AI помощника...",
            font=font.Font(family="Segoe UI", size=8),
            fill=self.text_dim,
            anchor='center'
        )
    
    def animate(self):
        """Animation loop"""
        if not self.is_running:
            return
        
        # Clear canvas
        self.canvas.delete("all")
        
        # Draw elements
        self.draw_gradient_background()
        self.draw_content()
        
        # Update animation frame
        self.animation_frame += 1
        
        # Schedule next frame (30 FPS)
        self.root.after(33, self.animate)
    
    def update_progress(self, progress: int, status: str = "", detail: str = ""):
        """Update progress bar and status text"""
        self.progress = min(progress, 100)
        self.status_text = status or self.status_text
        self.status_detail = detail
    
    def show(self):
        """Show the splash screen"""
        try:
            self.root.deiconify()
            self.root.lift()
            self.root.update()
        except:
            pass
    
    def close(self):
        """Close the splash screen"""
        self.is_running = False
        try:
            self.root.destroy()
        except:
            pass
    
    def __del__(self):
        """Cleanup"""
        self.close()


def main():
    """Test the splash screen"""
    root = tk.Tk()
    splash = ModernSplashScreen(root)
    splash.show()
    
    # Simulate loading
    for i in range(0, 101, 5):
        splash.update_progress(i, "Инициализация компонентов...", "Загрузка данных...")
        time.sleep(0.1)
    
    time.sleep(2)
    splash.close()


if __name__ == "__main__":
    main()

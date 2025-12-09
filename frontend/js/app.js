/* ═══════════════════════════════════════════════════════════════════
   PANDORA v2.0 - Theme & UI Manager
   Управление темой, интерактивностью и глобальным состоянием
   ═════════════════════════════════════════════════════════════════ */

class ThemeManager {
  constructor() {
    this.htmlElement = document.documentElement;
    this.storageKey = 'pandora-theme';
    this.themes = ['light', 'dark'];
    this.init();
  }

  init() {
    const savedTheme = this.getSavedTheme();
    const prefersDark = this.getSystemPreference();
    const theme = savedTheme || (prefersDark ? 'dark' : 'light');
    
    this.setTheme(theme);
    this.setupThemeToggle();
    this.watchSystemPreference();
  }

  getSavedTheme() {
    return localStorage.getItem(this.storageKey);
  }

  getSystemPreference() {
    return window.matchMedia('(prefers-color-scheme: dark)').matches;
  }

  setTheme(theme) {
    if (!this.themes.includes(theme)) return;
    
    this.htmlElement.setAttribute('data-theme', theme);
    localStorage.setItem(this.storageKey, theme);
    
    // Dispatch custom event
    document.dispatchEvent(new CustomEvent('theme-changed', { detail: { theme } }));
  }

  toggleTheme() {
    const currentTheme = this.htmlElement.getAttribute('data-theme') || 'light';
    const newTheme = currentTheme === 'light' ? 'dark' : 'light';
    this.setTheme(newTheme);
  }

  getCurrentTheme() {
    return this.htmlElement.getAttribute('data-theme') || 'light';
  }

  setupThemeToggle() {
    const toggleBtn = document.querySelector('[data-action="toggle-theme"]');
    if (toggleBtn) {
      toggleBtn.addEventListener('click', () => this.toggleTheme());
      this.updateThemeToggleIcon(toggleBtn);
    }

    // Listen for theme changes
    document.addEventListener('theme-changed', (e) => {
      const btn = document.querySelector('[data-action="toggle-theme"]');
      if (btn) this.updateThemeToggleIcon(btn);
    });
  }

  updateThemeToggleIcon(btn) {
    const currentTheme = this.getCurrentTheme();
    const icon = currentTheme === 'light' ? '🌙' : '☀️';
    const label = currentTheme === 'light' ? 'Тёмная тема' : 'Светлая тема';
    btn.textContent = icon;
    btn.title = label;
    btn.setAttribute('aria-label', label);
  }

  watchSystemPreference() {
    const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
    mediaQuery.addListener((e) => {
      if (!this.getSavedTheme()) {
        this.setTheme(e.matches ? 'dark' : 'light');
      }
    });
  }
}

/* ═════════════════════════════════════════════════════════════════
   UI MANAGER - Управление интерактивностью
   ═════════════════════════════════════════════════════════════════ */

class UIManager {
  constructor() {
    this.modals = new Map();
    this.toasts = [];
    this.init();
  }

  init() {
    this.setupModals();
    this.setupToasts();
    this.setupMenus();
    this.setupAnimations();
  }

  /* МОДАЛЬНЫЕ ОКНА */
  setupModals() {
    document.addEventListener('click', (e) => {
      const trigger = e.target.closest('[data-modal-trigger]');
      if (trigger) {
        const modalId = trigger.getAttribute('data-modal-trigger');
        this.openModal(modalId);
      }

      const closeBtn = e.target.closest('[data-modal-close]');
      if (closeBtn) {
        const modal = closeBtn.closest('[data-modal]');
        if (modal) {
          const modalId = modal.getAttribute('data-modal');
          this.closeModal(modalId);
        }
      }

      const backdrop = e.target.closest('.modal-backdrop');
      if (backdrop && e.target === backdrop) {
        const modalId = backdrop.getAttribute('data-modal-id');
        this.closeModal(modalId);
      }
    });
  }

  openModal(modalId) {
    const backdrop = document.querySelector(`[data-modal-id="${modalId}"]`);
    if (!backdrop) return;

    backdrop.classList.add('active');
    backdrop.style.display = 'flex';
    document.body.style.overflow = 'hidden';

    // Trigger animation
    const modal = backdrop.querySelector('[data-modal]');
    if (modal) {
      modal.classList.add('animate-zoom-in');
    }

    this.modals.set(modalId, true);
  }

  closeModal(modalId) {
    const backdrop = document.querySelector(`[data-modal-id="${modalId}"]`);
    if (!backdrop) return;

    const modal = backdrop.querySelector('[data-modal]');
    if (modal) {
      modal.classList.remove('animate-zoom-in');
    }

    setTimeout(() => {
      backdrop.classList.remove('active');
      backdrop.style.display = 'none';
      document.body.style.overflow = 'auto';
      this.modals.delete(modalId);
    }, 150);
  }

  closeAllModals() {
    this.modals.forEach((_, modalId) => this.closeModal(modalId));
  }

  /* ТОСТЫ / УВЕДОМЛЕНИЯ */
  setupToasts() {
    // Контейнер создаётся динамически при необходимости
  }

  showToast(message, type = 'info', duration = 3000) {
    // Создаём контейнер если его нет
    let container = document.querySelector('.toast-container');
    if (!container) {
      container = document.createElement('div');
      container.className = 'toast-container';
      document.body.appendChild(container);
    }

    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    
    const icons = {
      success: '✓',
      error: '✕',
      info: 'ℹ',
      warning: '⚠'
    };

    toast.innerHTML = `
      <span class="toast-icon">${icons[type] || '•'}</span>
      <span class="toast-message">${message}</span>
    `;

    container.appendChild(toast);

    setTimeout(() => {
      toast.classList.add('animate-fade-out');
      setTimeout(() => toast.remove(), 150);
    }, duration);

    this.toasts.push(toast);
  }

  /* МЕНЮ И НАВИГАЦИЯ */
  setupMenus() {
    document.addEventListener('click', (e) => {
      // Закрываем открытые меню при клике вне их
      const menuTrigger = e.target.closest('[data-menu-trigger]');
      const menu = e.target.closest('[data-menu]');

      if (!menuTrigger && !menu) {
        document.querySelectorAll('[data-menu]').forEach(m => {
          m.classList.remove('active');
        });
      }

      if (menuTrigger) {
        const menuId = menuTrigger.getAttribute('data-menu-trigger');
        const menuElement = document.querySelector(`[data-menu="${menuId}"]`);
        if (menuElement) {
          menuElement.classList.toggle('active');
        }
      }
    });

    // Sidebar toggle на мобильных
    const sidebarToggle = document.querySelector('[data-sidebar-toggle]');
    if (sidebarToggle) {
      sidebarToggle.addEventListener('click', () => {
        const sidebar = document.querySelector('.sidebar-wrapper');
        if (sidebar) {
          sidebar.classList.toggle('mobile-open');
        }
      });
    }
  }

  /* АНИМАЦИИ */
  setupAnimations() {
    // Intersection Observer для анимаций при скролле
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('in-view');
          observer.unobserve(entry.target);
        }
      });
    }, {
      threshold: 0.1
    });

    document.querySelectorAll('.scroll-fade-in, [data-animate-on-scroll]').forEach(el => {
      observer.observe(el);
    });
  }

  /* ФОКУС НА ЭЛЕМЕНТЕ */
  focusElement(selector) {
    const element = document.querySelector(selector);
    if (element) {
      element.focus();
      element.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
  }
}

/* ═════════════════════════════════════════════════════════════════
   UTILITY FUNCTIONS
   ═════════════════════════════════════════════════════════════════ */

class Utilities {
  /* Дебаунс функции */
  static debounce(func, wait = 300) {
    let timeout;
    return function executedFunction(...args) {
      const later = () => {
        clearTimeout(timeout);
        func(...args);
      };
      clearTimeout(timeout);
      timeout = setTimeout(later, wait);
    };
  }

  /* Троттл функции */
  static throttle(func, limit = 300) {
    let inThrottle;
    return function(...args) {
      if (!inThrottle) {
        func.apply(this, args);
        inThrottle = true;
        setTimeout(() => inThrottle = false, limit);
      }
    };
  }

  /* Анимация числового счётчика */
  static animateNumber(element, target, duration = 1000) {
    const start = parseInt(element.textContent) || 0;
    const increment = (target - start) / (duration / 16);
    let current = start;

    const timer = setInterval(() => {
      current += increment;
      if (current >= target) {
        element.textContent = target.toLocaleString();
        clearInterval(timer);
      } else {
        element.textContent = Math.floor(current).toLocaleString();
      }
    }, 16);
  }

  /* Копирование в буфер обмена */
  static copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
      console.log('Скопировано:', text);
    });
  }

  /* Форматирование даты */
  static formatDate(date, locale = 'ru-RU') {
    return new Date(date).toLocaleDateString(locale, {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  }

  /* Форматирование времени */
  static formatTime(date, locale = 'ru-RU') {
    return new Date(date).toLocaleTimeString(locale, {
      hour: '2-digit',
      minute: '2-digit'
    });
  }

  /* Проверка на mobile */
  static isMobile() {
    return window.innerWidth < 768;
  }

  /* Плавный скролл */
  static smoothScroll(target) {
    const element = typeof target === 'string' 
      ? document.querySelector(target) 
      : target;
    
    if (element) {
      element.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  }
}

/* ═════════════════════════════════════════════════════════════════
   KEYBOARD SHORTCUTS
   ═════════════════════════════════════════════════════════════════ */

class KeyboardShortcuts {
  constructor(uiManager) {
    this.uiManager = uiManager;
    this.shortcuts = new Map();
    this.registerDefaults();
    this.init();
  }

  registerDefaults() {
    // Ctrl/Cmd + K - Открыть поиск
    this.register('ctrl+k', 'cmd+k', () => {
      document.querySelector('[data-action="focus-search"]')?.focus();
    });

    // Escape - Закрыть модальные окна
    this.register('escape', () => {
      this.uiManager.closeAllModals();
    });

    // Ctrl/Cmd + / - Открыть справку
    this.register('ctrl+/', 'cmd+/', () => {
      console.log('Справка');
    });

    // Ctrl/Cmd + T - Переключить тему
    this.register('ctrl+shift+l', 'cmd+shift+l', () => {
      document.querySelector('[data-action="toggle-theme"]')?.click();
    });
  }

  register(...keys) {
    const handler = keys[keys.length - 1];
    keys.slice(0, -1).forEach(key => {
      this.shortcuts.set(key.toLowerCase(), handler);
    });
  }

  init() {
    document.addEventListener('keydown', (e) => {
      const ctrl = e.ctrlKey || e.metaKey;
      const shift = e.shiftKey;
      const alt = e.altKey;

      let shortcut = '';
      if (ctrl) shortcut += 'ctrl+';
      if (shift) shortcut += 'shift+';
      if (alt) shortcut += 'alt+';
      shortcut += e.key.toLowerCase();

      const handler = this.shortcuts.get(shortcut);
      if (handler) {
        e.preventDefault();
        handler();
      }
    });
  }
}

/* ═════════════════════════════════════════════════════════════════
   ИНИЦИАЛИЗАЦИЯ
   ═════════════════════════════════════════════════════════════════ */

document.addEventListener('DOMContentLoaded', () => {
  // Инициализируем менеджеры
  const themeManager = new ThemeManager();
  const uiManager = new UIManager();
  const keyboardShortcuts = new KeyboardShortcuts(uiManager);

  // Инициализируем новые модули (Phase 3)
  let editor = null;
  let tagManager = null;

  // Инициализация Enhanced Editor (если есть контейнер)
  const editorContainer = document.getElementById('editor-container');
  if (editorContainer && typeof PromptEditor !== 'undefined') {
    editor = new PromptEditor({
      containerId: 'editor-container',
      api: {
        baseUrl: '/api',
        endpoints: {
          savePrompt: '/prompts',
          updatePrompt: '/prompts/{id}',
          getTags: '/tags'
        }
      },
      onSave: (promptData) => {
        console.log('📝 Промпт сохранён:', promptData);
      }
    });
    console.log('✓ Enhanced Editor инициализирован');
  }

  // Инициализация Tag Manager (если есть контейнер)
  const tagsManagerContainer = document.getElementById('tags-manager');
  if (tagsManagerContainer && typeof TagManager !== 'undefined') {
    tagManager = new TagManager({
      containerId: 'tags-manager',
      api: {
        baseUrl: '/api',
        endpoints: {
          getTags: '/tags',
          createTag: '/tags',
          updateTag: '/tags/{id}',
          deleteTag: '/tags/{id}'
        }
      },
      onTagsChange: (tags) => {
        console.log('🏷️ Теги обновлены:', tags);
      }
    });
    console.log('✓ Tag Manager инициализирован');
  }

  // Инициализация Analytics (если есть контейнер и модуль)
  const analyticsContainer = document.getElementById('analytics-dashboard');
  if (analyticsContainer && typeof AnalyticsDashboard !== 'undefined') {
    const analytics = new AnalyticsDashboard({
      containerId: 'analytics-dashboard',
      api: {
        baseUrl: '/api',
        endpoints: {
          getStats: '/analytics/stats',
          getTrends: '/analytics/trends'
        }
      }
    });
    console.log('✓ Analytics Dashboard инициализирован');
  }

  // Делаем доступными в глобальном окне
  window.App = {
    theme: themeManager,
    ui: uiManager,
    utils: Utilities,
    shortcuts: keyboardShortcuts,
    editor: editor,
    tagManager: tagManager
  };

  console.log('PANDORA v2.0 инициализирована ✨');
  console.log('Используйте window.App для доступа к менеджерам');
});

/* ═════════════════════════════════════════════════════════════════
   ПОДДЕРЖКА СТАРЫХ БРАУЗЕРОВ
   ═════════════════════════════════════════════════════════════════ */

if (!String.prototype.replaceAll) {
  String.prototype.replaceAll = function(str, newStr) {
    return this.split(str).join(newStr);
  };
}

// Полифилл для matchMedia
if (!window.matchMedia) {
  window.matchMedia = function() {
    return {
      matches: false,
      addListener: function() {},
      removeListener: function() {}
    };
  };
}

// Полифилл для IntersectionObserver
if (!window.IntersectionObserver) {
  window.IntersectionObserver = function() {
    return { observe: () => {}, unobserve: () => {} };
  };
}

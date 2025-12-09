/* ═══════════════════════════════════════════════════════════════════
   PANDORA v2.0 - Application Core
   Theme & UI Manager + Event System + HTTP Client
   ═════════════════════════════════════════════════════════════════ */

// Проверить что все необходимые модули загружены
const requiredModules = ['HTTPClient', 'EventManager', 'NavigationManager'];
const missingModules = requiredModules.filter(m => typeof window[m] === 'undefined');
if (missingModules.length > 0) {
  console.error('Отсутствуют модули:', missingModules);
  console.warn('Убедитесь что загружены: http-client.js, event-manager.js, navigation-manager.js');
}

/**
 * Инициализирует анимированный gradient background с плавающими orbs
 */
function initializeAnimatedBackground() {
  // Добавить класс для активирования gradient анимации
  document.body.classList.add('has-animated-gradient');

  // Создать floating orbs
  const orbsHTML = `
    <div class="gradient-orb gradient-orb-1"></div>
    <div class="gradient-orb gradient-orb-2"></div>
    <div class="gradient-orb gradient-orb-3"></div>
  `;
  
  document.body.insertAdjacentHTML('afterbegin', orbsHTML);
  
  console.log('[Background] Animated gradient background initialized');
}

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
    // Обработка кликов на backdrop для закрытия модали
    document.addEventListener('click', (e) => {
      const modal = e.target.closest('.modal');
      if (!modal) return;
      
      // Закрытие при клике на backdrop (вне modal-content)
      if (e.target === modal) {
        this.closeModal(modal.id);
        return;
      }

      // Закрытие при клике на close button
      if (e.target.closest('[data-action="close-modal"]')) {
        this.closeModal(modal.id);
      }
    });
  }

  openModal(modalId) {
    const modal = document.getElementById(modalId);
    if (!modal) {
      console.warn(`[UIManager] Modal not found: ${modalId}`);
      return;
    }

    modal.classList.add('active');
    modal.style.display = 'flex';
    document.body.style.overflow = 'hidden';
    this.modals.set(modalId, true);
  }

  closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (!modal) return;

    modal.classList.remove('active');
    modal.style.display = 'none';
    document.body.style.overflow = 'auto';
    this.modals.delete(modalId);
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
   ИНИЦИАЛИЗАЦИЯ - Phase 4: Modern Architecture
   ═════════════════════════════════════════════════════════════════ */

document.addEventListener('DOMContentLoaded', () => {
  try {
    // ========== 1. ИНИЦИАЛИЗАЦИЯ CORE СИСТЕМ ==========
    console.log('[INIT] Initializing PANDORA v2.0...');

    // Инициализировать animated gradient background
    initializeAnimatedBackground();

    const themeManager = new ThemeManager();
    const uiManager = new UIManager();
    const keyboardShortcuts = new KeyboardShortcuts(uiManager);

    // ========== 2. ИНИЦИАЛИЗАЦИЯ ADVANCED СИСТЕМЫ ==========
    // HTTP Client - централизованный API клиент
    const http = new HTTPClient({
      baseUrl: '/api',
      timeout: 30000,
      retryAttempts: 3,
      retryDelay: 1000,
      cacheTTL: 60000,
      debug: false // Включить для отладки
    });

    // Event Manager - управление событиями + error boundary
    const eventManager = new EventManager();
    eventManager.setupErrorBoundary({
      onError: (error, errorInfo) => {
        console.error('[Error Boundary]', errorInfo);
        uiManager.showToast(
          `Ошибка: ${error.message.slice(0, 50)}...`,
          'error',
          5000
        );
      },
      shouldLog: true,
      logToServer: true,
      logEndpoint: '/api/logs'
    });

    // Navigation Manager - управление страницами
    const navigationManager = new NavigationManager({
      defaultPage: 'dashboard',
      onNavigate: (pageName) => {
        console.log('[Nav] Navigated to:', pageName);
      }
    });

    // ========== 3. EVENT DELEGATION SETUP ==========
    setupEventDelegation(eventManager, http, uiManager, navigationManager);

    // ========== 4. ИНИЦИАЛИЗАЦИЯ МОДУЛЕЙ ==========
    let editor = null;
    let tagManager = null;
    let analytics = null;

    // Enhanced Editor
    const editorContainer = document.getElementById('editor-container');
    if (editorContainer && typeof PromptEditor !== 'undefined') {
      editor = new PromptEditor({
        containerId: 'editor-container',
        http: http,
        onSave: (promptData) => {
          eventManager.emit('app:prompt-saved', promptData);
          uiManager.showToast('Промпт сохранён', 'success');
        }
      });
      console.log('[INIT] Enhanced Editor initialized');
    }

    // Tag Manager
    const tagsManagerContainer = document.getElementById('tags-manager');
    if (tagsManagerContainer && typeof TagManager !== 'undefined') {
      tagManager = new TagManager({
        containerId: 'tags-manager',
        http: http,
        onTagsChange: (tags) => {
          eventManager.emit('app:tags-changed', tags);
        }
      });
      console.log('[INIT] Tag Manager initialized');
    }

    // Analytics Dashboard
    const analyticsContainer = document.getElementById('analytics-dashboard');
    if (analyticsContainer && typeof AnalyticsDashboard !== 'undefined') {
      analytics = new AnalyticsDashboard({
        containerId: 'analytics-dashboard',
        http: http
      });
      console.log('[INIT] Analytics Dashboard initialized');
    }

    // ========== 5. SETUP GLOBAL APP STATE ==========
    window.App = {
      // Core managers
      theme: themeManager,
      ui: uiManager,
      utils: Utilities,
      shortcuts: keyboardShortcuts,
      
      // Advanced systems
      http: http,
      eventManager: eventManager,
      navigation: navigationManager,
      
      // Feature modules
      editor: editor,
      tagManager: tagManager,
      analytics: analytics,
      
      // Utility methods
      showNotification: (msg, type = 'info') => uiManager.showToast(msg, type),
      navigate: (page) => navigationManager.navigateTo(page),
      closeAllModals: () => uiManager.closeAllModals()
    };

    // ========== 6. KEYBOARD SHORTCUTS FOR NAVIGATION ==========
    eventManager.on('document', 'keydown', (e) => {
      // Alt+1-5 для быстрого перехода между страницами
      const pages = ['dashboard', 'prompts', 'editor', 'tags-page', 'analytics'];
      if (e.altKey && e.key >= '1' && e.key <= '5') {
        const pageIndex = parseInt(e.key) - 1;
        if (pages[pageIndex]) {
          e.preventDefault();
          navigationManager.navigateTo(pages[pageIndex]);
        }
      }
    });

    // ========== 7. STARTUP CHECKS ==========
    performStartupChecks(http, uiManager);

    // ========== 8. PAGE DISPLAY CALLBACKS ==========
    // Reload analytics when dashboard is shown
    const dashboardPage = document.getElementById('dashboard');
    if (dashboardPage) {
      const observer = new MutationObserver((mutations) => {
        mutations.forEach((mutation) => {
          if (mutation.attributeName === 'class') {
            if (dashboardPage.classList.contains('active') && analytics) {
              console.log('[Dashboard] Page shown, refreshing analytics');
              analytics.loadStats();
            }
          }
        });
      });
      observer.observe(dashboardPage, { attributes: true });
    }

    console.log('%cPANDORA v2.0 готова', 'color: #00ff00; font-size: 14px; font-weight: bold');
    console.log('%cАрхитектура:', 'color: #00ff00; font-weight: bold');
    console.log('  ✓ HTTPClient (centralized API)');
    console.log('  ✓ EventManager (event delegation + error boundary)');
    console.log('  ✓ NavigationManager (page routing)');
    console.log('  ✓ UIManager (modals, toasts, menus)');
    console.log('  ✓ ThemeManager (light/dark mode)');
    console.log('%cДоступно через window.App', 'color: #00ffff');

  } catch (error) {
    console.error('[INIT ERROR]', error);
    console.error('Stack:', error.stack);
    document.body.innerHTML = `<div style="padding: 20px; background: #ffebee; color: #c62828; font-family: monospace;">
      <h2>Ошибка инициализации</h2>
      <pre>${error.message}\n${error.stack}</pre>
    </div>`;
  }
});

/**
 * Настройка Event Delegation для всех интерактивных элементов
 */
function setupEventDelegation(eventManager, http, uiManager, navigationManager) {
  // ========== КАТЕГОРИЯ МЕНЮ DROPDOWN ==========
  document.addEventListener('click', (e) => {
    const toggle = e.target.closest('[data-toggle-submenu]');
    if (toggle) {
      e.preventDefault();
      const menuId = toggle.getAttribute('data-toggle-submenu');
      const menu = document.getElementById(menuId);
      if (menu) {
        const isOpen = menu.classList.toggle('open');
        toggle.setAttribute('data-open', isOpen);
      }
    }
  });

  // ========== НАВИГАЦИЯ ==========
  eventManager.on('.nav-link[data-page]', 'click', function(e) {
    e.preventDefault();
    const page = this.getAttribute('data-page');
    navigationManager.navigateTo(page);
    
    // Обновить активный класс на nav links
    document.querySelectorAll('.nav-link').forEach(link => {
      link.classList.remove('active');
    });
    this.classList.add('active');
  });

  // ========== ПОИСК ==========
  const searchInput = document.querySelector('[data-action="search"]');
  if (searchInput) {
    // Debounced поиск при вводе
    eventManager.on('[data-action="search"]', 'input', function(e) {
      const query = this.value.trim();
      if (query.length > 2) {
        performSearch(query, http, uiManager);
      } else if (query.length === 0) {
        clearSearchResults();
      }
    }, { debounce: 300 });

    // Поиск по Enter
    eventManager.on('[data-action="search"]', 'keydown', function(e) {
      if (e.key === 'Enter') {
        e.preventDefault();
        const query = this.value.trim();
        if (query) {
          performSearch(query, http, uiManager);
        }
      }
    });
  }

  // ========== БЫСТРЫЕ ДЕЙСТВИЯ ==========
  eventManager.on('[data-action]', 'click', function(e) {
    const action = this.getAttribute('data-action');
    handleQuickAction(action, e, uiManager, navigationManager);
  });

  // ========== ФОРМА СОЗДАНИЯ ПРОМПТА ==========
  // Старый селектор для совместимости
  let promptFormElement = document.querySelector('[data-form="new-prompt"]');
  // Новый селектор для modal
  if (!promptFormElement) {
    promptFormElement = document.getElementById('prompt-form');
  }
  
  if (promptFormElement) {
    eventManager.addEventListener(promptFormElement, 'submit', (e) => {
      e.preventDefault();
      handleCreatePrompt(new FormData(promptFormElement), http, uiManager);
    });
  }

  // ========== ФОРМА СОЗДАНИЯ ПРОЕКТА (MODAL) ==========
  const projectForm = document.getElementById('project-form');
  if (projectForm) {
    projectForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      try {
        const formData = new FormData(projectForm);
        const data = Object.fromEntries(formData);
        const result = await http.post('/api/projects', data);
        uiManager.showToast('Проект создан успешно', 'success');
        projectForm.reset();
        uiManager.closeModal('project-modal');
        window.App.eventManager.emit('app:project-created', result);
      } catch (error) {
        console.error('[Project Form Error]', error);
        uiManager.showToast('Ошибка при создании проекта', 'error');
      }
    });
  }

  // ========== УДАЛЕНИЕ ЭЛЕМЕНТОВ ==========
  eventManager.on('[data-action="delete"]', 'click', async function(e) {
    e.preventDefault();
    const itemId = this.getAttribute('data-item-id');
    const itemType = this.getAttribute('data-item-type');
    
    if (confirm(`Вы уверены? Это действие нельзя отменить.`)) {
      await handleDeleteItem(itemId, itemType, http, uiManager);
    }
  });

  // ========== EDIT ДЕЙСТВИЯ ==========
  eventManager.on('[data-action="edit"]', 'click', function(e) {
    e.preventDefault();
    const itemId = this.getAttribute('data-item-id');
    const itemType = this.getAttribute('data-item-type');
    handleEditItem(itemId, itemType, uiManager, navigationManager);
  });

  // ========== COPY TO CLIPBOARD ==========
  eventManager.on('[data-action="copy"]', 'click', function(e) {
    e.preventDefault();
    const text = this.getAttribute('data-copy-text') || this.textContent;
    navigator.clipboard.writeText(text).then(() => {
      uiManager.showToast('Скопировано в буфер обмена', 'success');
    });
  });

  // ========== IMPORT FILE ==========
  const importBtn = document.querySelector('[data-action="import"]');
  if (importBtn) {
    eventManager.addEventListener(importBtn, 'click', (e) => {
      e.preventDefault();
      const fileInput = document.createElement('input');
      fileInput.type = 'file';
      fileInput.accept = '.json,.csv';
      fileInput.addEventListener('change', (event) => {
        handleImportFile(event.target.files[0], http, uiManager);
      });
      fileInput.click();
    });
  }

  // ========== EXPORT DATA ==========
  const exportBtn = document.querySelector('[data-action="export"]');
  if (exportBtn) {
    eventManager.addEventListener(exportBtn, 'click', (e) => {
      e.preventDefault();
      handleExportData(http, uiManager);
    });
  }

  console.log('[Setup] Event delegation configured');
}

/**
 * Обработчик поиска
 */
async function performSearch(query, http, uiManager) {
  try {
    if (!query || query.trim().length === 0) {
      clearSearchResults();
      return;
    }

    const resultsContainer = document.getElementById('search-results');
    if (!resultsContainer) {
      console.warn('[Search] Results container not found');
      return;
    }

    // Показать loading
    resultsContainer.style.display = 'block';
    resultsContainer.innerHTML = '<div class="loading">Поиск...</div>';

    // Пытаемся получить результаты с сервера
    let results = [];
    try {
      const response = await http.get('/api/search', { query });
      results = Array.isArray(response) ? response : (response.results || []);
    } catch (apiError) {
      console.warn('[Search] API search failed, using client-side fallback', apiError);
      
      // Client-side fallback: ищем в локальном хранилище/кэше
      results = performClientSideSearch(query);
    }

    if (results.length === 0) {
      resultsContainer.innerHTML = '<div class="no-results">Ничего не найдено</div>';
      return;
    }

    // Рендерим результаты
    resultsContainer.innerHTML = results.slice(0, 10).map(result => `
      <div class="search-result" data-item-id="${result.id}" data-item-type="${result.type || 'prompt'}">
        <div class="search-result-title">${escapeHtml(result.title || result.name || 'Без названия')}</div>
        <div class="search-result-desc">${escapeHtml((result.description || '').slice(0, 80))}</div>
        <div class="search-result-meta">${result.type || 'prompt'}</div>
      </div>
    `).join('');

    // Добавляем обработчик клика по результатам
    resultsContainer.addEventListener('click', (e) => {
      const result = e.target.closest('.search-result');
      if (result) {
        const itemId = result.getAttribute('data-item-id');
        const itemType = result.getAttribute('data-item-type');
        
        if (itemType === 'prompt') {
          window.App.navigationManager.navigateTo('editor');
          window.App.eventManager.emit('app:edit-item', { itemId, itemType });
        }
        
        clearSearchResults();
      }
    }, { once: true });

  } catch (error) {
    console.error('[Search Error]', error);
    const resultsContainer = document.getElementById('search-results');
    if (resultsContainer) {
      resultsContainer.innerHTML = '<div class="no-results">Ошибка при поиске</div>';
    }
  }
}

/**
 * Client-side search fallback для когда API недоступно
 */
function performClientSideSearch(query) {
  const normalizedQuery = query.toLowerCase();
  const results = [];

  // Ищем в промптах из localStorage если есть
  const prompts = [];
  for (let i = 0; i < localStorage.length; i++) {
    const key = localStorage.key(i);
    if (key?.startsWith('prompt_')) {
      try {
        const prompt = JSON.parse(localStorage.getItem(key));
        if (prompt && (
          prompt.title?.toLowerCase().includes(normalizedQuery) ||
          prompt.content?.toLowerCase().includes(normalizedQuery) ||
          prompt.description?.toLowerCase().includes(normalizedQuery)
        )) {
          results.push({
            id: prompt.id,
            title: prompt.title,
            description: prompt.description,
            type: 'prompt'
          });
        }
      } catch (e) {
        // Skip invalid items
      }
    }
  }

  return results.slice(0, 10);
}

function clearSearchResults() {
  const resultsContainer = document.getElementById('search-results');
  if (resultsContainer) {
    resultsContainer.style.display = 'none';
    resultsContainer.innerHTML = '';
  }
}

/**
 * Обработчик быстрых действий
 */
function handleQuickAction(action, e, uiManager, navigationManager) {
  const actions = {
    // Editor
    'new-prompt': () => navigationManager.navigateTo('editor'),
    'open-prompt-modal': () => uiManager.openModal('prompt-modal'),
    
    // Projects
    'new-project': () => uiManager.openModal('project-modal'),
    'open-project-modal': () => uiManager.openModal('project-modal'),
    
    // Tags
    'new-tag': () => window.App.tagManager.openCreateModal(),
    
    // Theme & Search
    'toggle-theme': () => window.App.theme.toggleTheme(),
    'focus-search': () => document.querySelector('[data-action="search"]')?.focus(),
    
    // Modal controls
    'close-modal': () => {
      const modal = e?.target?.closest('.modal');
      if (modal) {
        uiManager.closeModal(modal.id);
      }
    }
  };

  const handler = actions[action];
  if (handler) {
    handler();
  }
}

/**
 * Обработчик создания промпта
 */
async function handleCreatePrompt(formData, http, uiManager) {
  try {
    const data = Object.fromEntries(formData);
    const result = await http.post('/prompts', data);
    
    uiManager.showToast('Промпт создан', 'success');
    window.App.eventManager.emit('app:prompt-created', result);
    
  } catch (error) {
    console.error('[Create Prompt Error]', error);
    uiManager.showToast('Ошибка при создании промпта', 'error');
  }
}

/**
 * Обработчик удаления элемента
 */
async function handleDeleteItem(itemId, itemType, http, uiManager) {
  try {
    const endpoint = `//${itemType}/${itemId}`;
    await http.delete(endpoint);
    
    uiManager.showToast('Элемент удалён', 'success');
    window.App.eventManager.emit('app:item-deleted', { itemId, itemType });
    
  } catch (error) {
    console.error('[Delete Error]', error);
    uiManager.showToast('Ошибка при удалении', 'error');
  }
}

/**
 * Обработчик редактирования элемента
 */
function handleEditItem(itemId, itemType, uiManager, navigationManager) {
  if (itemType === 'prompt') {
    navigationManager.navigateTo('editor');
    window.App.eventManager.emit('app:edit-item', { itemId, itemType });
  } else {
    uiManager.showToast('Редактирование для этого типа не поддерживается', 'info');
  }
}

/**
 * Обработчик импорта файла
 */
async function handleImportFile(file, http, uiManager) {
  if (!file) return;

  try {
    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch('/api/import', {
      method: 'POST',
      body: formData
    });

    if (!response.ok) throw new Error(`HTTP ${response.status}`);

    const result = await response.json();
    uiManager.showToast(`Импортировано ${result.count} элементов`, 'success');
    window.App.eventManager.emit('app:data-imported', result);

  } catch (error) {
    console.error('[Import Error]', error);
    uiManager.showToast('Ошибка при импорте файла', 'error');
  }
}

/**
 * Обработчик экспорта данных
 */
async function handleExportData(http, uiManager) {
  try {
    const data = await http.get('/export');
    
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `pandora-export-${Date.now()}.json`;
    a.click();
    URL.revokeObjectURL(url);

    uiManager.showToast('Данные экспортированы', 'success');

  } catch (error) {
    console.error('[Export Error]', error);
    uiManager.showToast('Ошибка при экспорте', 'error');
  }
}

/**
 * Проверки при запуске
 */
async function performStartupChecks(http, uiManager) {
  try {
    // Проверить API
    const health = await http.get('/health', { timeout: 5000 });
    console.log('[Health Check] API status:', health);

    // Загрузить начальные данные если нужно
    if (document.querySelector('[data-load-on-start]')) {
      console.log('[Startup] Loading initial data...');
    }

  } catch (error) {
    console.warn('[Startup Check] API не доступна:', error.message);
  }
}

/**
 * Утилита для экранирования HTML
 */
function escapeHtml(text) {
  const map = {
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
    '"': '&quot;',
    "'": '&#039;'
  };
  return text.replace(/[&<>"']/g, m => map[m]);
}

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

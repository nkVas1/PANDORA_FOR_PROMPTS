/**
 * ═════════════════════════════════════════════════════════════════════
 * PANDORA v2.0 - Navigation Manager
 * Система управления навигацией между страницами приложения
 * ═════════════════════════════════════════════════════════════════════
 */

class NavigationManager {
  /**
   * Инициализирует менеджер навигации
   * @param {Object} config - конфигурация
   * @param {string} config.defaultPage - страница по умолчанию
   * @param {Function} config.onNavigate - callback при навигации
   */
  constructor(config = {}) {
    this.defaultPage = config.defaultPage || 'dashboard';
    this.onNavigate = config.onNavigate || (() => {});
    this.currentPage = this.defaultPage;
    this.pageHistory = [this.defaultPage];
    this.maxHistory = 20;
    this.transitionSpeed = 300; // ms
    
    this.init();
  }

  /**
   * Инициализирует менеджер
   */
  init() {
    this.setupNavigation();
    this.setupBrowserHistory();
    this.setupKeyboardShortcuts();
    console.log('[Navigation] Manager initialized');
  }

  /**
   * Настраивает обработчики навигационных кнопок
   */
  setupNavigation() {
    // Event delegation для всех nav-link кнопок
    document.addEventListener('click', (e) => {
      const navLink = e.target.closest('.nav-link[data-page]');
      if (!navLink) return;

      e.preventDefault();
      e.stopPropagation();

      const targetPage = navLink.getAttribute('data-page');
      if (targetPage) {
        this.navigateTo(targetPage);
      }
    });
  }

  /**
   * Настраивает browser history API
   */
  setupBrowserHistory() {
    window.addEventListener('popstate', (e) => {
      if (e.state && e.state.page) {
        this.showPage(e.state.page, false); // false = не добавляем в history
      }
    });
  }

  /**
   * Настраивает клавишные комбинации для навигации
   */
  setupKeyboardShortcuts() {
    const pageShortcuts = {
      'Digit1': 'dashboard',
      'Digit2': 'prompts',
      'Digit3': 'editor',
      'Digit4': 'tags-page',
      'Digit5': 'analytics',
    };

    document.addEventListener('keydown', (e) => {
      // Alt+Number для навигации
      if (e.altKey && pageShortcuts[e.code]) {
        e.preventDefault();
        this.navigateTo(pageShortcuts[e.code]);
      }

      // Alt+Left/Right для истории
      if (e.altKey && e.key === 'ArrowLeft') {
        e.preventDefault();
        this.goBack();
      }
      if (e.altKey && e.key === 'ArrowRight') {
        e.preventDefault();
        this.goForward();
      }
    });
  }

  /**
   * Переходит на указанную страницу
   * @param {string} pageName - название страницы
   */
  navigateTo(pageName) {
    // Проверка валидности страницы
    const pageElement = document.getElementById(pageName);
    if (!pageElement) {
      console.warn(`[Navigation] Page not found: ${pageName}`);
      return;
    }

    // Не переходим если уже на этой странице
    if (this.currentPage === pageName) {
      return;
    }

    this.showPage(pageName, true); // true = добавляем в history
  }

  /**
   * Показывает страницу с анимацией
   * @param {string} pageName - название страницы
   * @param {boolean} addHistory - добавить в browser history
   */
  showPage(pageName, addHistory = true) {
    const pageElement = document.getElementById(pageName);
    if (!pageElement) {
      console.error(`[Navigation] Page element not found: ${pageName}`);
      return;
    }

    // Найти активную страницу и скрыть её
    const activePages = document.querySelectorAll('.page.active');
    activePages.forEach(page => {
      page.classList.remove('active');
      // Trigger fade-out animation
      page.style.opacity = '0';
      page.style.pointerEvents = 'none';
    });

    // Обновить активный nav-link
    const navLinks = document.querySelectorAll('.nav-link[data-page]');
    navLinks.forEach(link => {
      const linkPage = link.getAttribute('data-page');
      link.classList.toggle('active', linkPage === pageName);
    });

    // Показать новую страницу с fade-in анимацией
    setTimeout(() => {
      pageElement.classList.add('active');
      pageElement.style.opacity = '0';
      pageElement.style.pointerEvents = 'auto';
      
      // Trigger reflow to apply opacity transition
      pageElement.offsetHeight;
      
      pageElement.style.opacity = '1';
    }, 50);

    // Обновить текущую страницу
    this.currentPage = pageName;

    // Обновить историю
    if (addHistory) {
      this.addToHistory(pageName);
      window.history.pushState({ page: pageName }, '', `#${pageName}`);
    }

    // Вызвать callback
    this.onNavigate({ page: pageName, timestamp: Date.now() });

    // Scroll to top
    window.scrollTo({ top: 0, behavior: 'smooth' });

    // Dispatch custom event для других компонентов
    window.dispatchEvent(new CustomEvent('page-changed', {
      detail: { page: pageName }
    }));

    console.log(`[Navigation] Navigated to: ${pageName}`);
  }

  /**
   * Добавляет страницу в историю
   */
  addToHistory(pageName) {
    // Удалить текущую страницу если она в конце истории
    if (this.pageHistory[this.pageHistory.length - 1] === pageName) {
      return;
    }

    this.pageHistory.push(pageName);

    // Ограничить размер истории
    if (this.pageHistory.length > this.maxHistory) {
      this.pageHistory.shift();
    }
  }

  /**
   * Переходит на предыдущую страницу
   */
  goBack() {
    if (this.pageHistory.length > 1) {
      this.pageHistory.pop(); // Удалить текущую
      const previousPage = this.pageHistory[this.pageHistory.length - 1];
      this.showPage(previousPage, false);
    }
  }

  /**
   * Переходит на следующую страницу (если есть история)
   */
  goForward() {
    // Простая реализация - в полной версии нужна отдельная forward история
    console.log('[Navigation] Forward not implemented in this version');
  }

  /**
   * Получить текущую страницу
   */
  getCurrentPage() {
    return this.currentPage;
  }

  /**
   * Получить историю навигации
   */
  getHistory() {
    return [...this.pageHistory];
  }

  /**
   * Очистить историю
   */
  clearHistory() {
    this.pageHistory = [this.currentPage];
  }
}

// Экспорт для использования
if (typeof module !== 'undefined' && module.exports) {
  module.exports = NavigationManager;
}

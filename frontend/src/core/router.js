/**
 * Router - Modern Hash-Based Routing System
 * 
 * Система навигации с поддержкой:
 * - Hash-based маршрутизации
 * - Динамической загрузки views
 * - Переходов между страницами
 * - Query параметров
 * - Истории навигации
 * - Защиты маршрутов
 * 
 * @class Router
 * @example
 * const router = new Router({
 *   container: '#app',
 *   defaultRoute: '/dashboard'
 * });
 * 
 * router.addRoute('/dashboard', DashboardView);
 * router.addRoute('/prompts', PromptsView);
 * router.navigate('/dashboard');
 */
class Router {
  constructor(options = {}) {
    this.container = typeof options.container === 'string' 
      ? document.querySelector(options.container) 
      : options.container;
    
    this.defaultRoute = options.defaultRoute || '/dashboard';
    this.routes = new Map();
    this.currentRoute = null;
    this.currentView = null;
    this.guards = [];
    this.beforeHooks = [];
    this.afterHooks = [];
    this.history = [];
    
    this.init();
  }

  /**
   * Инициализировать маршрутизатор
   * @private
   */
  init() {
    // Слушать изменения hash
    window.addEventListener('hashchange', () => {
      this.resolveRoute();
    });
    
    // Начальная навигация
    this.resolveRoute();
  }

  /**
   * Добавить маршрут
   * @param {string} path - Путь (e.g. "/dashboard", "/prompts/:id")
   * @param {Class|Object} view - Класс view или объект с методом render()
   * @param {Object} options - Опции маршрута
   */
  addRoute(path, view, options = {}) {
    this.routes.set(path, {
      view,
      options: {
        title: options.title || 'PANDORA',
        requiresAuth: options.requiresAuth || false,
        meta: options.meta || {},
        ...options
      }
    });
  }

  /**
   * Добавить guard (защиту маршрута)
   * @param {Function} guardFn - (to, from) => boolean | Promise<boolean>
   */
  addGuard(guardFn) {
    this.guards.push(guardFn);
  }

  /**
   * Hook до перехода на маршрут
   * @param {Function} hookFn - (to, from) => void
   */
  beforeEach(hookFn) {
    this.beforeHooks.push(hookFn);
  }

  /**
   * Hook после перехода на маршрут
   * @param {Function} hookFn - (to, from) => void
   */
  afterEach(hookFn) {
    this.afterHooks.push(hookFn);
  }

  /**
   * Получить текущий маршрут из hash
   * @private
   * @returns {string} Маршрут
   */
  getCurrentRoute() {
    let hash = window.location.hash.slice(1) || this.defaultRoute;
    if (!hash.startsWith('/')) hash = '/' + hash;
    return hash;
  }

  /**
   * Разрешить (найти) маршрут по пути
   * @private
   * @param {string} path - Путь
   * @returns {Object|null} Маршрут или null
   */
  resolveRouteByPath(path) {
    // Точное совпадение
    if (this.routes.has(path)) {
      return this.routes.get(path);
    }
    
    // Параметризованные маршруты
    for (const [routePath, route] of this.routes) {
      const pattern = routePath.replace(/:[^\s/]+/g, '[^/]+');
      const regex = new RegExp(`^${pattern}$`);
      
      if (regex.test(path)) {
        return route;
      }
    }
    
    return null;
  }

  /**
   * Разрешить текущий маршрут
   * @private
   */
  async resolveRoute() {
    const path = this.getCurrentRoute();
    const from = this.currentRoute;
    
    // Проверить guards
    for (const guardFn of this.guards) {
      const allowed = await guardFn({ path, from });
      if (!allowed) {
        this.navigate(from || this.defaultRoute);
        return;
      }
    }
    
    // Выполнить beforeEach hooks
    for (const hookFn of this.beforeHooks) {
      await hookFn({ path, from });
    }
    
    // Найти маршрут
    const route = this.resolveRouteByPath(path);
    
    if (!route) {
      console.warn(`Route not found: ${path}`);
      this.navigate(this.defaultRoute);
      return;
    }
    
    // Обновить текущий маршрут
    this.currentRoute = path;
    this.history.push(path);
    
    // Загрузить и отобразить view
    await this.loadView(route, path);
    
    // Обновить заголовок
    document.title = route.options.title;
    
    // Выполнить afterEach hooks
    for (const hookFn of this.afterHooks) {
      await hookFn({ path, from });
    }
    
    // Emit события
    window.dispatchEvent(new CustomEvent('route:changed', {
      detail: { path, from, route }
    }));
  }

  /**
   * Загрузить и отобразить view
   * @private
   */
  async loadView(route, path) {
    try {
      console.log(`[Router] Loading view for path: ${path}`);
      
      // Очистить старый view
      if (this.currentView && typeof this.currentView.destroy === 'function') {
        this.currentView.destroy();
      }
      
      // Получить view обработчик
      let viewHandler = route.view;
      
      // Если это Promise - подождать
      if (viewHandler instanceof Promise) {
        viewHandler = await viewHandler;
      }
      
      // viewHandler это async функция которая возвращает DOM элемент
      // Вызываем её и ждем результат
      if (typeof viewHandler === 'function') {
        console.log(`[Router] Calling view handler for ${path}`);
        this.currentView = await viewHandler({
          router: this,
          route: route.options,
          path: path
        });
      } else {
        this.currentView = viewHandler;
      }
      
      // Проверяем результат
      if (!this.currentView) {
        throw new Error(`View handler returned null/undefined for ${path}`);
      }
      
      console.log(`[Router] View loaded:`, this.currentView);
      
      // Очищаем контейнер
      this.container.innerHTML = '';
      
      // Отображаем view в зависимости от типа
      if (this.currentView instanceof HTMLElement) {
        // Это готовый DOM элемент
        console.log(`[Router] ✓ View is HTMLElement, appending to container`);
        this.container.appendChild(this.currentView);
      } else if (typeof this.currentView === 'object' && this.currentView.render && typeof this.currentView.render === 'function') {
        // Если это объект с методом render()
        console.log(`[Router] View has render() method, calling it`);
        const element = this.currentView.render();
        if (element instanceof HTMLElement) {
          this.container.appendChild(element);
        }
      } else if (typeof this.currentView === 'string') {
        // HTML строка
        console.log(`[Router] View is HTML string`);
        this.container.innerHTML = this.currentView;
      } else {
        throw new Error(`View is not a valid type: ${typeof this.currentView}`);
      }
      
      // Trigger animation
      requestAnimationFrame(() => {
        this.container.classList.add('view-enter');
      });
      
      console.log(`[Router] ✓ View loaded successfully for ${path}`);
      
    } catch (error) {
      console.error(`[Router] ✗ Error loading view for ${path}:`, error);
      console.error('[Router] Stack:', error.stack);
      
      this.container.innerHTML = `
        <div class="error-view" style="padding: 40px; text-align: center; color: #ef4444;">
          <h2>⚠️ Error loading page</h2>
          <p style="color: #94a3b8; margin: 10px 0;">${error.message}</p>
          <p style="color: #64748b; font-size: 0.9rem; font-family: monospace; text-align: left; background: #0f0f0f; padding: 10px; border-radius: 4px; overflow-x: auto;">
            ${error.stack}
          </p>
          <button onclick="window.router.navigate('${this.defaultRoute}')" style="padding: 10px 20px; margin-top: 20px; cursor: pointer; background: #3b82f6; color: white; border: none; border-radius: 4px;">
            Go Home
          </button>
        </div>
      `;
    }
  }

  /**
   * Навигировать на маршрут
   * @param {string} path - Путь
   * @param {Object} state - Состояние для передачи
   */
  navigate(path, state = {}) {
    if (!path.startsWith('/')) path = '/' + path;
    
    // Сохранить состояние (если нужно)
    if (Object.keys(state).length > 0) {
      sessionStorage.setItem('router-state', JSON.stringify(state));
    }
    
    // Изменить hash (это триггерит hashchange)
    window.location.hash = path;
  }

  /**
   * Навигация назад
   */
  back() {
    if (this.history.length > 1) {
      this.history.pop();
      const previousRoute = this.history[this.history.length - 1];
      this.navigate(previousRoute);
    }
  }

  /**
   * Получить параметры из пути
   * @param {string} path - Путь с параметрами
   * @param {string} routePath - Определение маршрута
   * @returns {Object} Параметры
   */
  getParams(path, routePath) {
    const routeParts = routePath.split('/');
    const pathParts = path.split('/');
    const params = {};
    
    for (let i = 0; i < routeParts.length; i++) {
      if (routeParts[i].startsWith(':')) {
        const paramName = routeParts[i].slice(1);
        params[paramName] = pathParts[i];
      }
    }
    
    return params;
  }

  /**
   * Получить query параметры
   * @returns {Object} Query параметры
   */
  getQuery() {
    const hash = window.location.hash;
    const [, query] = hash.split('?');
    
    if (!query) return {};
    
    const params = {};
    query.split('&').forEach(param => {
      const [key, value] = param.split('=');
      params[decodeURIComponent(key)] = decodeURIComponent(value);
    });
    
    return params;
  }

  /**
   * Получить состояние (если было передано)
   * @returns {Object} Состояние
   */
  getState() {
    try {
      const state = sessionStorage.getItem('router-state');
      if (state) {
        sessionStorage.removeItem('router-state');
        return JSON.parse(state);
      }
    } catch (error) {
      console.error('Error getting router state:', error);
    }
    return {};
  }

  /**
   * Получить все маршруты
   * @returns {Array} Массив маршрутов
   */
  getRoutes() {
    return Array.from(this.routes.entries()).map(([path, route]) => ({
      path,
      title: route.options.title,
      requiresAuth: route.options.requiresAuth,
      meta: route.options.meta
    }));
  }

  /**
   * Проверить активность маршрута
   * @param {string} path - Путь
   * @returns {boolean} Активен ли маршрут
   */
  isActive(path) {
    if (!path.startsWith('/')) path = '/' + path;
    const current = this.getCurrentRoute();
    
    // Точное совпадение
    if (current === path) return true;
    
    // Начинается с пути (для подмаршрутов)
    return current.startsWith(path + '/');
  }
}

// Экспорт
export default Router;

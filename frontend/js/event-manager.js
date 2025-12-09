/**
 * ═════════════════════════════════════════════════════════════════════
 * PANDORA v2.0 - Event Manager & Error Boundary
 * Centralized event handling with delegation + error boundary
 * ═════════════════════════════════════════════════════════════════════
 */

class EventManager {
  constructor() {
    this.handlers = new Map();
    this.boundHandlers = new WeakMap();
    this.delegatedHandlers = new Map();
    this.globalErrorBoundary = null;
  }

  /**
   * Регистрирует обработчик события с event delegation
   * @param {string} selector - CSS селектор (использует 'closest' для delegation)
   * @param {string} event - тип события (e.g., 'click', 'change')
   * @param {Function} handler - функция-обработчик
   * @param {Object} options - опции (capture, once, debounce, throttle)
   */
  on(selector, event, handler, options = {}) {
    const key = `${selector}:${event}`;
    
    if (!this.delegatedHandlers.has(key)) {
      this.setupDelegation(selector, event, options);
      this.delegatedHandlers.set(key, []);
    }

    const wrappedHandler = this.wrapHandler(handler, options);
    this.delegatedHandlers.get(key).push(wrappedHandler);

    // Вернуть функцию для удаления обработчика
    return () => {
      const handlers = this.delegatedHandlers.get(key);
      const index = handlers.indexOf(wrappedHandler);
      if (index > -1) {
        handlers.splice(index, 1);
      }
    };
  }

  /**
   * Регистрирует обработчик на конкретный элемент
   */
  addEventListener(element, event, handler, options = {}) {
    if (!element) return;

    const wrappedHandler = this.wrapHandler(handler, options);
    const bound = wrappedHandler.bind(this);

    element.addEventListener(event, bound, {
      capture: options.capture || false,
      once: options.once || false,
      passive: options.passive !== false
    });

    // Сохранить для удаления
    if (!this.boundHandlers.has(element)) {
      this.boundHandlers.set(element, []);
    }
    this.boundHandlers.get(element).push({ event, bound });

    // Вернуть функцию для удаления
    return () => {
      element.removeEventListener(event, bound);
    };
  }

  /**
   * Setupдельгирование события
   */
  setupDelegation(selector, event, options = {}) {
    const delegationHandler = (e) => {
      const target = e.target.closest(selector);
      if (!target) return;

      const key = `${selector}:${event}`;
      const handlers = this.delegatedHandlers.get(key);

      if (handlers) {
        handlers.forEach(handler => {
          try {
            handler.call(target, e, target);
          } catch (error) {
            this.handleError(error, { selector, event, target });
          }
        });
      }
    };

    document.addEventListener(event, delegationHandler, {
      capture: options.capture || false,
      passive: options.passive !== false
    });
  }

  /**
   * Оборачивает обработчик с debounce/throttle/error handling
   */
  wrapHandler(handler, options = {}) {
    let wrappedFn = handler;

    // Debounce
    if (options.debounce) {
      let timeoutId;
      wrappedFn = function(...args) {
        clearTimeout(timeoutId);
        timeoutId = setTimeout(() => handler.apply(this, args), options.debounce);
      };
    }

    // Throttle
    if (options.throttle) {
      let lastCall = 0;
      wrappedFn = function(...args) {
        const now = Date.now();
        if (now - lastCall >= options.throttle) {
          lastCall = now;
          handler.apply(this, args);
        }
      };
    }

    // Error boundary
    const finalFn = function(...args) {
      try {
        return wrappedFn.apply(this, args);
      } catch (error) {
        this.handleError(error, { handler: handler.name, args });
        if (options.onError) {
          options.onError(error);
        }
      }
    };

    return finalFn;
  }

  /**
   * Удаляет все обработчики с элемента
   */
  removeAllListeners(element) {
    if (!this.boundHandlers.has(element)) return;

    const handlers = this.boundHandlers.get(element);
    handlers.forEach(({ event, bound }) => {
      element.removeEventListener(event, bound);
    });

    this.boundHandlers.delete(element);
  }

  /**
   * Эмитит custom event
   */
  emit(eventName, detail = {}) {
    const event = new CustomEvent(eventName, {
      detail,
      bubbles: true,
      cancelable: true
    });

    document.dispatchEvent(event);
  }

  /**
   * Слушает custom events
   */
  onCustom(eventName, handler, element = document) {
    const wrappedHandler = (e) => {
      try {
        handler(e.detail, e);
      } catch (error) {
        this.handleError(error, { event: eventName });
      }
    };

    element.addEventListener(eventName, wrappedHandler);

    // Вернуть функцию для удаления
    return () => {
      element.removeEventListener(eventName, wrappedHandler);
    };
  }

  /**
   * Setup global error boundary
   */
  setupErrorBoundary(config = {}) {
    this.globalErrorBoundary = {
      onError: config.onError || ((error) => {
        console.error('[Error Boundary]', error);
      }),
      onWarning: config.onWarning || ((message) => {
        console.warn('[Warning]', message);
      }),
      shouldLog: config.shouldLog !== false,
      logToServer: config.logToServer || false,
      logEndpoint: config.logEndpoint || '/api/logs'
    };

    // Handle uncaught errors
    window.addEventListener('error', (e) => {
      this.handleError(e.error || e.message, {
        type: 'uncaughtError',
        filename: e.filename,
        lineno: e.lineno,
        colno: e.colno
      });
    });

    // Handle unhandled promise rejections
    window.addEventListener('unhandledrejection', (e) => {
      this.handleError(e.reason, {
        type: 'unhandledRejection'
      });
    });
  }

  /**
   * Обработка ошибок с error boundary
   */
  handleError(error, context = {}) {
    const errorInfo = {
      message: error.message || String(error),
      stack: error.stack,
      context,
      timestamp: new Date().toISOString(),
      userAgent: navigator.userAgent,
      url: window.location.href
    };

    // Log in console
    if (this.globalErrorBoundary?.shouldLog) {
      console.error('[Error Handler]', errorInfo);
    }

    // Call error callback
    if (this.globalErrorBoundary?.onError) {
      try {
        this.globalErrorBoundary.onError(error, errorInfo);
      } catch (e) {
        console.error('Error in error handler:', e);
      }
    }

    // Log to server
    if (this.globalErrorBoundary?.logToServer && window.App?.http) {
      this.sendErrorLog(errorInfo).catch(e => {
        console.error('Failed to send error log:', e);
      });
    }

    // Emit error event for other components
    this.emit('app:error', errorInfo);

    return errorInfo;
  }

  /**
   * Отправить ошибку на сервер
   */
  async sendErrorLog(errorInfo) {
    try {
      const endpoint = this.globalErrorBoundary?.logEndpoint || '/api/logs';
      const http = window.App?.http;

      if (http && http.post) {
        await http.post(endpoint, {
          type: 'frontend_error',
          ...errorInfo
        });
      }
    } catch (error) {
      // Silent fail - не создавай infinite loop
      console.error('Error logging failed:', error);
    }
  }

  /**
   * Создать safe async wrapper
   */
  async safeAsync(asyncFn, context = {}) {
    try {
      return await asyncFn();
    } catch (error) {
      this.handleError(error, { ...context, type: 'asyncError' });
      throw error;
    }
  }

  /**
   * Создать safe function wrapper
   */
  safeSync(fn, context = {}) {
    return function(...args) {
      try {
        return fn.apply(this, args);
      } catch (error) {
        this.handleError(error, { ...context, type: 'syncError', args });
        throw error;
      }
    };
  }

  /**
   * Clear все обработчики
   */
  clearAll() {
    this.delegatedHandlers.clear();
    this.boundHandlers = new WeakMap();
    this.handlers.clear();
  }
}

// Export
if (typeof module !== 'undefined' && module.exports) {
  module.exports = EventManager;
}

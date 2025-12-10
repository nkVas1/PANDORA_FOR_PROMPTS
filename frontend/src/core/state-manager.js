/**
 * StateManager - Reactive State Management System
 * 
 * Система управления состоянием с реактивными обновлениями
 * 
 * Возможности:
 * - Реактивные прокси для отслеживания изменений
 * - Паттерн Observer для подписок на изменения
 * - Computed свойства (вычисляемые значения)
 * - История изменений (undo/redo)
 * - Middleware для логирования и валидации
 * - Персистентность (localStorage)
 * 
 * @class StateManager
 * @example
 * const appState = new StateManager({
 *   prompts: [],
 *   user: { name: 'John' }
 * });
 * 
 * // Наблюдать за изменениями
 * appState.observe('prompts', (newValue) => {
 *   console.log('Prompts updated:', newValue);
 * });
 * 
 * // Изменить состояние (автоматически уведомит наблюдателей)
 * appState.state.prompts = [...appState.state.prompts, newPrompt];
 */
class StateManager {
  constructor(initialState = {}) {
    this.state = this.createReactiveProxy(initialState);
    this.observers = new Map();
    this.computed = new Map();
    this.history = [];
    this.historyIndex = -1;
    this.middleware = [];
    this.maxHistory = 50;
  }

  /**
   * Создать реактивный прокси для отслеживания изменений
   * @private
   * @param {Object} target - Целевой объект
   * @param {string} path - Текущий путь в объекте
   * @returns {Proxy} Реактивный прокси
   */
  createReactiveProxy(target, path = '') {
    const self = this;
    
    return new Proxy(target, {
      get(obj, prop) {
        const value = obj[prop];
        const fullPath = path ? `${path}.${prop}` : prop;
        
        // Если есть computed значение, вернуть его
        if (self.computed.has(fullPath)) {
          return self.computed.get(fullPath)();
        }
        
        // Если объект - обернуть в реактивный прокси
        if (typeof value === 'object' && value !== null && !Array.isArray(value)) {
          return self.createReactiveProxy(value, fullPath);
        }
        
        return value;
      },
      
      set(obj, prop, value) {
        const fullPath = path ? `${path}.${prop}` : prop;
        const oldValue = obj[prop];
        
        // Не триггерить если значение не изменилось
        if (oldValue === value) return true;
        
        // Контекст для middleware
        const context = {
          path: fullPath,
          oldValue,
          newValue: value,
          state: self.state
        };
        
        // Применить middleware
        for (const middlewareFn of self.middleware) {
          const result = middlewareFn(context);
          if (result === false) return false; // Предотвратить обновление
          if (result !== undefined) value = result;
        }
        
        // Обновить значение
        obj[prop] = value;
        
        // Добавить в историю
        self.addToHistory({
          path: fullPath,
          oldValue,
          newValue: value,
          timestamp: Date.now()
        });
        
        // Уведомить наблюдателей
        self.notify(fullPath, value, oldValue);
        
        return true;
      }
    });
  }

  /**
   * Подписаться на изменения состояния
   * @param {string} path - Путь к свойству (поддерживает wildcards: "prompts.*")
   * @param {Function} callback - Функция обратного вызова (newValue, oldValue, path) => void
   * @returns {Function} Функция отписки
   */
  observe(path, callback) {
    if (!this.observers.has(path)) {
      this.observers.set(path, new Set());
    }
    
    this.observers.get(path).add(callback);
    
    // Вернуть функцию отписки
    return () => {
      const observers = this.observers.get(path);
      if (observers) {
        observers.delete(callback);
      }
    };
  }

  /**
   * Уведомить наблюдателей об изменении
   * @private
   */
  notify(path, newValue, oldValue) {
    // Уведомить точных наблюдателей
    const observers = this.observers.get(path);
    if (observers) {
      observers.forEach(callback => callback(newValue, oldValue, path));
    }
    
    // Уведомить wildcard наблюдателей
    this.observers.forEach((callbacks, observerPath) => {
      if (this.matchPath(path, observerPath)) {
        callbacks.forEach(callback => callback(newValue, oldValue, path));
      }
    });
  }

  /**
   * Проверить совпадение пути с паттерном
   * @private
   */
  matchPath(actualPath, pattern) {
    if (pattern.includes('*')) {
      const regex = new RegExp('^' + pattern.replace(/\*/g, '.*') + '$');
      return regex.test(actualPath);
    }
    return actualPath.startsWith(pattern);
  }

  /**
   * Создать вычисляемое свойство (computed)
   * @param {string} path - Путь к вычисляемому свойству
   * @param {Function} computeFn - Функция вычисления
   */
  createComputed(path, computeFn) {
    this.computed.set(path, computeFn);
  }

  /**
   * Добавить middleware для логирования/валидации
   * @param {Function} middlewareFn - (context) => result | false
   */
  use(middlewareFn) {
    this.middleware.push(middlewareFn);
  }

  /**
   * Добавить изменение в историю
   * @private
   */
  addToHistory(change) {
    // Удалить будущую историю если мы не в конце
    if (this.historyIndex < this.history.length - 1) {
      this.history = this.history.slice(0, this.historyIndex + 1);
    }
    
    this.history.push(change);
    
    // Ограничить размер истории
    if (this.history.length > this.maxHistory) {
      this.history.shift();
    } else {
      this.historyIndex++;
    }
  }

  /**
   * Отменить последнее изменение (Undo)
   * @returns {boolean} Успешность операции
   */
  undo() {
    if (this.historyIndex >= 0) {
      const change = this.history[this.historyIndex];
      this.setValueByPath(change.path, change.oldValue);
      this.historyIndex--;
      return true;
    }
    return false;
  }

  /**
   * Повторить отменённое изменение (Redo)
   * @returns {boolean} Успешность операции
   */
  redo() {
    if (this.historyIndex < this.history.length - 1) {
      this.historyIndex++;
      const change = this.history[this.historyIndex];
      this.setValueByPath(change.path, change.newValue);
      return true;
    }
    return false;
  }

  /**
   * Установить значение по пути
   * @private
   */
  setValueByPath(path, value) {
    const parts = path.split('.');
    let obj = this.state;
    
    for (let i = 0; i < parts.length - 1; i++) {
      obj = obj[parts[i]];
    }
    
    obj[parts[parts.length - 1]] = value;
  }

  /**
   * Получить значение по пути
   * @param {string} path - Путь к свойству (e.g. "user.name" или "prompts.0.title")
   * @returns {*} Значение свойства
   */
  getValueByPath(path) {
    const parts = path.split('.');
    let value = this.state;
    
    for (const part of parts) {
      value = value[part];
      if (value === undefined) break;
    }
    
    return value;
  }

  /**
   * Сохранить состояние в localStorage
   * @param {string} key - Ключ для хранения
   */
  persist(key = 'app-state') {
    try {
      // Сериализовать только нужные части состояния
      const toSave = {
        prompts: this.state.prompts || [],
        projects: this.state.projects || [],
        tags: this.state.tags || [],
        ui: this.state.ui || {}
      };
      localStorage.setItem(key, JSON.stringify(toSave));
    } catch (error) {
      console.error('Failed to persist state:', error);
    }
  }

  /**
   * Восстановить состояние из localStorage
   * @param {string} key - Ключ хранилища
   */
  restore(key = 'app-state') {
    try {
      const stored = localStorage.getItem(key);
      if (stored) {
        const data = JSON.parse(stored);
        Object.assign(this.state, data);
      }
    } catch (error) {
      console.error('Failed to restore state:', error);
    }
  }

  /**
   * Сбросить состояние на начальное
   * @param {Object} initialState - Начальное состояние
   */
  reset(initialState = {}) {
    Object.keys(this.state).forEach(key => delete this.state[key]);
    Object.assign(this.state, initialState);
    this.history = [];
    this.historyIndex = -1;
  }

  /**
   * Получить текущую историю
   * @returns {Array} Массив изменений
   */
  getHistory() {
    return this.history.map(item => ({
      ...item,
      timestamp: new Date(item.timestamp).toLocaleTimeString('ru-RU')
    }));
  }

  /**
   * Очистить историю
   */
  clearHistory() {
    this.history = [];
    this.historyIndex = -1;
  }
}

// Экспорт
export default StateManager;

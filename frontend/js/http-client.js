/**
 * ═════════════════════════════════════════════════════════════════════
 * PANDORA v2.0 - HTTP Client & API Manager
 * Advanced HTTP клиент с retry logic, caching, deduplication
 * ═════════════════════════════════════════════════════════════════════
 */

class HTTPClient {
  /**
   * Инициализирует HTTP клиент
   * @param {Object} config - конфигурация
   * @param {string} config.baseUrl - базовый URL API
   * @param {number} config.timeout - таймаут запроса (ms)
   * @param {number} config.retryAttempts - количество повторов
   * @param {number} config.retryDelay - задержка между повторами (ms)
   */
  constructor(config = {}) {
    this.baseUrl = config.baseUrl || '/api';
    this.timeout = config.timeout || 30000;
    this.retryAttempts = config.retryAttempts || 3;
    this.retryDelay = config.retryDelay || 1000;
    
    // Cache для GET запросов
    this.cache = new Map();
    this.cacheExpiry = new Map();
    this.cacheTTL = config.cacheTTL || 60000; // 1 minute по умолчанию

    // Request deduplication - предотвращает дублирование одновременных запросов
    this.pendingRequests = new Map();

    // Request/Response interceptors
    this.interceptors = {
      request: [],
      response: [],
      error: []
    };

    // Логирование
    this.debug = config.debug || false;
  }

  /**
   * Выполняет GET запрос
   * @param {string} endpoint - URL endpoint
   * @param {Object} options - опции запроса
   */
  async get(endpoint, options = {}) {
    const url = this.buildUrl(endpoint);
    
    // Проверить кэш
    if (!options.skipCache && this.isCacheValid(url)) {
      this.log('Cache hit:', url);
      return this.cache.get(url);
    }

    const fullOptions = {
      method: 'GET',
      headers: this.getHeaders(options.headers),
      signal: this.getAbortSignal(options.timeout),
      ...options
    };

    try {
      const data = await this.request(url, fullOptions);
      
      // Кэшировать результат
      if (!options.skipCache) {
        this.setCacheData(url, data);
      }

      return data;
    } catch (error) {
      this.handleError(error, 'GET', url, options);
      throw error;
    }
  }

  /**
   * Выполняет POST запрос
   */
  async post(endpoint, body = {}, options = {}) {
    const url = this.buildUrl(endpoint);

    const fullOptions = {
      method: 'POST',
      headers: this.getHeaders({
        'Content-Type': 'application/json',
        ...options.headers
      }),
      body: JSON.stringify(body),
      signal: this.getAbortSignal(options.timeout),
      ...options
    };

    try {
      const data = await this.request(url, fullOptions);
      
      // Инвалидировать кэш для связанных GET запросов
      this.invalidateRelatedCache(endpoint);

      return data;
    } catch (error) {
      this.handleError(error, 'POST', url, options);
      throw error;
    }
  }

  /**
   * Выполняет PUT запрос
   */
  async put(endpoint, body = {}, options = {}) {
    const url = this.buildUrl(endpoint);

    const fullOptions = {
      method: 'PUT',
      headers: this.getHeaders({
        'Content-Type': 'application/json',
        ...options.headers
      }),
      body: JSON.stringify(body),
      signal: this.getAbortSignal(options.timeout),
      ...options
    };

    try {
      const data = await this.request(url, fullOptions);
      this.invalidateRelatedCache(endpoint);
      return data;
    } catch (error) {
      this.handleError(error, 'PUT', url, options);
      throw error;
    }
  }

  /**
   * Выполняет DELETE запрос
   */
  async delete(endpoint, options = {}) {
    const url = this.buildUrl(endpoint);

    const fullOptions = {
      method: 'DELETE',
      headers: this.getHeaders(options.headers),
      signal: this.getAbortSignal(options.timeout),
      ...options
    };

    try {
      const data = await this.request(url, fullOptions);
      this.invalidateRelatedCache(endpoint);
      return data;
    } catch (error) {
      this.handleError(error, 'DELETE', url, options);
      throw error;
    }
  }

  /**
   * Core метод для выполнения HTTP запроса с retry logic
   */
  async request(url, options = {}, attemptNumber = 0) {
    // Deduplication: если такой запрос уже выполняется, вернуть то же Promise
    const requestKey = `${options.method || 'GET'}:${url}`;
    if (this.pendingRequests.has(requestKey)) {
      this.log('Request deduplicated:', requestKey);
      return this.pendingRequests.get(requestKey);
    }

    // Создать Promise для запроса
    const requestPromise = this.executeRequest(url, options, attemptNumber);
    this.pendingRequests.set(requestKey, requestPromise);

    try {
      const result = await requestPromise;
      return result;
    } finally {
      this.pendingRequests.delete(requestKey);
    }
  }

  /**
   * Выполняет запрос с retry logic
   */
  async executeRequest(url, options = {}, attemptNumber = 0) {
    this.log(`Attempt ${attemptNumber + 1}/${this.retryAttempts}: ${options.method} ${url}`);

    try {
      const response = await Promise.race([
        fetch(url, options),
        this.createTimeoutPromise(options.timeout || this.timeout)
      ]);

      if (!response.ok) {
        const error = new Error(`HTTP ${response.status}: ${response.statusText}`);
        error.status = response.status;
        error.response = response;
        throw error;
      }

      const contentType = response.headers.get('content-type');
      let data;

      if (contentType && contentType.includes('application/json')) {
        data = await response.json();
      } else {
        data = await response.text();
      }

      // Response interceptors
      for (const interceptor of this.interceptors.response) {
        data = await interceptor(data, response);
      }

      return data;

    } catch (error) {
      // Определить стоит ли retry
      const shouldRetry = this.shouldRetry(error, attemptNumber);

      if (shouldRetry) {
        const delay = this.retryDelay * Math.pow(2, attemptNumber); // Exponential backoff
        this.log(`Retrying after ${delay}ms...`);
        
        await new Promise(resolve => setTimeout(resolve, delay));
        return this.executeRequest(url, options, attemptNumber + 1);
      }

      // Error interceptors
      for (const interceptor of this.interceptors.error) {
        const handled = await interceptor(error);
        if (handled) {
          return handled;
        }
      }

      throw error;
    }
  }

  /**
   * Определяет стоит ли повторить запрос
   */
  shouldRetry(error, attemptNumber) {
    if (attemptNumber >= this.retryAttempts) {
      return false;
    }

    // Retry для network errors
    if (error.message.includes('Failed to fetch')) {
      return true;
    }

    // Retry для timeout
    if (error.name === 'AbortError') {
      return true;
    }

    // Retry для 5xx ошибок
    if (error.status >= 500) {
      return true;
    }

    // Не retry для 4xx ошибок
    if (error.status >= 400 && error.status < 500) {
      return false;
    }

    return false;
  }

  /**
   * Builds полный URL из endpoint
   */
  buildUrl(endpoint) {
    if (endpoint.startsWith('http://') || endpoint.startsWith('https://')) {
      return endpoint;
    }

    const cleanEndpoint = endpoint.startsWith('/') ? endpoint : `/${endpoint}`;
    return `${this.baseUrl}${cleanEndpoint}`;
  }

  /**
   * Получить headers с автоматическими
   */
  getHeaders(customHeaders = {}) {
    return {
      'Accept': 'application/json',
      'X-Requested-With': 'XMLHttpRequest',
      ...customHeaders
    };
  }

  /**
   * Создать abort signal с таймаутом
   */
  getAbortSignal(timeout = null) {
    const controller = new AbortController();
    const actualTimeout = timeout || this.timeout;

    setTimeout(() => {
      controller.abort();
    }, actualTimeout);

    return controller.signal;
  }

  /**
   * Создать Promise который reject через определённое время
   */
  createTimeoutPromise(ms) {
    return new Promise((_, reject) => {
      setTimeout(() => {
        reject(new Error(`Request timeout after ${ms}ms`));
      }, ms);
    });
  }

  /**
   * Кэширование данных
   */
  setCacheData(key, data) {
    this.cache.set(key, data);
    this.cacheExpiry.set(key, Date.now() + this.cacheTTL);
  }

  /**
   * Проверить валидность кэша
   */
  isCacheValid(key) {
    if (!this.cache.has(key)) {
      return false;
    }

    const expiry = this.cacheExpiry.get(key);
    if (Date.now() > expiry) {
      this.cache.delete(key);
      this.cacheExpiry.delete(key);
      return false;
    }

    return true;
  }

  /**
   * Инвалидировать связанный кэш
   */
  invalidateRelatedCache(endpoint) {
    // Инвалидировать GET запросы для этого endpoint
    const keysToInvalidate = [];
    for (const [key] of this.cache) {
      try {
        const cacheKey = key.split(':')[1]?.split('?')[0];
        if (key.includes(endpoint) || (cacheKey && endpoint.includes(cacheKey))) {
          keysToInvalidate.push(key);
        }
      } catch (e) {
        // Skip invalid cache keys
      }
    }

    keysToInvalidate.forEach(key => {
      this.cache.delete(key);
      this.cacheExpiry.delete(key);
    });
  }

  /**
   * Очистить кэш
   */
  clearCache() {
    this.cache.clear();
    this.cacheExpiry.clear();
  }

  /**
   * Добавить interceptor
   */
  addInterceptor(type, fn) {
    if (this.interceptors[type]) {
      this.interceptors[type].push(fn);
    }
  }

  /**
   * Логирование (если debug=true)
   */
  log(...args) {
    if (this.debug) {
      console.log('[HTTPClient]', ...args);
    }
  }

  /**
   * Обработка ошибок
   */
  handleError(error, method, url, options) {
    const errorInfo = {
      method,
      url,
      message: error.message,
      status: error.status,
      timestamp: new Date().toISOString()
    };

    console.error('[HTTPClient Error]', errorInfo);

    // Логирование на сервер (может быть добавлено в будущем)
    // Здесь можно отправить ошибку на сервер для анализа
  }
}

// Экспорт
if (typeof module !== 'undefined' && module.exports) {
  module.exports = HTTPClient;
}

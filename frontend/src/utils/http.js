/**
 * HTTP Client with interceptors, retry logic, caching
 */

export class HTTPClient {
  constructor(baseURL = '') {
    this.baseURL = baseURL;
    this.interceptors = {
      request: [],
      response: [],
      error: []
    };
    this.cache = new Map();
    this.pendingRequests = new Map();
  }

  /**
   * GET request
   */
  async get(url, options = {}) {
    return this.request(url, { ...options, method: 'GET' });
  }

  /**
   * POST request
   */
  async post(url, data, options = {}) {
    return this.request(url, { ...options, method: 'POST', body: data });
  }

  /**
   * PUT request
   */
  async put(url, data, options = {}) {
    return this.request(url, { ...options, method: 'PUT', body: data });
  }

  /**
   * DELETE request
   */
  async delete(url, options = {}) {
    return this.request(url, { ...options, method: 'DELETE' });
  }

  /**
   * Main request method
   */
  async request(url, options = {}) {
    const fullURL = url.startsWith('http') ? url : this.baseURL + url;
    const cacheKey = `${options.method || 'GET'}:${fullURL}`;

    // Check cache
    if (options.cache && this.cache.has(cacheKey)) {
      return this.cache.get(cacheKey);
    }

    // Check pending request deduplication
    if (this.pendingRequests.has(cacheKey)) {
      return this.pendingRequests.get(cacheKey);
    }

    // Run request interceptors
    let finalOptions = { ...options };
    for (const interceptor of this.interceptors.request) {
      finalOptions = await interceptor(finalOptions);
    }

    // Prepare request
    const config = {
      method: finalOptions.method || 'GET',
      headers: {
        'Content-Type': 'application/json',
        ...finalOptions.headers
      }
    };

    if (finalOptions.body) {
      config.body = typeof finalOptions.body === 'string' 
        ? finalOptions.body 
        : JSON.stringify(finalOptions.body);
    }

    // Create promise
    const promise = fetch(fullURL, config)
      .then(async res => {
        let data;
        try {
          data = await res.json();
        } catch {
          data = await res.text();
        }

        const response = {
          status: res.status,
          statusText: res.statusText,
          headers: res.headers,
          data
        };

        if (!res.ok) {
          throw response;
        }

        // Run response interceptors
        for (const interceptor of this.interceptors.response) {
          response = await interceptor(response);
        }

        // Cache if requested
        if (finalOptions.cache) {
          this.cache.set(cacheKey, response);
        }

        return response;
      })
      .catch(async error => {
        // Run error interceptors
        for (const interceptor of this.interceptors.error) {
          try {
            return await interceptor(error);
          } catch (e) {
            // Continue to next interceptor
          }
        }

        // Retry logic
        if (finalOptions.retry && !finalOptions._retryCount) {
          finalOptions._retryCount = 1;
          await new Promise(r => setTimeout(r, 1000));
          return this.request(url, finalOptions);
        }

        throw error;
      });

    // Store pending request
    this.pendingRequests.set(cacheKey, promise);

    try {
      return await promise;
    } finally {
      this.pendingRequests.delete(cacheKey);
    }
  }

  /**
   * Add interceptor
   */
  addInterceptor(type, fn) {
    if (this.interceptors[type]) {
      this.interceptors[type].push(fn);
    }
  }

  /**
   * Clear cache
   */
  clearCache() {
    this.cache.clear();
  }

  /**
   * Set cache for specific key
   */
  setCache(key, value, ttl = null) {
    this.cache.set(key, value);
    if (ttl) {
      setTimeout(() => this.cache.delete(key), ttl);
    }
  }
}

// Create default HTTP client instance
export const http = new HTTPClient('http://127.0.0.1:8000/api');

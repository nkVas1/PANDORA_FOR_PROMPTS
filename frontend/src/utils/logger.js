/**
 * Frontend Logger - Centralized logging system
 * Логирует все ошибки, предупреждения и другие события на клиенте
 * 
 * Usage:
 * Logger.error('Error message', error_object)
 * Logger.warn('Warning message', context_data)
 * Logger.info('Info message')
 * Logger.debug('Debug message', debug_data)
 */

class LoggerManager {
    constructor() {
        this.logs = [];
        this.maxLogs = 1000;
        this.enableConsole = true;
        this.logLevels = {
            DEBUG: 0,
            INFO: 1,
            WARN: 2,
            ERROR: 3,
            CRITICAL: 4
        };
        this.currentLevel = this.logLevels.DEBUG;
        
        // Перехватываем console методы
        this._interceptConsole();
        
        // Перехватываем unhandled errors
        this._setupErrorHandlers();
    }

    /**
     * Логировать ошибку
     */
    error(message, data = null) {
        this._log('ERROR', message, data, 'error');
    }

    /**
     * Логировать предупреждение
     */
    warn(message, data = null) {
        this._log('WARN', message, data, 'warn');
    }

    /**
     * Логировать информацию
     */
    info(message, data = null) {
        this._log('INFO', message, data, 'info');
    }

    /**
     * Логировать отладку
     */
    debug(message, data = null) {
        this._log('DEBUG', message, data, 'debug');
    }

    /**
     * Логировать критическую ошибку
     */
    critical(message, data = null) {
        this._log('CRITICAL', message, data, 'error');
    }

    /**
     * Внутренняя функция логирования
     */
    _log(level, message, data = null, consoleMethod = 'log') {
        const timestamp = this._getTimestamp();
        const logEntry = {
            timestamp,
            level,
            message,
            data,
            stackTrace: this._getStackTrace(),
            userAgent: navigator.userAgent,
            url: window.location.href
        };

        this.logs.push(logEntry);

        // Ограничиваем размер логов
        if (this.logs.length > this.maxLogs) {
            this.logs.shift();
        }

        // Вывод в консоль если включено
        if (this.enableConsole) {
            const consoleData = data ? [message, data] : [message];
            if (console[consoleMethod]) {
                console[consoleMethod](`[${timestamp}] [${level}] ${message}`, data);
            }
        }

        // Отправляем на сервер если это ошибка
        if (level === 'ERROR' || level === 'CRITICAL') {
            this._sendToServer(logEntry);
        }
    }

    /**
     * Получить текущее время в формате HH:MM:SS
     */
    _getTimestamp() {
        const now = new Date();
        return now.toLocaleTimeString('ru-RU', { 
            hour12: false,
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit'
        });
    }

    /**
     * Получить stack trace
     */
    _getStackTrace() {
        try {
            throw new Error();
        } catch (e) {
            return e.stack;
        }
    }

    /**
     * Перехватываем console.log, console.error и т.д.
     */
    _interceptConsole() {
        const self = this;
        const originalLog = console.log;
        const originalError = console.error;
        const originalWarn = console.warn;

        console.log = function(...args) {
            originalLog.apply(console, args);
            // self._log('DEBUG', args.join(' '), null);
        };

        console.error = function(...args) {
            originalError.apply(console, args);
            self._log('ERROR', args.join(' '), args);
        };

        console.warn = function(...args) {
            originalWarn.apply(console, args);
            self._log('WARN', args.join(' '), args);
        };
    }

    /**
     * Перехватываем unhandled errors
     */
    _setupErrorHandlers() {
        const self = this;

        // Unhandled Promise Rejections
        window.addEventListener('unhandledrejection', (event) => {
            self.error('Unhandled Promise Rejection', {
                reason: event.reason,
                promise: event.promise
            });
        });

        // Global Error Handler
        window.addEventListener('error', (event) => {
            self.error('Global Error', {
                message: event.message,
                filename: event.filename,
                lineno: event.lineno,
                colno: event.colno,
                error: event.error
            });
        });
    }

    /**
     * Отправить логи на сервер
     */
    _sendToServer(logEntry) {
        try {
            // Отправляем на специальный endpoint если он существует
            if (window.http && window.http.post) {
                window.http.post('/api/logs', logEntry).catch(err => {
                    console.error('Failed to send log to server:', err);
                });
            }
        } catch (err) {
            console.error('Error sending log to server:', err);
        }
    }

    /**
     * Экспортировать логи в JSON
     */
    export() {
        return JSON.stringify(this.logs, null, 2);
    }

    /**
     * Получить все логи
     */
    getLogs() {
        return this.logs;
    }

    /**
     * Получить логи конкретного уровня
     */
    getLogsByLevel(level) {
        return this.logs.filter(log => log.level === level);
    }

    /**
     * Очистить логи
     */
    clear() {
        this.logs = [];
    }

    /**
     * Получить статистику логов
     */
    getStats() {
        const stats = {};
        Object.keys(this.logLevels).forEach(level => {
            stats[level] = this.logs.filter(log => log.level === level).length;
        });
        return stats;
    }

    /**
     * Вывести логи в консоль красиво
     */
    printStats() {
        const stats = this.getStats();
        console.group('📊 Log Statistics');
        Object.entries(stats).forEach(([level, count]) => {
            console.log(`${level}: ${count}`);
        });
        console.groupEnd();
    }
}

// Глобальный экземпляр
export const Logger = new LoggerManager();

// Также доступен как window.Logger
window.Logger = Logger;

export default Logger;

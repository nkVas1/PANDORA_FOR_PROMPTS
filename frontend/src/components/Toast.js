/**
 * Toast Notification System
 * 
 * Система уведомлений для показа сообщений пользователю
 * 
 * Usage:
 * Toast.success('Operation completed!')
 * Toast.error('Something went wrong')
 * Toast.warning('Warning message')
 * Toast.info('Information message')
 */

class ToastManager {
    constructor() {
        this.container = this._createContainer();
        this.toasts = [];
    }

    _createContainer() {
        if (document.getElementById('toast-container')) {
            return document.getElementById('toast-container');
        }

        const container = document.createElement('div');
        container.id = 'toast-container';
        container.style.cssText = `
            position: fixed;
            bottom: 20px;
            right: 20px;
            z-index: 9999;
            display: flex;
            flex-direction: column;
            gap: 10px;
            pointer-events: none;
        `;
        document.body.appendChild(container);
        return container;
    }

    /**
     * Показать toast уведомление
     * @param {string} message - Текст сообщения
     * @param {string} type - Тип ('success', 'error', 'warning', 'info')
     * @param {number} duration - Длительность в мс (0 = не скрывать автоматически)
     */
    show(message, type = 'info', duration = 4000) {
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        toast.style.cssText = `
            padding: 12px 16px;
            border-radius: 8px;
            font-size: 14px;
            font-weight: 500;
            display: flex;
            align-items: center;
            gap: 12px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
            pointer-events: auto;
            cursor: pointer;
            animation: slideInRight 0.3s ease;
            min-width: 300px;
            max-width: 400px;
            word-break: break-word;
        `;

        // Иконки для разных типов
        const icons = {
            success: '✓',
            error: '✕',
            warning: '⚠',
            info: 'ℹ'
        };

        const icon = document.createElement('span');
        icon.textContent = icons[type] || icons.info;
        icon.style.cssText = `
            flex-shrink: 0;
            font-weight: bold;
            font-size: 16px;
        `;

        const text = document.createElement('span');
        text.textContent = message;

        const closeBtn = document.createElement('button');
        closeBtn.textContent = '✕';
        closeBtn.style.cssText = `
            flex-shrink: 0;
            background: none;
            border: none;
            color: inherit;
            cursor: pointer;
            font-size: 16px;
            padding: 0;
            margin-left: auto;
            opacity: 0.7;
            transition: opacity 0.2s;
        `;

        closeBtn.addEventListener('mouseenter', () => closeBtn.style.opacity = '1');
        closeBtn.addEventListener('mouseleave', () => closeBtn.style.opacity = '0.7');
        closeBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            this._removeToast(toast);
        });

        toast.appendChild(icon);
        toast.appendChild(text);
        toast.appendChild(closeBtn);

        // Применяем цвета в зависимости от типа
        this._applyToastStyle(toast, type);

        this.container.appendChild(toast);
        this.toasts.push(toast);

        // Auto-hide
        if (duration > 0) {
            setTimeout(() => this._removeToast(toast), duration);
        }

        return toast;
    }

    _applyToastStyle(toast, type) {
        const styles = {
            success: {
                backgroundColor: '#10b981',
                color: '#ffffff'
            },
            error: {
                backgroundColor: '#ef4444',
                color: '#ffffff'
            },
            warning: {
                backgroundColor: '#f59e0b',
                color: '#ffffff'
            },
            info: {
                backgroundColor: '#3b82f6',
                color: '#ffffff'
            }
        };

        const style = styles[type] || styles.info;
        toast.style.backgroundColor = style.backgroundColor;
        toast.style.color = style.color;
    }

    _removeToast(toast) {
        toast.style.animation = 'slideOutRight 0.3s ease';
        setTimeout(() => {
            toast.remove();
            this.toasts = this.toasts.filter(t => t !== toast);
        }, 300);
    }

    success(message, duration = 3000) {
        return this.show(message, 'success', duration);
    }

    error(message, duration = 5000) {
        return this.show(message, 'error', duration);
    }

    warning(message, duration = 4000) {
        return this.show(message, 'warning', duration);
    }

    info(message, duration = 4000) {
        return this.show(message, 'info', duration);
    }

    /**
     * Показать toast с кастомной иконкой
     */
    custom(message, icon = '•', backgroundColor = '#6b7280', duration = 4000) {
        const toast = document.createElement('div');
        toast.className = 'toast';
        toast.style.cssText = `
            padding: 12px 16px;
            border-radius: 8px;
            font-size: 14px;
            font-weight: 500;
            display: flex;
            align-items: center;
            gap: 12px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
            pointer-events: auto;
            cursor: pointer;
            animation: slideInRight 0.3s ease;
            min-width: 300px;
            max-width: 400px;
            word-break: break-word;
            background-color: ${backgroundColor};
            color: white;
        `;

        const iconEl = document.createElement('span');
        iconEl.textContent = icon;
        iconEl.style.cssText = `
            flex-shrink: 0;
            font-weight: bold;
            font-size: 16px;
        `;

        const text = document.createElement('span');
        text.textContent = message;

        const closeBtn = document.createElement('button');
        closeBtn.textContent = '✕';
        closeBtn.style.cssText = `
            flex-shrink: 0;
            background: none;
            border: none;
            color: inherit;
            cursor: pointer;
            font-size: 16px;
            padding: 0;
            margin-left: auto;
            opacity: 0.7;
            transition: opacity 0.2s;
        `;

        closeBtn.addEventListener('mouseenter', () => closeBtn.style.opacity = '1');
        closeBtn.addEventListener('mouseleave', () => closeBtn.style.opacity = '0.7');
        closeBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            this._removeToast(toast);
        });

        toast.appendChild(iconEl);
        toast.appendChild(text);
        toast.appendChild(closeBtn);

        this.container.appendChild(toast);
        this.toasts.push(toast);

        if (duration > 0) {
            setTimeout(() => this._removeToast(toast), duration);
        }

        return toast;
    }
}

// Глобальный экземпляр
export const Toast = new ToastManager();

// Добавляем стили для анимаций
const style = document.createElement('style');
style.textContent = `
    @keyframes slideInRight {
        from {
            opacity: 0;
            transform: translateX(400px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }

    @keyframes slideOutRight {
        from {
            opacity: 1;
            transform: translateX(0);
        }
        to {
            opacity: 0;
            transform: translateX(400px);
        }
    }

    .toast:hover {
        box-shadow: 0 6px 16px rgba(0, 0, 0, 0.2);
    }
`;
document.head.appendChild(style);

export default Toast;

/**
 * ═════════════════════════════════════════════════════════════════════
 * PANDORA v2.0 - Enhanced Editor Module
 * Расширенный редактор для написания и редактирования промптов
 * ═════════════════════════════════════════════════════════════════════
 */

class PromptEditor {
    /**
     * Инициализирует редактор промптов
     * @param {Object} config - конфигурация редактора
     * @param {string} config.containerId - ID контейнера
     * @param {HTTPClient} config.http - HTTP клиент (от app.js)
     * @param {Function} config.onSave - callback при сохранении
     */
    constructor(config = {}) {
        this.containerId = config.containerId || 'editor-container';
        this.http = config.http || window.App?.http; // Используем глобальный HTTP клиент
        this.onSave = config.onSave || (() => {});
        
        // Состояние редактора
        this.state = {
            content: '',
            title: '',
            category: 'General',
            tags: [],
            isDirty: false,
            isSaving: false,
            autoSaveInterval: null,
            wordCount: 0,
            charCount: 0,
            versionHistory: [],
            currentVersion: 0
        };

        // Элементы DOM
        this.elements = {};
        
        // Инициализация
        this.init();
    }

    /**
     * Сохраняет промпт на сервер
     * @param {Object} data - данные для сохранения
     * @returns {Promise}
     */
    async save(data = {}) {
        if (this.state.isSaving) return;
        this.state.isSaving = true;
        return `${baseUrl}${cleanEndpoint}`;
    }

    /**
     * Инициализирует редактор
     */
    init() {
        console.log('📝 Инициализирую Enhanced Editor');
        
        // Кэш элементов DOM
        this.cacheElements();
        
        // Привязать обработчики событий
        this.bindEvents();
        
        // Инициализировать Markdown preview
        this.initMarkdownPreview();
        
        // Запустить auto-save (каждые 30 секунд)
        this.startAutoSave(30000);
        
        console.log('✅ Enhanced Editor готов');
    }

    /**
     * Кэширует ссылки на элементы DOM
     */
    cacheElements() {
        const container = document.getElementById(this.containerId);
        if (!container) {
            console.error(`Container #${this.containerId} not found`);
            return;
        }

        this.elements = {
            container: container,
            titleInput: container.querySelector('.editor-title-input'),
            contentArea: container.querySelector('.editor-content-textarea'),
            categorySelect: container.querySelector('.editor-category-select'),
            tagsInput: container.querySelector('.editor-tags-input'),
            previewPane: container.querySelector('.editor-preview-pane'),
            charCounter: container.querySelector('.editor-char-count'),
            wordCounter: container.querySelector('.editor-word-count'),
            saveBtn: container.querySelector('.editor-save-btn'),
            undoBtn: container.querySelector('.editor-undo-btn'),
            redoBtn: container.querySelector('.editor-redo-btn'),
            versionHistory: container.querySelector('.editor-version-history'),
            statusBar: container.querySelector('.editor-status-bar'),
            highlightedContent: container.querySelector('.editor-syntax-highlight')
        };
    }

    /**
     * Привязывает обработчики событий
     */
    bindEvents() {
        // Обновление счетчиков при вводе
        this.elements.contentArea?.addEventListener('input', (e) => {
            this.handleContentChange(e);
        });

        this.elements.titleInput?.addEventListener('input', (e) => {
            this.state.title = e.target.value;
            this.markDirty();
        });

        this.elements.categorySelect?.addEventListener('change', (e) => {
            this.state.category = e.target.value;
            this.markDirty();
        });

        this.elements.tagsInput?.addEventListener('change', (e) => {
            this.state.tags = e.target.value.split(',').map(t => t.trim()).filter(Boolean);
            this.markDirty();
        });

        // Кнопки действий
        this.elements.saveBtn?.addEventListener('click', () => this.save());
        this.elements.undoBtn?.addEventListener('click', () => this.undo());
        this.elements.redoBtn?.addEventListener('click', () => this.redo());

        // Горячие клавиши
        document.addEventListener('keydown', (e) => {
            if (e.ctrlKey || e.metaKey) {
                if (e.key === 's') {
                    e.preventDefault();
                    this.save();
                } else if (e.key === 'z') {
                    e.preventDefault();
                    e.shiftKey ? this.redo() : this.undo();
                }
            }
        });
    }

    /**
     * Обработчик изменения содержимого
     */
    handleContentChange(event) {
        const content = event.target.value;
        
        // Обновить состояние
        this.state.content = content;
        this.markDirty();
        
        // Обновить счетчики
        this.updateCounters(content);
        
        // Обновить подсветку синтаксиса
        this.updateSyntaxHighlight(content);
        
        // Обновить превью
        this.updateMarkdownPreview(content);
    }

    /**
     * Обновляет счетчики символов и слов
     */
    updateCounters(content) {
        this.state.charCount = content.length;
        this.state.wordCount = content.trim().split(/\s+/).filter(w => w.length > 0).length;
        
        // Обновить DOM
        if (this.elements.charCounter) {
            this.elements.charCounter.textContent = `${this.state.charCount} символов`;
        }
        if (this.elements.wordCounter) {
            this.elements.wordCounter.textContent = `${this.state.wordCount} слов`;
        }
    }

    /**
     * Обновляет подсветку синтаксиса (простая реализация)
     */
    updateSyntaxHighlight(content) {
        if (!this.elements.highlightedContent) return;
        
        // Простая подсветка: выделение кода в `backticks`
        let highlighted = content
            .replace(/```([\s\S]*?)```/g, (match) => {
                return `<div class="code-block">${this.escapeHtml(match)}</div>`;
            })
            .replace(/`([^`]*)`/g, (match) => {
                return `<code class="inline-code">${this.escapeHtml(match)}</code>`;
            });
        
        this.elements.highlightedContent.innerHTML = highlighted;
    }

    /**
     * Инициализирует Markdown preview
     */
    initMarkdownPreview() {
        if (!this.elements.previewPane) return;
        
        // Если есть markdown library, используем её
        if (typeof marked !== 'undefined') {
            console.log('📄 Markdown library (marked.js) найдена');
        } else {
            console.warn('⚠️ Markdown library не найдена (marked.js). Используется basic preview.');
        }
    }

    /**
     * Обновляет Markdown превью
     */
    updateMarkdownPreview(content) {
        if (!this.elements.previewPane) return;
        
        let preview;
        
        // Если есть marked.js, используем его
        if (typeof marked !== 'undefined') {
            try {
                preview = marked.parse(content);
            } catch (e) {
                preview = this.basicMarkdownPreview(content);
            }
        } else {
            preview = this.basicMarkdownPreview(content);
        }
        
        this.elements.previewPane.innerHTML = preview;
    }

    /**
     * Простой Markdown превью без библиотеки
     */
    basicMarkdownPreview(content) {
        return content
            // Заголовки
            .replace(/^### (.*?)$/gm, '<h3>$1</h3>')
            .replace(/^## (.*?)$/gm, '<h2>$1</h2>')
            .replace(/^# (.*?)$/gm, '<h1>$1</h1>')
            // Жирный текст
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/__( .*?)__/g, '<strong>$1</strong>')
            // Курсив
            .replace(/\*(.*?)\*/g, '<em>$1</em>')
            .replace(/_( .*?)_/g, '<em>$1</em>')
            // Списки
            .replace(/^\* (.*?)$/gm, '<li>$1</li>')
            .replace(/^\- (.*?)$/gm, '<li>$1</li>')
            // Коды блоков
            .replace(/```([\s\S]*?)```/g, '<pre><code>$1</code></pre>')
            // Inline коды
            .replace(/`([^`]*)`/g, '<code>$1</code>')
            // Новые строки
            .replace(/\n\n/g, '</p><p>')
            .replace(/\n/g, '<br>')
            // Оборачиваем в теги
            .split('<li>')
            .map(part => part.startsWith('</li>') ? '<ul>' + part : part)
            .join('')
            .replace(/<\/li>/g, '</li>\n')
            || `<p>${content}</p>`;
    }

    /**
     * Помечает документ как изменённый
     */
    markDirty() {
        this.state.isDirty = true;
        this.updateStatusBar();
    }

    /**
     * Обновляет строку статуса
     */
    updateStatusBar() {
        if (!this.elements.statusBar) return;
        
        const status = this.state.isDirty ? '⚠️ Несохраненные изменения' : '✅ Все сохранено';
        const lastSaved = new Date().toLocaleTimeString('ru-RU');
        
        this.elements.statusBar.textContent = `${status} | Последнее сохранение: ${lastSaved}`;
        this.elements.statusBar.classList.toggle('status-dirty', this.state.isDirty);
    }

    /**
     * Сохраняет текущее содержимое в историю версий
     */
    saveToHistory() {
        // Сохранить в историю (макс 20 версий)
        if (this.state.versionHistory.length >= 20) {
            this.state.versionHistory.shift();
        }
        
        this.state.versionHistory.push({
            content: this.state.content,
            title: this.state.title,
            timestamp: new Date(),
            wordCount: this.state.wordCount,
            charCount: this.state.charCount
        });
        
        this.state.currentVersion = this.state.versionHistory.length - 1;
        this.updateVersionHistory();
    }

    /**
     * Обновляет отображение истории версий
     */
    updateVersionHistory() {
        if (!this.elements.versionHistory) return;
        
        const list = this.state.versionHistory.map((v, idx) => `
            <div class="version-item ${idx === this.state.currentVersion ? 'active' : ''}" 
                 onclick="editor.loadVersion(${idx})">
                <span class="version-time">${v.timestamp.toLocaleTimeString('ru-RU')}</span>
                <span class="version-preview">${v.title.substring(0, 30)}...</span>
                <span class="version-stats">${v.wordCount} слов</span>
            </div>
        `).join('');
        
        this.elements.versionHistory.innerHTML = list || '<p class="text-neutral-400">История версий пуста</p>';
    }

    /**
     * Загружает версию из истории
     */
    loadVersion(index) {
        const version = this.state.versionHistory[index];
        if (!version) return;
        
        this.state.content = version.content;
        this.state.title = version.title;
        this.state.currentVersion = index;
        
        // Обновить UI
        if (this.elements.contentArea) {
            this.elements.contentArea.value = this.state.content;
        }
        if (this.elements.titleInput) {
            this.elements.titleInput.value = this.state.title;
        }
        
        this.updateCounters(this.state.content);
        this.updateMarkdownPreview(this.state.content);
        this.updateVersionHistory();
        
        console.log(`📂 Загружена версия ${index + 1} из ${this.state.versionHistory.length}`);
    }

    /**
     * Отмена последнего действия
     */
    undo() {
        if (this.state.currentVersion <= 0) {
            console.warn('⚠️ Нечего отменять');
            return;
        }
        
        this.state.currentVersion--;
        this.loadVersion(this.state.currentVersion);
        console.log('↶ Undo выполнен');
    }

    /**
     * Повтор последнего отменённого действия
     */
    redo() {
        if (this.state.currentVersion >= this.state.versionHistory.length - 1) {
            console.warn('⚠️ Нечего повторять');
            return;
        }
        
        this.state.currentVersion++;
        this.loadVersion(this.state.currentVersion);
        console.log('↷ Redo выполнен');
    }

    /**
     * Запускает автосохранение
     */
    startAutoSave(interval = 30000) {
        this.state.autoSaveInterval = setInterval(() => {
            if (this.state.isDirty) {
                console.log('💾 Автосохранение...');
                this.saveToHistory();
                this.state.isDirty = false;
                this.updateStatusBar();
            }
        }, interval);
        
        console.log(`⏰ Автосохранение включено (каждые ${interval / 1000} сек)`);
    }

    /**
     * Останавливает автосохранение
     */
    stopAutoSave() {
        if (this.state.autoSaveInterval) {
            clearInterval(this.state.autoSaveInterval);
            this.state.autoSaveInterval = null;
            console.log('⏸️ Автосохранение отключено');
        }
    }

    /**
     * Сохраняет промпт на сервер
     */
    async save() {
        if (this.state.isSaving) return;
        if (!this.state.content.trim()) {
            alert('⚠️ Содержимое не может быть пустым');
            return;
        }
        
        this.state.isSaving = true;
        
        try {
            // Обновить UI кнопки
            if (this.elements.saveBtn) {
                this.elements.saveBtn.disabled = true;
                this.elements.saveBtn.textContent = '💾 Сохранение...';
            }
            
            // Сохранить в историю
            this.saveToHistory();
            
            // Подготовить данные
            const data = {
                title: this.state.title || 'Без названия',
                content: this.state.content,
                category: this.state.category,
                tags: this.state.tags
            };
            
            // Отправить на сервер (используем HTTP клиент)
            const result = await this.http.post('/prompts', data);
            
            // Вызвать callback
            this.onSave(result);
            
            // Обновить UI
            this.state.isDirty = false;
            this.updateStatusBar();
            
            console.log('✅ Промпт сохранён:', result);
            
        } catch (error) {
            console.error('❌ Ошибка сохранения:', error);
            alert(`Ошибка сохранения: ${error.message}`);
        } finally {
            this.state.isSaving = false;
            
            if (this.elements.saveBtn) {
                this.elements.saveBtn.disabled = false;
                this.elements.saveBtn.textContent = '💾 Сохранить';
            }
        }
    }

    /**
     * Загружает промпт из объекта
     */
    loadPrompt(prompt) {
        this.state.content = prompt.content || '';
        this.state.title = prompt.title || prompt.name || '';
        this.state.category = prompt.category || 'General';
        this.state.tags = prompt.tags?.map(t => t.name || t) || [];
        
        // Обновить UI
        if (this.elements.contentArea) {
            this.elements.contentArea.value = this.state.content;
        }
        if (this.elements.titleInput) {
            this.elements.titleInput.value = this.state.title;
        }
        if (this.elements.categorySelect) {
            this.elements.categorySelect.value = this.state.category;
        }
        if (this.elements.tagsInput) {
            this.elements.tagsInput.value = this.state.tags.join(', ');
        }
        
        // Обновить счетчики и превью
        this.updateCounters(this.state.content);
        this.updateMarkdownPreview(this.state.content);
        this.updateSyntaxHighlight(this.state.content);
        
        // Сохранить начальное состояние в историю
        this.saveToHistory();
        
        console.log('📖 Промпт загружен:', prompt.title);
    }

    /**
     * Очищает редактор
     */
    clear() {
        this.state.content = '';
        this.state.title = '';
        this.state.category = 'General';
        this.state.tags = [];
        this.state.versionHistory = [];
        this.state.currentVersion = 0;
        
        // Очистить UI
        if (this.elements.contentArea) {
            this.elements.contentArea.value = '';
        }
        if (this.elements.titleInput) {
            this.elements.titleInput.value = '';
        }
        if (this.elements.previewPane) {
            this.elements.previewPane.innerHTML = '';
        }
        if (this.elements.versionHistory) {
            this.elements.versionHistory.innerHTML = '';
        }
        
        this.updateCounters('');
        console.log('🗑️ Редактор очищен');
    }

    /**
     * Деструктор - очистить ресурсы
     */
    destroy() {
        this.stopAutoSave();
        console.log('🛑 Enhanced Editor уничтожен');
    }

    /**
     * Утилита для экранирования HTML
     */
    escapeHtml(text) {
        const map = {
            '&': '&amp;',
            '<': '&lt;',
            '>': '&gt;',
            '"': '&quot;',
            "'": '&#039;'
        };
        return text.replace(/[&<>"']/g, m => map[m]);
    }
}

// Экспорт для использования в других модулях
if (typeof module !== 'undefined' && module.exports) {
    module.exports = PromptEditor;
}

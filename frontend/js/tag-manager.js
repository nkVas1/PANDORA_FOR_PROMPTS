/**
 * ═════════════════════════════════════════════════════════════════════
 * PANDORA v2.0 - Tag Manager Module
 * Система управления тегами с UI компонентами
 * ═════════════════════════════════════════════════════════════════════
 */

class TagManager {
    /**
     * Инициализирует менеджер тегов
     * @param {Object} config - конфигурация
     * @param {string} config.containerId - ID контейнера
     * @param {HTTPClient} config.http - HTTP клиент (от app.js)
     * @param {Function} config.onTagsChange - callback при изменении тегов
     */
    constructor(config = {}) {
        this.containerId = config.containerId || 'tags-manager';
        this.http = config.http || window.App?.http; // Используем глобальный HTTP клиент
        this.onTagsChange = config.onTagsChange || (() => {});
        
        // Состояние
        this.state = {
            tags: [],
            selectedTags: [],
            searchQuery: '',
            sortBy: 'name',  // 'name', 'usage', 'recent'
            isLoading: false
        };

        // Элементы DOM
        this.elements = {};
        
        // Инициализация
        this.init();
    }

    /**
     * Построить URL для API запроса
     * @param {string} endpoint - относительный путь (без baseUrl)
     * @returns {string} полный URL
     */
    buildApiUrl(endpoint) {
        const baseUrl = this.api.baseUrl || '/api';
        // Убедиться что endpoint не начинается с /
        const cleanEndpoint = endpoint.startsWith('/') ? endpoint : `/${endpoint}`;
        return `${baseUrl}${cleanEndpoint}`;
    }

    /**
     * Инициализирует менеджер
     */
    async init() {
        console.log('🏷️ Инициализирую Tag Manager');
        
        // Кэш элементов
        this.cacheElements();
        
        // Привязать события
        this.bindEvents();
        
        // Загрузить теги
        await this.loadTags();
        
        console.log('✅ Tag Manager готов');
    }

    /**
     * Кэширует ссылки на DOM элементы
     */
    cacheElements() {
        const container = document.getElementById(this.containerId);
        if (!container) {
            console.error(`Container #${this.containerId} not found`);
            return;
        }

        this.elements = {
            container: container,
            searchInput: container.querySelector('.tags-search-input'),
            addTagBtn: container.querySelector('.tags-add-btn'),
            clearBtn: container.querySelector('.tags-clear-btn'),
            sortSelect: container.querySelector('.tags-sort-select'),
            tagsList: container.querySelector('.tags-list'),
            tagCloud: container.querySelector('.tag-cloud'),
            statsCount: container.querySelector('.tags-stats-count'),
            statsUsage: container.querySelector('.tags-stats-usage')
        };
    }

    /**
     * Привязывает обработчики событий
     */
    bindEvents() {
        // Поиск по тегам
        this.elements.searchInput?.addEventListener('input', (e) => {
            this.state.searchQuery = e.target.value;
            this.renderTags();
        });

        // Кнопка добавления тега
        this.elements.addTagBtn?.addEventListener('click', () => {
            this.showAddTagModal();
        });

        // Кнопка очистки
        this.elements.clearBtn?.addEventListener('click', () => {
            this.state.selectedTags = [];
            this.renderTags();
            this.onTagsChange([]);
        });

        // Сортировка
        this.elements.sortSelect?.addEventListener('change', (e) => {
            this.state.sortBy = e.target.value;
            this.renderTags();
        });
    }

    /**
     * Alias для openCreateModal (для совместимости с handleQuickAction)
     */
    openCreateModal() {
        this.showAddTagModal();
    }

    /**
     * Загружает теги с сервера
     */
    async loadTags() {
        this.state.isLoading = true;
        
        try {
            // Используем HTTP клиент с кэшированием
            const data = await this.http.get('/tags');
            this.state.tags = Array.isArray(data) ? data : data.tags || [];
            
            this.renderTags();
            this.updateStats();
            
            console.log(`✅ Загруженo ${this.state.tags.length} тегов`);

        } catch (error) {
            console.error('❌ Error loading tags:', error);
            if (this.elements.tagsList) {
                this.elements.tagsList.innerHTML = `<p class="text-error">Ошибка загрузки тегов: ${error.message}</p>`;
            }
        } finally {
            this.state.isLoading = false;
        }
    }

    /**
     * Фильтрует и сортирует теги
     */
    getFilteredAndSortedTags() {
        let filtered = this.state.tags;

        // Фильтр по поиску
        if (this.state.searchQuery) {
            const query = this.state.searchQuery.toLowerCase();
            filtered = filtered.filter(tag => 
                tag.name.toLowerCase().includes(query)
            );
        }

        // Сортировка
        const sorted = [...filtered].sort((a, b) => {
            switch (this.state.sortBy) {
                case 'usage':
                    return (b.usage_count || 0) - (a.usage_count || 0);
                case 'recent':
                    return new Date(b.created_at) - new Date(a.created_at);
                case 'name':
                default:
                    return a.name.localeCompare(b.name);
            }
        });

        return sorted;
    }

    /**
     * Отображает список тегов
     */
    renderTags() {
        if (!this.elements.tagsList) return;

        const filtered = this.getFilteredAndSortedTags();

        if (filtered.length === 0) {
            this.elements.tagsList.innerHTML = `
                <div class="tags-empty">
                    <p>🏷️ Теги не найдены</p>
                    <p class="text-secondary">Попробуйте изменить поиск или добавить новый тег</p>
                </div>
            `;
            return;
        }

        const html = filtered.map(tag => `
            <div class="tag-item ${this.state.selectedTags.includes(tag.id) ? 'selected' : ''}">
                <div class="tag-color" style="background-color: ${tag.color || '#3B82F6'}"></div>
                <div class="tag-info">
                    <div class="tag-name" onclick="tagManager.toggleTag(${tag.id})">${this.escapeHtml(tag.name)}</div>
                    <div class="tag-usage">${tag.usage_count || 0} использований</div>
                </div>
                <div class="tag-actions">
                    <button class="tag-edit-btn" onclick="tagManager.showEditTagModal(${tag.id}, event)">
                        ✏️
                    </button>
                    <button class="tag-delete-btn" onclick="tagManager.deleteTag(${tag.id}, event)">
                        🗑️
                    </button>
                </div>
            </div>
        `).join('');

        this.elements.tagsList.innerHTML = html;
    }

    /**
     * Отображает tag cloud (облако тегов)
     */
    renderTagCloud() {
        if (!this.elements.tagCloud) return;

        const sorted = this.getFilteredAndSortedTags();
        
        if (sorted.length === 0) {
            this.elements.tagCloud.innerHTML = '<p class="text-secondary">Облако тегов пусто</p>';
            return;
        }

        // Найти макс и мин использование для масштабирования
        const usageCounts = sorted.map(t => t.usage_count || 0);
        const maxUsage = Math.max(...usageCounts, 1);
        const minUsage = Math.min(...usageCounts);

        const html = sorted.map(tag => {
            // Вычислить размер шрифта на основе количества использований
            const usage = tag.usage_count || 0;
            const size = minUsage === maxUsage 
                ? 1 
                : 0.7 + (usage / maxUsage) * 0.8;
            
            return `
                <button 
                    class="tag-cloud-item" 
                    style="
                        font-size: ${size}rem;
                        background-color: ${tag.color || '#3B82F6'}20;
                        color: ${tag.color || '#3B82F6'};
                        border-color: ${tag.color || '#3B82F6'};
                    "
                    onclick="tagManager.toggleTag(${tag.id})"
                    title="${tag.usage_count || 0} использований">
                    ${this.escapeHtml(tag.name)}
                </button>
            `;
        }).join('');

        this.elements.tagCloud.innerHTML = html;
    }

    /**
     * Переключает выделение тега
     */
    toggleTag(tagId) {
        const index = this.state.selectedTags.indexOf(tagId);
        if (index === -1) {
            this.state.selectedTags.push(tagId);
        } else {
            this.state.selectedTags.splice(index, 1);
        }
        
        this.renderTags();
        this.renderTagCloud();
        this.onTagsChange(this.state.selectedTags);
    }

    /**
     * Показывает модаль для добавления тега
     */
    showAddTagModal() {
        const name = prompt('📝 Введите название тега:');
        if (!name) return;

        const color = prompt('🎨 Выберите цвет (hex, например #FF5733):', '#3B82F6');
        if (!color) return;

        this.createTag(name, color);
    }

    /**
     * Показывает модаль для редактирования тега
     */
    showEditTagModal(tagId, event) {
        event?.stopPropagation?.();
        
        const tag = this.state.tags.find(t => t.id === tagId);
        if (!tag) return;

        const newName = prompt('📝 Обновить название тега:', tag.name);
        if (!newName) return;

        const newColor = prompt('🎨 Обновить цвет (hex):', tag.color);
        if (!newColor) return;

        this.updateTag(tagId, newName, newColor);
    }

    /**
     * Создает новый тег
     */
    async createTag(name, color) {
        try {
            // Используем HTTP клиент
            const newTag = await this.http.post('/tags', { name, color });
            this.state.tags.push(newTag);
            this.renderTags();
            this.renderTagCloud();
            
            console.log('✅ Тег создан:', newTag);

        } catch (error) {
            console.error('❌ Error creating tag:', error);
            alert(`Ошибка создания тега: ${error.message}`);
        }
    }

    /**
     * Обновляет тег
     */
    async updateTag(tagId, name, color) {
        try {
            // Используем HTTP клиент
            const updated = await this.http.put(`/tags/${tagId}`, { name, color });
            const index = this.state.tags.findIndex(t => t.id === tagId);
            if (index !== -1) {
                this.state.tags[index] = updated;
            }

            this.renderTags();
            this.renderTagCloud();
            
            console.log('✅ Тег обновлен:', updated);

        } catch (error) {
            console.error('❌ Error updating tag:', error);
            alert(`Ошибка обновления тега: ${error.message}`);
        }
    }

    /**
     * Удаляет тег
     */
    async deleteTag(tagId, event) {
        event?.stopPropagation?.();

        if (!confirm('⚠️ Удалить этот тег? Это действие необратимо.')) {
            return;
        }

        try {
            const response = await fetch(
                this.buildApiUrl(`tags/${tagId}`),
                { method: 'DELETE' }
            );

            if (!response.ok) {
                throw new Error('Failed to delete tag');
            }

            this.state.tags = this.state.tags.filter(t => t.id !== tagId);
            this.state.selectedTags = this.state.selectedTags.filter(id => id !== tagId);
            
            this.renderTags();
            this.renderTagCloud();
            this.updateStats();
            this.onTagsChange(this.state.selectedTags);
            
            console.log('✅ Тег удален');

        } catch (error) {
            console.error('❌ Error deleting tag:', error);
            alert(`Ошибка удаления тега: ${error.message}`);
        }
    }

    /**
     * Получает выбранные теги
     */
    getSelectedTags() {
        return this.state.selectedTags.map(id => 
            this.state.tags.find(t => t.id === id)
        ).filter(Boolean);
    }

    /**
     * Устанавливает выбранные теги
     */
    setSelectedTags(tagIds) {
        this.state.selectedTags = tagIds;
        this.renderTags();
        this.renderTagCloud();
    }

    /**
     * Обновляет статистику
     */
    updateStats() {
        if (this.elements.statsCount) {
            this.elements.statsCount.textContent = `${this.state.tags.length} тегов`;
        }
        
        if (this.elements.statsUsage) {
            const totalUsage = this.state.tags.reduce((sum, tag) => sum + (tag.usage_count || 0), 0);
            this.elements.statsUsage.textContent = `${totalUsage} использований`;
        }
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

    /**
     * Деструктор
     */
    destroy() {
        console.log('🛑 Tag Manager уничтожен');
    }
}

// Экспорт для использования в других модулях
if (typeof module !== 'undefined' && module.exports) {
    module.exports = TagManager;
}

/**
 * ═════════════════════════════════════════════════════════════════════
 * PANDORA v2.0 - Analytics Dashboard Module
 * Система аналитики использования промптов
 * ═════════════════════════════════════════════════════════════════════
 */

class AnalyticsDashboard {
    /**
     * Инициализирует аналитическую панель
     * @param {Object} config - конфигурация
     * @param {string} config.containerId - ID контейнера
     * @param {Object} config.api - API конфиг
     */
    constructor(config = {}) {
        this.containerId = config.containerId || 'analytics-dashboard';
        this.api = config.api || {};
        
        // Состояние
        this.state = {
            stats: {},
            categoryStats: [],
            isLoading: false,
            refreshInterval: null
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
        const cleanEndpoint = endpoint.startsWith('/') ? endpoint : `/${endpoint}`;
        return `${baseUrl}${cleanEndpoint}`;
    }

    /**
     * Инициализирует dashboard
     */
    async init() {
        console.log('📊 Инициализирую Analytics Dashboard');
        
        // Кэш элементов
        this.cacheElements();
        
        // Привязать события
        this.bindEvents();
        
        // Загрузить статистику
        await this.loadStats();
        
        // Автоматическое обновление каждые 30 сек
        this.startAutoRefresh(30000);
        
        console.log('✅ Analytics Dashboard готов');
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
            statsGrid: container.querySelector('.stats-grid'),
            categoryChart: container.querySelector('.category-chart'),
            trendingList: container.querySelector('.trending-list'),
            refreshBtn: container.querySelector('.analytics-refresh-btn'),
            lastUpdated: container.querySelector('.analytics-last-updated')
        };
    }

    /**
     * Привязывает обработчики событий
     */
    bindEvents() {
        this.elements.refreshBtn?.addEventListener('click', () => {
            this.loadStats();
        });
    }

    /**
     * Загружает статистику с сервера
     */
    async loadStats() {
        this.state.isLoading = true;
        
        try {
            // Загрузить список промптов для расчета статистики
            const prompts = await this.loadPrompts();
            
            // Расчитать статистику на клиенте
            this.state.stats = {
                total_prompts: prompts.length,
                total_categories: [...new Set(prompts.map(p => p.category))].length,
                total_uses: prompts.reduce((sum, p) => sum + (p.use_count || 0), 0),
                most_used: prompts.sort((a, b) => (b.use_count || 0) - (a.use_count || 0))[0]
            };

            this.state.categoryStats = this.calculateCategoryStats(prompts);

            // Отобразить
            this.renderStats();
            this.renderCategoryBreakdown();
            this.renderTrendingPrompts(prompts);
            this.updateLastUpdated();

            console.log('Stats loaded');

        } catch (error) {
            console.error('Error loading stats:', error);
            if (this.elements.statsGrid) {
                this.elements.statsGrid.innerHTML = `<p class="text-error">Error loading statistics: ${error.message}</p>`;
            }
        } finally {
            this.state.isLoading = false;
        }
    }

    /**
     * Загружает список всех промптов
     */
    async loadPrompts() {
        const response = await fetch(
            this.buildApiUrl('prompts'),
            { method: 'GET', headers: { 'Content-Type': 'application/json' } }
        );

        if (!response.ok) {
            throw new Error('Failed to load prompts');
        }

        return await response.json();
    }

    /**
     * Вычисляет статистику по категориям
     */
    calculateCategoryStats(prompts) {
        const stats = {};

        prompts.forEach(prompt => {
            const category = prompt.category || 'General';
            if (!stats[category]) {
                stats[category] = {
                    name: category,
                    count: 0,
                    usages: 0
                };
            }
            stats[category].count++;
            stats[category].usages += prompt.usage_count || 0;
        });

        return Object.values(stats).sort((a, b) => b.count - a.count);
    }

    /**
     * Отображает основную статистику
     */
    renderStats() {
        if (!this.elements.statsGrid) return;

        const stats = this.state.stats;
        
        const html = `
            <div class="stat-card">
                <div class="stat-icon">✨</div>
                <div class="stat-content">
                    <div class="stat-value">${stats.total_prompts || 0}</div>
                    <div class="stat-label">Промптов</div>
                </div>
            </div>

            <div class="stat-card">
                <div class="stat-icon">🏷️</div>
                <div class="stat-content">
                    <div class="stat-value">${stats.total_tags || 0}</div>
                    <div class="stat-label">Тегов</div>
                </div>
            </div>

            <div class="stat-card">
                <div class="stat-icon">📁</div>
                <div class="stat-content">
                    <div class="stat-value">${stats.total_projects || 0}</div>
                    <div class="stat-label">Проектов</div>
                </div>
            </div>

            <div class="stat-card">
                <div class="stat-icon">📂</div>
                <div class="stat-content">
                    <div class="stat-value">${stats.total_categories || 0}</div>
                    <div class="stat-label">Категорий</div>
                </div>
            </div>
        `;

        this.elements.statsGrid.innerHTML = html;
    }

    /**
     * Отображает разбор по категориям
     */
    renderCategoryBreakdown() {
        if (!this.elements.categoryChart) return;

        const stats = this.state.categoryStats;

        if (stats.length === 0) {
            this.elements.categoryChart.innerHTML = '<p class="text-secondary">Нет категорий</p>';
            return;
        }

        // Найти макс и мин для масштабирования
        const maxCount = Math.max(...stats.map(s => s.count), 1);

        const html = stats.map(stat => {
            const percentage = (stat.count / maxCount) * 100;
            return `
                <div class="category-item">
                    <div class="category-header">
                        <span class="category-name">${this.escapeHtml(stat.name)}</span>
                        <span class="category-count">${stat.count}</span>
                    </div>
                    <div class="category-bar">
                        <div class="category-progress" style="width: ${percentage}%"></div>
                    </div>
                    <div class="category-stats">
                        <span>${stat.usages || 0} использований</span>
                    </div>
                </div>
            `;
        }).join('');

        this.elements.categoryChart.innerHTML = html;
    }

    /**
     * Отображает trending prompts
     */
    renderTrendingPrompts(prompts) {
        if (!this.elements.trendingList) return;

        if (!prompts || prompts.length === 0) {
            this.elements.trendingList.innerHTML = '<p class="text-secondary">Нет промптов</p>';
            return;
        }

        // Сортировать по использованию (descending)
        const trending = [...prompts]
            .sort((a, b) => (b.usage_count || 0) - (a.usage_count || 0))
            .slice(0, 5);  // Топ 5

        const html = trending.map((prompt, idx) => {
            const usages = prompt.usage_count || 0;
            const medal = idx === 0 ? '🥇' : idx === 1 ? '🥈' : idx === 2 ? '🥉' : `${idx + 1}.`;
            
            return `
                <div class="trending-item">
                    <div class="trending-rank">${medal}</div>
                    <div class="trending-info">
                        <div class="trending-title">${this.escapeHtml(prompt.title)}</div>
                        <div class="trending-category">${prompt.category || 'General'}</div>
                    </div>
                    <div class="trending-usages">
                        <span class="usages-count">${usages}</span>
                        <span class="usages-label">использований</span>
                    </div>
                </div>
            `;
        }).join('');

        this.elements.trendingList.innerHTML = html;
    }

    /**
     * Обновляет время последнего обновления
     */
    updateLastUpdated() {
        if (!this.elements.lastUpdated) return;
        
        const now = new Date();
        const timeStr = now.toLocaleTimeString('ru-RU');
        this.elements.lastUpdated.textContent = `Последнее обновление: ${timeStr}`;
    }

    /**
     * Запускает автоматическое обновление
     */
    startAutoRefresh(interval = 30000) {
        this.state.refreshInterval = setInterval(() => {
            this.loadStats();
        }, interval);

        console.log(`⏰ Автоматическое обновление включено (каждые ${interval / 1000} сек)`);
    }

    /**
     * Останавливает автоматическое обновление
     */
    stopAutoRefresh() {
        if (this.state.refreshInterval) {
            clearInterval(this.state.refreshInterval);
            this.state.refreshInterval = null;
            console.log('⏸️ Автоматическое обновление отключено');
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
        this.stopAutoRefresh();
        console.log('🛑 Analytics Dashboard уничтожен');
    }
}

// Экспорт для использования в других модулях
if (typeof module !== 'undefined' && module.exports) {
    module.exports = AnalyticsDashboard;
}

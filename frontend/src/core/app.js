/**
 * PANDORA v2.0 - Main Application Bootstrap
 * 
 * Инициализирует основное приложение:
 * - Создает Router для навигации
 * - Инициализирует StateManager для реактивного состояния
 * - Создает HTTPClient для API запросов
 * - Запускает CommandPalette (Cmd+K)
 * - Инициализирует AnimatedGradientMesh фон
 * - Загружает Dashboard по умолчанию
 */

import Router from './router.js';

/**
 * Инициализация приложения
 */
function initApp() {
    console.log('[APP] Initializing PANDORA v2.0...');
    
    // ==================== ROUTER ====================
    /**
     * Создаем Router для управления навигацией
     * Используется hash-based routing (#/dashboard, #/prompts, etc.)
     */
    window.router = new Router({
        container: document.getElementById('app') || document.body,
        defaultRoute: '/dashboard'
    });
    
    // Регистрируем маршруты
    window.router.addRoute('/dashboard', async () => {
        const { default: Dashboard } = await import('../views/Dashboard.js');
        return Dashboard();
    });
    
    window.router.addRoute('/prompts', async () => {
        const { default: PromptsView } = await import('../views/PromptsView.js');
        return PromptsView();
    });
    
    window.router.addRoute('/projects', async () => {
        const { default: ProjectsView } = await import('../views/ProjectsView.js');
        return ProjectsView();
    });
    
    window.router.addRoute('/editor', async () => {
        const { default: EditorView } = await import('../views/EditorView.js');
        return EditorView();
    });
    
    window.router.addRoute('/analytics', async () => {
        const { default: AnalyticsView } = await import('../views/AnalyticsView.js');
        return AnalyticsView();
    });
    
    console.log('[APP] Router initialized');
    
    // ==================== STATE MANAGER ====================
    /**
     * Инициализируем StateManager для реактивного состояния
     * Стейт будет синхронизирован с LocalStorage
     */
    if (window.StateManager) {
        window.appState = new window.StateManager({
            prompts: [],
            projects: [],
            tags: [],
            user: {
                preferences: {
                    theme: 'dark',
                    sidebarOpen: true
                }
            },
            ui: {
                loading: false,
                notification: null,
                sidebarOpen: true,
                currentView: 'dashboard'
            }
        });
        
        // Восстанавливаем состояние из LocalStorage
        window.appState.restore('pandora-app-state');
        
        // Сохраняем состояние при изменениях
        window.appState.observe('*', () => {
            window.appState.persist('pandora-app-state');
        });
        
        console.log('[APP] StateManager initialized');
    } else {
        // Fallback если StateManager не загружен
        window.appState = {
            state: {
                prompts: [],
                projects: [],
                tags: [],
                user: {},
                ui: {}
            },
            observe: () => {},
            persist: () => {},
            restore: () => {}
        };
    }
    
    // ==================== HTTP CLIENT ====================
    /**
     * HTTPClient для API запросов
     * Уже инициализирован в utils/http.js
     * window.http должен быть доступен глобально
     */
    if (!window.http) {
        // Fallback: простой HTTP клиент
        window.http = {
            async get(endpoint) {
                const response = await fetch(endpoint);
                if (!response.ok) throw new Error(`HTTP ${response.status}`);
                return { data: await response.json() };
            },
            async post(endpoint, data) {
                const response = await fetch(endpoint, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data)
                });
                if (!response.ok) throw new Error(`HTTP ${response.status}`);
                return { data: await response.json() };
            },
            async put(endpoint, data) {
                const response = await fetch(endpoint, {
                    method: 'PUT',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data)
                });
                if (!response.ok) throw new Error(`HTTP ${response.status}`);
                return { data: await response.json() };
            },
            async delete(endpoint) {
                const response = await fetch(endpoint, { method: 'DELETE' });
                if (!response.ok) throw new Error(`HTTP ${response.status}`);
                return { data: await response.json() };
            }
        };
    }
    
    console.log('[APP] HTTPClient ready');
    
    // ==================== COMMAND PALETTE ====================
    /**
     * Инициализируем CommandPalette (Cmd+K)
     * Если не загружена, создаем simplified версию
     */
    if (window.CommandPalette) {
        window.commandPalette = new window.CommandPalette();
        
        // Добавляем основные команды
        window.commandPalette.registerCommand({
            id: 'nav-dashboard',
            title: 'Go to Dashboard',
            category: 'Navigation',
            icon: '📊',
            keywords: ['home', 'main', 'dashboard'],
            action: () => window.router.navigate('/dashboard')
        });
        
        window.commandPalette.registerCommand({
            id: 'nav-prompts',
            title: 'Go to Prompts',
            category: 'Navigation',
            icon: '📝',
            keywords: ['prompts', 'list'],
            action: () => window.router.navigate('/prompts')
        });
        
        window.commandPalette.registerCommand({
            id: 'nav-projects',
            title: 'Go to Projects',
            category: 'Navigation',
            icon: '📁',
            keywords: ['projects'],
            action: () => window.router.navigate('/projects')
        });
        
        window.commandPalette.registerCommand({
            id: 'new-prompt',
            title: 'Create New Prompt',
            category: 'Actions',
            icon: '✨',
            keywords: ['new', 'create', 'prompt'],
            shortcut: 'Ctrl+N',
            action: () => window.router.navigate('/editor')
        });
        
        console.log('[APP] CommandPalette initialized');
    }
    
    // ==================== ANIMATED BACKGROUND ====================
    /**
     * Инициализируем анимированный фон с градиентными сферами
     * Если не загружена, это просто визуальное улучшение
     */
    try {
        if (window.AnimatedGradientMesh && !document.querySelector('.animated-gradient-mesh')) {
            new window.AnimatedGradientMesh(document.body, {
                orbCount: 5,
                opacity: 0.4,
                blur: 50,
                speed: 0.3
            });
            console.log('[APP] AnimatedGradientMesh initialized');
        }
    } catch (error) {
        console.warn('[APP] AnimatedGradientMesh initialization failed:', error);
    }
    
    // ==================== NAVIGATE TO DEFAULT VIEW ====================
    /**
     * Переходим на Dashboard по умолчанию
     */
    window.router.navigate('/dashboard');
    
    console.log('[APP] PANDORA v2.0 initialized successfully!');
}

/**
 * Обработчик DOMContentLoaded
 * Ждем пока DOM полностью загрузится перед инициализацией
 */
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initApp);
} else {
    // DOM уже загружен
    initApp();
}

export default initApp;

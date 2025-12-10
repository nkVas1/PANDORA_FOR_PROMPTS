/**
 * PANDORA v2.0 - Main Application Initialization
 * 
 * Главная инициализация:
 * - StateManager (реактивное состояние)
 * - Router (навигация между views)
 * - HTTP Client (запросы к API)
 * - UI Components (CommandPalette, AnimatedBg)
 * - Theme management
 * - Initial data loading
 */

// Simple Router implementation for hash-based routing
class Router {
    constructor({ container, defaultRoute = '/dashboard' } = {}) {
        this.container = container;
        this.routes = new Map();
        this.currentRoute = defaultRoute;
        this.setupHashListener();
    }

    addRoute(path, handler) {
        this.routes.set(path, handler);
    }

    async navigate(path) {
        const handler = this.routes.get(path);
        if (!handler) {
            console.warn(`[Router] Route not found: ${path}`);
            return;
        }
        try {
            const view = await handler();
            if (this.container && view) {
                this.container.innerHTML = '';
                this.container.appendChild(view);
                this.currentRoute = path;
                window.location.hash = path;
            }
        } catch (error) {
            console.error(`[Router] Error navigating to ${path}:`, error);
        }
    }

    setupHashListener() {
        window.addEventListener('hashchange', () => {
            const path = window.location.hash.slice(1) || this.currentRoute;
            this.navigate(path);
        });
    }
}

/**
 * Инициализация приложения
 */
function initApp() {
    console.log('[APP] Initializing PANDORA v2.0...');
    
    // ==================== LAYOUT ====================
    const app = document.getElementById('app');
    app.innerHTML = `
        <div class="main-layout">
            <aside class="sidebar">
                <div class="sidebar-header">
                    <div class="sidebar-logo">
                        <span>📚</span>
                        <span>PANDORA</span>
                    </div>
                </div>
                <nav class="sidebar-nav" id="sidebar-nav">
                    <div class="nav-item active" data-route="dashboard">
                        <span class="nav-icon">📊</span>
                        <span class="nav-label">Dashboard</span>
                    </div>
                    <div class="nav-item" data-route="prompts">
                        <span class="nav-icon">📝</span>
                        <span class="nav-label">Prompts</span>
                    </div>
                    <div class="nav-item" data-route="projects">
                        <span class="nav-icon">📁</span>
                        <span class="nav-label">Projects</span>
                    </div>
                    <div class="nav-item" data-route="editor">
                        <span class="nav-icon">✏️</span>
                        <span class="nav-label">Editor</span>
                    </div>
                    <div class="nav-item" data-route="analytics">
                        <span class="nav-icon">📊</span>
                        <span class="nav-label">Analytics</span>
                    </div>
                </nav>
            </aside>
            
            <div class="content-area">
                <div class="top-bar">
                    <div class="top-bar-left">
                        <h2 style="margin: 0; font-size: 1.25rem;">PANDORA v2.0</h2>
                    </div>
                    <div class="top-bar-right">
                        <button class="command-palette-btn" id="cmd-palette-btn">
                            ⌘ K - Command Palette
                        </button>
                    </div>
                </div>
                <div class="views-container" id="views-container"></div>
            </div>
        </div>
    `;
    
    // ==================== ROUTER ====================
    /**
     * Создаем Router для управления навигацией
     * Используется hash-based routing (#/dashboard, #/prompts, etc.)
     */
    window.router = new Router({
        container: document.getElementById('views-container') || document.body,
        defaultRoute: '/dashboard'
    });
    
    // Регистрируем маршруты
    window.router.addRoute('/dashboard', async () => {
        const { default: Dashboard } = await import('./Dashboard.js');
        return Dashboard();
    });
    
    window.router.addRoute('/prompts', async () => {
        const { default: PromptsView } = await import('./PromptsView.js');
        return PromptsView();
    });
    
    window.router.addRoute('/projects', async () => {
        const { default: ProjectsView } = await import('./ProjectsView.js');
        return ProjectsView();
    });
    
    window.router.addRoute('/editor', async () => {
        const { default: EditorView } = await import('./EditorView.js');
        return EditorView();
    });
    
    window.router.addRoute('/analytics', async () => {
        const { default: AnalyticsView } = await import('./AnalyticsView.js');
        return AnalyticsView();
    });
    
    console.log('[APP] Router initialized');
    
    // ==================== SIDEBAR NAVIGATION ====================
    const navItems = document.querySelectorAll('.nav-item');
    navItems.forEach(item => {
        item.addEventListener('click', (e) => {
            e.preventDefault();
            
            // Update active state
            navItems.forEach(i => i.classList.remove('active'));
            item.classList.add('active');
            
            // Navigate to route
            const route = item.dataset.route;
            window.router.navigate(`/${route}`);
        });
    });
    
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
        window.appState = {
            state: {
                prompts: [],
                projects: [],
                tags: [],
                user: {},
                ui: {}
            },
            get(key) { return this.state[key]; },
            set(key, value) { this.state[key] = value; },
            observe() {},
            persist() {},
            restore() {}
        };
    }
    
    // ==================== HTTP CLIENT ====================
    if (!window.http) {
        window.http = {
            async get(endpoint, options = {}) {
                const url = new URL(endpoint, window.location.origin);
                if (options.params) {
                    Object.entries(options.params).forEach(([k, v]) => {
                        url.searchParams.append(k, v);
                    });
                }
                const response = await fetch(url.toString());
                if (!response.ok) throw new Error(`HTTP ${response.status}`);
                return await response.json();
            },
            async post(endpoint, data) {
                const response = await fetch(endpoint, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data)
                });
                if (!response.ok) throw new Error(`HTTP ${response.status}`);
                return await response.json();
            },
            async put(endpoint, data) {
                const response = await fetch(endpoint, {
                    method: 'PUT',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data)
                });
                if (!response.ok) throw new Error(`HTTP ${response.status}`);
                return await response.json();
            },
            async delete(endpoint) {
                const response = await fetch(endpoint, { method: 'DELETE' });
                if (!response.ok) throw new Error(`HTTP ${response.status}`);
                return await response.json();
            }
        };
    }
    
    console.log('[APP] HTTPClient ready');
    
    // ==================== COMMAND PALETTE ====================
    if (window.CommandPalette) {
        window.commandPalette = new window.CommandPalette();
        window.commandPalette.registerCommand({
            id: 'nav-dashboard',
            title: 'Go to Dashboard',
            category: 'Navigation',
            icon: '📊',
            action: () => window.router.navigate('/dashboard')
        });
        console.log('[APP] CommandPalette initialized');
    }
    
    // ==================== NAVIGATE TO DEFAULT ====================
    window.router.navigate('/dashboard');
    console.log('[APP] ✓ PANDORA v2.0 ready');
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

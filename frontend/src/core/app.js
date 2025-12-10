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

// Import dependencies
import StateManager from './state-manager.js';
import Router from './router.js';
import { HTTPClient } from '../utils/http.js';
import { CommandPalette } from '../components/CommandPalette.js';

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
    window.appState = new StateManager({
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
    
    // ==================== HTTP CLIENT ====================
    window.http = new HTTPClient('http://127.0.0.1:8000/api');
    
    // Add request interceptor for auth token (if exists)
    window.http.addInterceptor('request', (options) => {
        const token = localStorage.getItem('auth-token');
        if (token) {
            options.headers = options.headers || {};
            options.headers['Authorization'] = `Bearer ${token}`;
        }
        return options;
    });
    
    console.log('[APP] HTTPClient ready');
    
    // ==================== COMMAND PALETTE ====================
    window.commandPalette = new CommandPalette();
    
    // Register basic commands
    window.commandPalette.registerCommand({
        id: 'nav-dashboard',
        label: 'Go to Dashboard',
        description: 'Navigate to the main dashboard',
        category: 'Navigation',
        action: () => window.router.navigate('/dashboard')
    });
    
    window.commandPalette.registerCommand({
        id: 'nav-prompts',
        label: 'Go to Prompts',
        description: 'View all prompts',
        category: 'Navigation',
        action: () => window.router.navigate('/prompts')
    });
    
    window.commandPalette.registerCommand({
        id: 'nav-projects',
        label: 'Go to Projects',
        description: 'View all projects',
        category: 'Navigation',
        action: () => window.router.navigate('/projects')
    });
    
    window.commandPalette.registerCommand({
        id: 'new-prompt',
        label: 'New Prompt',
        description: 'Create a new prompt',
        category: 'Actions',
        action: () => window.router.navigate('/editor')
    });
    
    console.log('[APP] CommandPalette initialized');
    
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

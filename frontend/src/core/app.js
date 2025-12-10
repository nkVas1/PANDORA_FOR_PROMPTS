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
        const { default: createDashboard } = await import('../views/Dashboard.js');
        return createDashboard();
    });
    
    window.router.addRoute('/prompts', async () => {
        const { default: createPromptsView } = await import('../views/PromptsView.js');
        return createPromptsView();
    });
    
    window.router.addRoute('/projects', async () => {
        const { default: createProjectsView } = await import('../views/ProjectsView.js');
        return createProjectsView();
    });
    
    window.router.addRoute('/editor', async () => {
        const { default: createEditorView } = await import('../views/EditorView.js');
        return createEditorView();
    });
    
    window.router.addRoute('/analytics', async () => {
        const { default: createAnalyticsView } = await import('../views/AnalyticsView.js');
        return createAnalyticsView();
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
            console.log('[APP] Navigating to:', route);
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
    // Создаем простой HTTP client для API запросов
    window.http = {
        baseURL: 'http://127.0.0.1:8000/api',
        
        async request(method, endpoint, data = null) {
            const url = this.baseURL + endpoint;
            const options = {
                method,
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                }
            };
            
            // Add auth token if exists
            const token = localStorage.getItem('auth-token');
            if (token) {
                options.headers['Authorization'] = `Bearer ${token}`;
            }
            
            if (data && (method === 'POST' || method === 'PUT' || method === 'PATCH')) {
                options.body = JSON.stringify(data);
            }
            
            try {
                console.log(`[HTTP] ${method} ${endpoint}`);
                const response = await fetch(url, options);
                
                if (!response.ok) {
                    console.error(`[HTTP] Error: ${response.status} ${response.statusText}`);
                    const error = new Error(`HTTP ${response.status}`);
                    error.response = response;
                    throw error;
                }
                
                const responseData = await response.json();
                console.log(`[HTTP] ✓ Response:`, responseData);
                return responseData;
            } catch (error) {
                console.error(`[HTTP] ✗ Request failed:`, error);
                throw error;
            }
        },
        
        get(endpoint) {
            return this.request('GET', endpoint);
        },
        
        post(endpoint, data) {
            return this.request('POST', endpoint, data);
        },
        
        put(endpoint, data) {
            return this.request('PUT', endpoint, data);
        },
        
        delete(endpoint) {
            return this.request('DELETE', endpoint);
        }
    };
    
    console.log('[APP] HTTP Client ready at:', window.http.baseURL);
    
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

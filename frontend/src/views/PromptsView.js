/**
 * PromptsView.js - Prompts Management View
 * 
 * Features:
 * - Paginated list of prompts
 * - Search and filter functionality
 * - Create, edit, delete operations
 * - Tag-based organization
 * - Copy to clipboard
 * - Context menu actions
 */

import { createGlassCard } from '../components/GlassCard.js';
import { createButton } from '../components/Button.js';

export default function createPromptsView() {
    const container = document.createElement('div');
    container.className = 'prompts-view';
    
    // ==================== HEADER ====================
    const header = document.createElement('div');
    header.className = 'view-header';
    header.innerHTML = `
        <div class="header-content">
            <h1 class="view-title">📝 Prompts</h1>
            <p class="view-subtitle">Manage your prompt templates and saved prompts</p>
        </div>
    `;
    container.appendChild(header);
    
    // ==================== CONTROLS ====================
    const controls = document.createElement('div');
    controls.className = 'prompts-controls';
    controls.innerHTML = `
        <div class="search-box">
            <input 
                type="text" 
                id="prompts-search" 
                placeholder="Search prompts by name, category, or tags..."
                class="search-input"
            />
            <span class="search-icon">🔍</span>
        </div>
        <div class="filters">
            <select id="prompts-category" class="filter-select">
                <option value="">All Categories</option>
                <option value="writing">Writing</option>
                <option value="code">Code</option>
                <option value="analysis">Analysis</option>
                <option value="creative">Creative</option>
                <option value="custom">Custom</option>
            </select>
            <select id="prompts-sort" class="filter-select">
                <option value="recent">Recent</option>
                <option value="name-asc">Name A-Z</option>
                <option value="name-desc">Name Z-A</option>
                <option value="uses-high">Most Used</option>
            </select>
        </div>
        <button id="btn-new-prompt" class="btn btn-primary">+ New Prompt</button>
    `;
    container.appendChild(controls);
    
    // ==================== PROMPTS LIST ====================
    const prompts = document.createElement('div');
    prompts.className = 'prompts-list';
    prompts.id = 'prompts-list';
    prompts.innerHTML = '<div class="loading">Loading prompts...</div>';
    container.appendChild(prompts);
    
    // ==================== EMPTY STATE ====================
    const emptyState = document.createElement('div');
    emptyState.className = 'empty-state';
    emptyState.innerHTML = `
        <div class="empty-state-icon">📭</div>
        <h3>No prompts yet</h3>
        <p>Create your first prompt to get started</p>
    `;
    emptyState.style.display = 'none';
    container.appendChild(emptyState);
    
    // ==================== PAGINATION ====================
    const pagination = document.createElement('div');
    pagination.className = 'pagination';
    pagination.id = 'prompts-pagination';
    pagination.innerHTML = '<div class="page-info">Page 1 of 1</div>';
    pagination.style.display = 'none';
    container.appendChild(pagination);
    
    // ==================== DATA STATE ====================
    let allPrompts = [];
    let currentPage = 1;
    const itemsPerPage = 12;
    let searchQuery = '';
    let filterCategory = '';
    let sortBy = 'recent';
    
    // ==================== FUNCTIONS ====================
    
    /**
     * Fetch prompts from API
     */
    async function loadPrompts() {
        try {
            if (!window.http) {
                throw new Error('HTTP client not available');
            }
            
            const response = await window.http.get('/api/prompts');
            allPrompts = response.data || response.prompts || [];
            
            if (!Array.isArray(allPrompts)) {
                allPrompts = [];
            }
            
            currentPage = 1;
            renderPrompts();
            
        } catch (error) {
            console.error('Failed to load prompts:', error);
            prompts.innerHTML = `
                <div class="error-message">
                    <p>Failed to load prompts</p>
                    <small>${error.message}</small>
                </div>
            `;
        }
    }
    
    /**
     * Filter and sort prompts
     */
    function getFilteredPrompts() {
        let filtered = allPrompts.filter(prompt => {
            const matchesSearch = !searchQuery || 
                prompt.name?.toLowerCase().includes(searchQuery.toLowerCase()) ||
                prompt.content?.toLowerCase().includes(searchQuery.toLowerCase()) ||
                (prompt.tags && prompt.tags.some(t => t.toLowerCase().includes(searchQuery.toLowerCase())));
            
            const matchesCategory = !filterCategory || prompt.category === filterCategory;
            
            return matchesSearch && matchesCategory;
        });
        
        // Sort
        switch (sortBy) {
            case 'name-asc':
                filtered.sort((a, b) => (a.name || '').localeCompare(b.name || ''));
                break;
            case 'name-desc':
                filtered.sort((a, b) => (b.name || '').localeCompare(a.name || ''));
                break;
            case 'uses-high':
                filtered.sort((a, b) => (b.uses || 0) - (a.uses || 0));
                break;
            case 'recent':
            default:
                filtered.sort((a, b) => 
                    new Date(b.created_at || 0) - new Date(a.created_at || 0)
                );
        }
        
        return filtered;
    }
    
    /**
     * Render prompts list
     */
    function renderPrompts() {
        const filtered = getFilteredPrompts();
        
        if (filtered.length === 0) {
            prompts.innerHTML = '';
            emptyState.style.display = 'flex';
            pagination.style.display = 'none';
            return;
        }
        
        emptyState.style.display = 'none';
        
        // Pagination
        const totalPages = Math.ceil(filtered.length / itemsPerPage);
        const start = (currentPage - 1) * itemsPerPage;
        const pagePrompts = filtered.slice(start, start + itemsPerPage);
        
        // Render cards
        prompts.innerHTML = pagePrompts
            .map(prompt => `
                <div class="prompt-card glass-card" data-id="${prompt.id}">
                    <div class="card-header">
                        <h3 class="card-title">${escapeHtml(prompt.name || 'Untitled')}</h3>
                        <div class="card-actions">
                            <button class="btn-icon" title="Copy">📋</button>
                            <button class="btn-icon" title="Edit">✏️</button>
                            <button class="btn-icon" title="Delete">🗑️</button>
                        </div>
                    </div>
                    
                    <p class="card-preview">${escapeHtml(
                        (prompt.content || '').substring(0, 100)
                    )}...</p>
                    
                    ${prompt.tags && prompt.tags.length > 0 ? `
                        <div class="card-tags">
                            ${prompt.tags.map(tag => 
                                `<span class="tag">#${escapeHtml(tag)}</span>`
                            ).join('')}
                        </div>
                    ` : ''}
                    
                    <div class="card-footer">
                        <span class="category-badge">${escapeHtml(prompt.category || 'custom')}</span>
                        <span class="uses-count">Used: ${prompt.uses || 0}</span>
                    </div>
                </div>
            `)
            .join('');
        
        // Setup event listeners
        document.querySelectorAll('.prompt-card').forEach(card => {
            card.querySelector('.btn-icon[title="Copy"]').addEventListener('click', async (e) => {
                e.preventDefault();
                const id = card.dataset.id;
                const prompt = allPrompts.find(p => p.id == id);
                if (prompt) {
                    navigator.clipboard.writeText(prompt.content || '').then(() => {
                        showToast('Copied to clipboard!');
                    });
                }
            });
            
            card.querySelector('.btn-icon[title="Edit"]').addEventListener('click', (e) => {
                e.preventDefault();
                const id = card.dataset.id;
                if (window.router) {
                    window.appState.set('editingPromptId', id);
                    window.router.navigate('/editor');
                }
            });
            
            card.querySelector('.btn-icon[title="Delete"]').addEventListener('click', async (e) => {
                e.preventDefault();
                const id = card.dataset.id;
                if (confirm('Delete this prompt?')) {
                    try {
                        await window.http.delete(`/api/prompts/${id}`);
                        loadPrompts();
                        showToast('Prompt deleted');
                    } catch (err) {
                        console.error('Delete failed:', err);
                    }
                }
            });
        });
        
        // Update pagination
        if (totalPages > 1) {
            pagination.style.display = 'flex';
            pagination.innerHTML = `
                <button class="btn-pagination" ${currentPage === 1 ? 'disabled' : ''} id="prev-page">← Prev</button>
                <div class="page-info">Page ${currentPage} of ${totalPages}</div>
                <button class="btn-pagination" ${currentPage === totalPages ? 'disabled' : ''} id="next-page">Next →</button>
            `;
            
            document.getElementById('prev-page').addEventListener('click', () => {
                if (currentPage > 1) {
                    currentPage--;
                    renderPrompts();
                }
            });
            
            document.getElementById('next-page').addEventListener('click', () => {
                if (currentPage < totalPages) {
                    currentPage++;
                    renderPrompts();
                }
            });
        } else {
            pagination.style.display = 'none';
        }
    }
    
    // ==================== EVENT LISTENERS ====================
    
    document.getElementById('prompts-search').addEventListener('input', (e) => {
        searchQuery = e.target.value;
        currentPage = 1;
        renderPrompts();
    });
    
    document.getElementById('prompts-category').addEventListener('change', (e) => {
        filterCategory = e.target.value;
        currentPage = 1;
        renderPrompts();
    });
    
    document.getElementById('prompts-sort').addEventListener('change', (e) => {
        sortBy = e.target.value;
        currentPage = 1;
        renderPrompts();
    });
    
    document.getElementById('btn-new-prompt').addEventListener('click', () => {
        if (window.router) {
            window.appState.set('editingPromptId', null);
            window.router.navigate('/editor');
        }
    });
    
    // ==================== INITIAL LOAD ====================
    loadPrompts();
    
    return container;
}

/**
 * Utility: Escape HTML special characters
 */
function escapeHtml(text) {
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
 * Utility: Show toast notification
 */
function showToast(message) {
    const toast = document.createElement('div');
    toast.className = 'toast-notification';
    toast.textContent = message;
    document.body.appendChild(toast);
    
    setTimeout(() => {
        toast.style.opacity = '0';
        setTimeout(() => toast.remove(), 300);
    }, 2000);
}

/**
 * ProjectsView.js - Projects Management View
 * 
 * Features:
 * - Grid/List view toggle
 * - Create, edit, delete projects
 * - Prompt linking to projects
 * - Progress tracking
 * - Project statistics
 * - Status indicators
 */

export default function createProjectsView() {
    const container = document.createElement('div');
    container.className = 'projects-view';
    
    // ==================== HEADER ====================
    const header = document.createElement('div');
    header.className = 'view-header';
    header.innerHTML = `
        <div class="header-content">
            <h1 class="view-title">📁 Projects</h1>
            <p class="view-subtitle">Organize and manage your prompt projects</p>
        </div>
    `;
    container.appendChild(header);
    
    // ==================== CONTROLS ====================
    const controls = document.createElement('div');
    controls.className = 'projects-controls';
    controls.innerHTML = `
        <div class="search-box">
            <input 
                type="text" 
                id="projects-search" 
                placeholder="Search projects..."
                class="search-input"
            />
            <span class="search-icon">🔍</span>
        </div>
        <div class="view-toggles">
            <button id="toggle-grid" class="toggle-btn active" title="Grid view">
                ⊞ Grid
            </button>
            <button id="toggle-list" class="toggle-btn" title="List view">
                ☰ List
            </button>
        </div>
        <button id="btn-new-project" class="btn btn-primary">+ New Project</button>
    `;
    container.appendChild(controls);
    
    // ==================== PROJECTS CONTAINER ====================
    const projectsContainer = document.createElement('div');
    projectsContainer.className = 'projects-container grid-view';
    projectsContainer.id = 'projects-container';
    projectsContainer.innerHTML = '<div class="loading">Loading projects...</div>';
    container.appendChild(projectsContainer);
    
    // ==================== EMPTY STATE ====================
    const emptyState = document.createElement('div');
    emptyState.className = 'empty-state';
    emptyState.innerHTML = `
        <div class="empty-state-icon">📂</div>
        <h3>No projects yet</h3>
        <p>Create your first project to start organizing prompts</p>
    `;
    emptyState.style.display = 'none';
    container.appendChild(emptyState);
    
    // ==================== DATA STATE ====================
    let allProjects = [];
    let viewMode = 'grid'; // grid or list
    let searchQuery = '';
    
    // ==================== FUNCTIONS ====================
    
    /**
     * Fetch projects from API
     */
    async function loadProjects() {
        try {
            if (!window.http) {
                throw new Error('HTTP client not available');
            }
            
            const response = await window.http.get('/api/projects');
            allProjects = response.data || response.projects || [];
            
            if (!Array.isArray(allProjects)) {
                allProjects = [];
            }
            
            renderProjects();
            
        } catch (error) {
            console.error('Failed to load projects:', error);
            projectsContainer.innerHTML = `
                <div class="error-message">
                    <p>Failed to load projects</p>
                    <small>${error.message}</small>
                </div>
            `;
        }
    }
    
    /**
     * Filter projects by search query
     */
    function getFilteredProjects() {
        if (!searchQuery) return allProjects;
        
        return allProjects.filter(project => 
            project.name?.toLowerCase().includes(searchQuery.toLowerCase()) ||
            project.description?.toLowerCase().includes(searchQuery.toLowerCase())
        );
    }
    
    /**
     * Render projects
     */
    function renderProjects() {
        const filtered = getFilteredProjects();
        
        if (filtered.length === 0) {
            projectsContainer.innerHTML = '';
            emptyState.style.display = 'flex';
            return;
        }
        
        emptyState.style.display = 'none';
        
        const cards = filtered.map(project => {
            const progress = project.progress || 0;
            const promptCount = project.prompt_count || 0;
            const status = project.status || 'active';
            
            return `
                <div class="project-card ${viewMode === 'list' ? 'list-item' : ''}" data-id="${project.id}">
                    <div class="project-header">
                        <div class="project-info">
                            <h3 class="project-name">${escapeHtml(project.name || 'Untitled')}</h3>
                            <span class="status-badge ${status}">${status}</span>
                        </div>
                        <div class="project-actions">
                            <button class="btn-icon" title="Edit">✏️</button>
                            <button class="btn-icon" title="Delete">🗑️</button>
                        </div>
                    </div>
                    
                    ${project.description ? `
                        <p class="project-description">${escapeHtml(project.description)}</p>
                    ` : ''}
                    
                    <div class="project-progress">
                        <div class="progress-bar">
                            <div class="progress-fill" style="width: ${progress}%"></div>
                        </div>
                        <span class="progress-text">${progress}%</span>
                    </div>
                    
                    <div class="project-stats">
                        <div class="stat">
                            <span class="stat-label">Prompts</span>
                            <span class="stat-value">${promptCount}</span>
                        </div>
                        <div class="stat">
                            <span class="stat-label">Created</span>
                            <span class="stat-value">${formatDate(project.created_at)}</span>
                        </div>
                        <div class="stat">
                            <span class="stat-label">Updated</span>
                            <span class="stat-value">${formatDate(project.updated_at)}</span>
                        </div>
                    </div>
                    
                    <div class="project-footer">
                        <button class="btn btn-small btn-primary" data-action="open">Open</button>
                        <button class="btn btn-small" data-action="edit">Edit</button>
                    </div>
                </div>
            `;
        }).join('');
        
        projectsContainer.innerHTML = cards;
        
        // Setup event listeners with null checks
        document.querySelectorAll('.project-card').forEach(card => {
            const id = card.dataset.id;
            
            const editBtn = card.querySelector('.btn-icon[title="Edit"]');
            if (editBtn) {
                editBtn.addEventListener('click', () => {
                    editProject(id);
                });
            }
            
            const deleteBtn = card.querySelector('.btn-icon[title="Delete"]');
            if (deleteBtn) {
                deleteBtn.addEventListener('click', () => {
                    deleteProject(id);
                });
            }
            
            const openBtn = card.querySelector('[data-action="open"]');
            if (openBtn) {
                openBtn.addEventListener('click', () => {
                    openProject(id);
                });
            }
            
            const editCardBtn = card.querySelector('[data-action="edit"]');
            if (editCardBtn) {
                editCardBtn.addEventListener('click', () => {
                    editProject(id);
                });
            }
        });
    }
    
    /**
     * Edit project
     */
    function editProject(id) {
        if (window.appState) {
            window.appState.set('editingProjectId', id);
        }
        console.log('Edit project:', id);
    }
    
    /**
     * Delete project
     */
    async function deleteProject(id) {
        if (!confirm('Delete this project? This cannot be undone.')) return;
        
        try {
            await window.http.delete(`/api/projects/${id}`);
            loadProjects();
            showToast('Project deleted');
        } catch (error) {
            console.error('Delete failed:', error);
            showToast('Failed to delete project');
        }
    }
    
    /**
     * Open project
     */
    function openProject(id) {
        if (window.appState) {
            window.appState.set('selectedProjectId', id);
        }
        console.log('Open project:', id);
    }
    
    // ==================== EVENT LISTENERS ====================
    
    document.getElementById('projects-search').addEventListener('input', (e) => {
        searchQuery = e.target.value;
        renderProjects();
    });
    
    document.getElementById('toggle-grid').addEventListener('click', () => {
        viewMode = 'grid';
        projectsContainer.className = 'projects-container grid-view';
        document.getElementById('toggle-grid').classList.add('active');
        document.getElementById('toggle-list').classList.remove('active');
        renderProjects();
    });
    
    document.getElementById('toggle-list').addEventListener('click', () => {
        viewMode = 'list';
        projectsContainer.className = 'projects-container list-view';
        document.getElementById('toggle-list').classList.add('active');
        document.getElementById('toggle-grid').classList.remove('active');
        renderProjects();
    });
    
    document.getElementById('btn-new-project').addEventListener('click', () => {
        if (window.appState) {
            window.appState.set('editingProjectId', null);
        }
        console.log('Create new project');
    });
    
    // ==================== INITIAL LOAD ====================
    loadProjects();
    
    return container;
}

/**
 * Utility: Escape HTML
 */
function escapeHtml(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return (text || '').replace(/[&<>"']/g, m => map[m]);
}

/**
 * Utility: Format date
 */
function formatDate(dateStr) {
    if (!dateStr) return '-';
    const date = new Date(dateStr);
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    });
}

/**
 * Utility: Show toast
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

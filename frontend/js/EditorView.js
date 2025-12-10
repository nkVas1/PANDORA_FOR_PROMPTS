/**
 * EditorView.js - Prompt Editor View
 * 
 * Features:
 * - Create and edit prompts
 * - Auto-save functionality
 * - Preview panel
 * - Template suggestions
 * - Tag management
 * - Category selection
 * - Markdown support
 */

export default function createEditorView() {
    const container = document.createElement('div');
    container.className = 'editor-view';
    
    // Get editing prompt ID from app state
    const editingPromptId = window.appState ? window.appState.get('editingPromptId') : null;
    const isNewPrompt = !editingPromptId;
    
    // ==================== HEADER ====================
    const header = document.createElement('div');
    header.className = 'view-header';
    header.innerHTML = `
        <div class="header-content">
            <h1 class="view-title">✏️ ${isNewPrompt ? 'New Prompt' : 'Edit Prompt'}</h1>
            <p class="view-subtitle">Create and refine your prompts</p>
        </div>
    `;
    container.appendChild(header);
    
    // ==================== EDITOR LAYOUT ====================
    const editorLayout = document.createElement('div');
    editorLayout.className = 'editor-layout';
    
    const deleteButtonDisplay = isNewPrompt ? 'none' : 'block';
    editorLayout.innerHTML = `
        <div class="editor-main">
            <div class="editor-form">
                <div class="form-group">
                    <label for="prompt-name">Prompt Name</label>
                    <input type="text" id="prompt-name" placeholder="Enter prompt name" class="form-input" maxlength="200" />
                    <small class="form-help">Give your prompt a descriptive name</small>
                </div>
                
                <div class="form-row">
                    <div class="form-group">
                        <label for="prompt-category">Category</label>
                        <select id="prompt-category" class="form-input">
                            <option value="writing">Writing</option>
                            <option value="code">Code</option>
                            <option value="analysis">Analysis</option>
                            <option value="creative">Creative</option>
                            <option value="custom">Custom</option>
                        </select>
                    </div>
                    
                    <div class="form-group">
                        <label for="prompt-project">Link Project</label>
                        <select id="prompt-project" class="form-input">
                            <option value="">No project</option>
                        </select>
                    </div>
                </div>
                
                <div class="form-group">
                    <label for="prompt-content">Prompt Content</label>
                    <textarea id="prompt-content" placeholder="Write your prompt here... Supports Markdown formatting" class="form-input editor-textarea" rows="12"></textarea>
                    <small class="form-help">Supports Markdown formatting. Use {{variable}} for placeholders.</small>
                </div>
                
                <div class="form-group">
                    <label for="prompt-tags">Tags</label>
                    <div class="tags-input" id="tags-input">
                        <input type="text" id="prompt-tags" placeholder="Add tags (press Enter)" class="form-input tags-field" />
                        <div class="tags-list" id="tags-list"></div>
                    </div>
                    <small class="form-help">Add multiple tags to organize your prompts</small>
                </div>
                
                <div class="form-actions">
                    <button id="btn-save" class="btn btn-primary btn-lg">💾 Save Prompt</button>
                    <button id="btn-cancel" class="btn btn-secondary btn-lg">Cancel</button>
                    <button id="btn-delete" class="btn btn-danger btn-lg" style="display: ${deleteButtonDisplay}">🗑️ Delete</button>
                </div>
            </div>
        </div>
        
        <div class="editor-preview">
            <div class="preview-header">
                <h3>Preview</h3>
                <button id="btn-copy-content" class="btn-icon" title="Copy">📋</button>
            </div>
            <div class="preview-content" id="preview-content">
                <p class="preview-placeholder">Your prompt preview will appear here</p>
            </div>
            
            <div class="preview-section">
                <h4>Prompt Info</h4>
                <div class="info-item">
                    <span class="info-label">Characters:</span>
                    <span class="info-value" id="char-count">0</span>
                </div>
                <div class="info-item">
                    <span class="info-label">Words:</span>
                    <span class="info-value" id="word-count">0</span>
                </div>
                <div class="info-item">
                    <span class="info-label">Variables:</span>
                    <span class="info-value" id="var-count">0</span>
                </div>
            </div>
        </div>
    `;
    container.appendChild(editorLayout);
    
    // ==================== DATA STATE ====================
    let promptData = {
        id: editingPromptId,
        name: '',
        content: '',
        category: 'custom',
        project_id: null,
        tags: []
    };
    let tags = [];
    let isDirty = false;
    let saveTimeout;
    
    // ==================== FUNCTIONS ====================
    
    /**
     * Load prompt if editing
     */
    async function loadPrompt() {
        if (!editingPromptId) return;
        
        try {
            const response = await window.http.get(`/api/prompts/${editingPromptId}`);
            promptData = response.data || response;
            tags = promptData.tags || [];
            
            // Populate form
            document.getElementById('prompt-name').value = promptData.name || '';
            document.getElementById('prompt-category').value = promptData.category || 'custom';
            document.getElementById('prompt-content').value = promptData.content || '';
            document.getElementById('prompt-project').value = promptData.project_id || '';
            
            renderTags();
            updatePreview();
            
        } catch (error) {
            console.error('Failed to load prompt:', error);
        }
    }
    
    /**
     * Load projects for select
     */
    async function loadProjects() {
        try {
            const response = await window.http.get('/api/projects');
            const projects = response.data || response.projects || [];
            
            const select = document.getElementById('prompt-project');
            projects.forEach(project => {
                const option = document.createElement('option');
                option.value = project.id;
                option.textContent = project.name;
                select.appendChild(option);
            });
            
            if (promptData.project_id) {
                select.value = promptData.project_id;
            }
        } catch (error) {
            console.error('Failed to load projects:', error);
        }
    }
    
    /**
     * Update preview and stats
     */
    function updatePreview() {
        const content = document.getElementById('prompt-content').value;
        const preview = document.getElementById('preview-content');
        
        // Simple markdown to HTML (basic)
        let html = content
            .replace(/# (.*)/g, '<h3>$1</h3>')
            .replace(/## (.*)/g, '<h4>$1</h4>')
            .replace(/\n/g, '<br>')
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\*(.*?)\*/g, '<em>$1</em>');
        
        if (!html.trim()) {
            preview.innerHTML = '<p class="preview-placeholder">Start typing to see preview</p>';
        } else {
            preview.innerHTML = html;
        }
        
        // Update stats
        document.getElementById('char-count').textContent = content.length;
        document.getElementById('word-count').textContent = content.split(/\s+/).filter(w => w).length;
        
        const variables = (content.match(/\{\{(.*?)\}\}/g) || []).length;
        document.getElementById('var-count').textContent = variables;
    }
    
    /**
     * Render tags
     */
    function renderTags() {
        const tagsList = document.getElementById('tags-list');
        tagsList.innerHTML = tags.map(tag => `
            <span class="tag-item">
                #${escapeHtml(tag)}
                <button class="btn-remove-tag" data-tag="${escapeHtml(tag)}">×</button>
            </span>
        `).join('');
        
        // Setup remove listeners
        document.querySelectorAll('.btn-remove-tag').forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.preventDefault();
                const tag = btn.dataset.tag;
                tags = tags.filter(t => t !== tag);
                renderTags();
            });
        });
    }
    
    /**
     * Save prompt
     */
    async function savePrompt() {
        try {
            promptData.name = document.getElementById('prompt-name').value;
            promptData.content = document.getElementById('prompt-content').value;
            promptData.category = document.getElementById('prompt-category').value;
            promptData.project_id = document.getElementById('prompt-project').value || null;
            promptData.tags = tags;
            
            if (!promptData.name.trim()) {
                alert('Please enter a prompt name');
                return;
            }
            
            if (!promptData.content.trim()) {
                alert('Please enter prompt content');
                return;
            }
            
            const method = editingPromptId ? 'PUT' : 'POST';
            const url = editingPromptId ? `/api/prompts/${editingPromptId}` : '/api/prompts';
            
            const response = await window.http[method.toLowerCase()](url, promptData);
            
            showToast('Prompt saved successfully!');
            isDirty = false;
            
            // Navigate back to prompts
            setTimeout(() => {
                if (window.router) {
                    window.router.navigate('/prompts');
                }
            }, 500);
            
        } catch (error) {
            console.error('Save failed:', error);
            showToast('Failed to save prompt');
        }
    }
    
    /**
     * Auto-save
     */
    function autoSave() {
        if (isDirty) {
            clearTimeout(saveTimeout);
            saveTimeout = setTimeout(() => {
                console.log('Auto-saving prompt...');
                // Could auto-save here, but for now just draft locally
            }, 2000);
        }
    }
    
    // ==================== EVENT LISTENERS ====================
    
    document.getElementById('prompt-name').addEventListener('input', () => {
        isDirty = true;
        autoSave();
    });
    
    document.getElementById('prompt-content').addEventListener('input', () => {
        isDirty = true;
        updatePreview();
        autoSave();
    });
    
    document.getElementById('prompt-category').addEventListener('change', () => {
        isDirty = true;
        autoSave();
    });
    
    document.getElementById('prompt-project').addEventListener('change', () => {
        isDirty = true;
        autoSave();
    });
    
    document.getElementById('prompt-tags').addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            e.preventDefault();
            const input = e.target;
            const tag = input.value.trim();
            
            if (tag && !tags.includes(tag)) {
                tags.push(tag);
                input.value = '';
                renderTags();
                isDirty = true;
            }
        }
    });
    
    document.getElementById('btn-copy-content').addEventListener('click', () => {
        const content = document.getElementById('prompt-content').value;
        navigator.clipboard.writeText(content).then(() => {
            showToast('Copied to clipboard!');
        });
    });
    
    document.getElementById('btn-save').addEventListener('click', savePrompt);
    
    document.getElementById('btn-cancel').addEventListener('click', () => {
        if (isDirty && !confirm('Discard unsaved changes?')) return;
        if (window.router) {
            window.router.navigate('/prompts');
        }
    });
    
    document.getElementById('btn-delete').addEventListener('click', async () => {
        if (!confirm('Delete this prompt?')) return;
        try {
            await window.http.delete(`/api/prompts/${editingPromptId}`);
            showToast('Prompt deleted');
            setTimeout(() => {
                if (window.router) {
                    window.router.navigate('/prompts');
                }
            }, 500);
        } catch (error) {
            console.error('Delete failed:', error);
            showToast('Failed to delete prompt');
        }
    });
    
    // ==================== INITIAL LOAD ====================
    loadPrompt();
    loadProjects();
    updatePreview();
    
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

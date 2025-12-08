// Модальные окна для PANDORA

const API_URL = 'http://127.0.0.1:8000';

// ======= МОДАЛЬНОЕ ОКНО РЕДАКТОРА ПРОМПТА =======
function openPromptEditor(promptId) {
    fetch(`${API_URL}/api/prompts/${promptId}`)
        .then(r => r.json())
        .then(prompt => {
            const modal = document.createElement('div');
            modal.className = 'modal-overlay';
            modal.innerHTML = `
                <div class="modal-content modal-large">
                    <div class="modal-header">
                        <h2>${prompt.title}</h2>
                        <button class="modal-close" onclick="this.closest('.modal-overlay').remove()">&times;</button>
                    </div>
                    <div class="modal-body">
                        <div class="editor-container">
                            <div class="editor-sidebar">
                                <div class="info-section">
                                    <label>📁 Категория</label>
                                    <p class="info-value">${prompt.category}</p>
                                </div>
                                <div class="info-section">
                                    <label>🏷️ Теги (${prompt.tags.length})</label>
                                    <div class="tags-list">
                                        ${prompt.tags.map(t => `<span class="tag-chip">${t.name}</span>`).join('')}
                                    </div>
                                </div>
                                <div class="info-section">
                                    <label>📊 Статистика</label>
                                    <p class="info-value">👁️ ${prompt.usage_count || 0} просмотров</p>
                                    <p class="info-value">📅 ${new Date(prompt.created_at).toLocaleDateString('ru-RU')}</p>
                                </div>
                                <div class="button-group">
                                    <button class="btn btn-primary btn-sm" onclick="copyPromptToClipboard('${prompt.id}')">📋 Скопировать</button>
                                    <button class="btn btn-secondary btn-sm" onclick="editPromptInline('${prompt.id}')">✏️ Редактировать</button>
                                </div>
                            </div>
                            <div class="editor-main">
                                <div id="prompt-content-${prompt.id}" class="prompt-content">
                                    <pre>${escapeHtml(prompt.content)}</pre>
                                </div>
                                <textarea id="prompt-edit-${prompt.id}" class="prompt-textarea" style="display:none;">${prompt.content}</textarea>
                            </div>
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button class="btn btn-secondary" onclick="this.closest('.modal-overlay').remove()">Закрыть</button>
                    </div>
                </div>
            `;
            document.body.appendChild(modal);
        })
        .catch(e => alert('Ошибка загрузки: ' + e));
}

function copyPromptToClipboard(promptId) {
    const content = document.querySelector(`#prompt-content-${promptId} pre`)?.textContent;
    if (content) {
        navigator.clipboard.writeText(content).then(() => {
            alert('✅ Скопировано в буфер обмена');
        });
    }
}

function editPromptInline(promptId) {
    const contentDiv = document.querySelector(`#prompt-content-${promptId}`);
    const textarea = document.querySelector(`#prompt-edit-${promptId}`);
    
    if (contentDiv.style.display === 'none') {
        // Сохранить
        const newContent = textarea.value;
        fetch(`${API_URL}/api/prompts/${promptId}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ content: newContent })
        }).then(r => {
            if (r.ok) {
                contentDiv.innerHTML = `<pre>${escapeHtml(newContent)}</pre>`;
                contentDiv.style.display = 'block';
                textarea.style.display = 'none';
                alert('✅ Сохранено');
            }
        });
    } else {
        // Включить редактирование
        contentDiv.style.display = 'none';
        textarea.style.display = 'block';
        textarea.focus();
    }
}

// ======= МОДАЛЬНОЕ ОКНО УПРАВЛЕНИЯ ПРОЕКТОМ =======
function openProjectManager(projectId) {
    fetch(`${API_URL}/api/projects/${projectId}`)
        .then(r => r.json())
        .then(project => {
            const modal = document.createElement('div');
            modal.className = 'modal-overlay';
            modal.innerHTML = `
                <div class="modal-content modal-large">
                    <div class="modal-header">
                        <h2>📊 ${project.name}</h2>
                        <button class="modal-close" onclick="this.closest('.modal-overlay').remove()">&times;</button>
                    </div>
                    <div class="modal-body">
                        <div class="project-manager">
                            <div class="project-info-panel">
                                <h3>Информация проекта</h3>
                                <p class="info-label">Описание:</p>
                                <p>${project.description || 'Нет описания'}</p>
                                <p class="info-label">Статус:</p>
                                <select class="form-input" onchange="updateProjectStatus('${project.id}', this.value)">
                                    <option value="active" ${project.status === 'active' ? 'selected' : ''}>🟢 Активный</option>
                                    <option value="paused" ${project.status === 'paused' ? 'selected' : ''}>🟡 На паузе</option>
                                    <option value="completed" ${project.status === 'completed' ? 'selected' : ''}>🟣 Завершён</option>
                                </select>
                            </div>
                            
                            <div class="project-tasks-panel">
                                <h3>Задачи проекта</h3>
                                <div id="tasks-list-${project.id}" class="tasks-list">
                                    <p style="color: var(--dark-400);">Загрузка задач...</p>
                                </div>
                                <div class="button-group">
                                    <button class="btn btn-primary btn-sm" onclick="addProjectTask('${project.id}')">➕ Добавить задачу</button>
                                </div>
                            </div>
                            
                            <div class="project-stats-panel">
                                <h3>Статистика</h3>
                                <div class="stat-grid">
                                    <div class="stat-box">
                                        <span class="stat-number">0</span>
                                        <span class="stat-label">Задач</span>
                                    </div>
                                    <div class="stat-box">
                                        <span class="stat-number">0</span>
                                        <span class="stat-label">Выполнено</span>
                                    </div>
                                    <div class="stat-box">
                                        <span class="stat-number">0%</span>
                                        <span class="stat-label">Прогресс</span>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button class="btn btn-secondary" onclick="this.closest('.modal-overlay').remove()">Закрыть</button>
                    </div>
                </div>
            `;
            document.body.appendChild(modal);
            loadProjectTasks(projectId);
        })
        .catch(e => alert('Ошибка загрузки: ' + e));
}

function loadProjectTasks(projectId) {
    fetch(`${API_URL}/api/projects/${projectId}/tasks`)
        .then(r => r.json())
        .then(tasks => {
            const container = document.querySelector(`#tasks-list-${projectId}`);
            if (tasks.length === 0) {
                container.innerHTML = '<p style="color: var(--dark-400); text-align: center;">Задач нет. Добавьте первую!</p>';
            } else {
                container.innerHTML = tasks.map(task => `
                    <div class="task-item">
                        <input type="checkbox" ${task.completed ? 'checked' : ''} onchange="toggleTask('${task.id}')">
                        <span>${task.title}</span>
                        <button class="btn-small" onclick="deleteTask('${task.id}')">🗑️</button>
                    </div>
                `).join('');
            }
        });
}

function addProjectTask(projectId) {
    const title = prompt('Введите название задачи:');
    if (!title) return;
    
    fetch(`${API_URL}/api/projects/${projectId}/tasks`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title, description: '' })
    }).then(r => {
        if (r.ok) {
            loadProjectTasks(projectId);
        }
    });
}

// ======= МОДАЛЬНОЕ ОКНО ВЫБОРА ТЕГОВ =======
function openTagsModal(onSelect) {
    fetch(`${API_URL}/api/tags`)
        .then(r => r.json())
        .then(tags => {
            // Группировать теги по категориям
            const tagsByCategory = {};
            
            fetch(`${API_URL}/api/prompts`)
                .then(r => r.json())
                .then(prompts => {
                    prompts.forEach(p => {
                        if (!tagsByCategory[p.category]) {
                            tagsByCategory[p.category] = [];
                        }
                        p.tags.forEach(t => {
                            if (!tagsByCategory[p.category].find(tag => tag.id === t.id)) {
                                tagsByCategory[p.category].push(t);
                            }
                        });
                    });
                    
                    const modal = document.createElement('div');
                    modal.className = 'modal-overlay';
                    modal.innerHTML = `
                        <div class="modal-content modal-large">
                            <div class="modal-header">
                                <h2>🏷️ Тегов по категориям</h2>
                                <button class="modal-close" onclick="this.closest('.modal-overlay').remove()">&times;</button>
                            </div>
                            <div class="modal-body">
                                <div class="tags-categories">
                                    ${Object.entries(tagsByCategory).map(([category, categoryTags]) => `
                                        <div class="category-section">
                                            <h3>${category}</h3>
                                            <div class="tags-cloud">
                                                ${categoryTags.map(t => `
                                                    <button class="tag-button" onclick="selectTag('${t.id}', '${t.name}')">${t.name}</button>
                                                `).join('')}
                                            </div>
                                        </div>
                                    `).join('')}
                                </div>
                            </div>
                            <div class="modal-footer">
                                <button class="btn btn-secondary" onclick="this.closest('.modal-overlay').remove()">Закрыть</button>
                            </div>
                        </div>
                    `;
                    document.body.appendChild(modal);
                });
        });
}

// ======= УТИЛИТЫ =======
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

function updateProjectStatus(projectId, status) {
    fetch(`${API_URL}/api/projects/${projectId}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ status })
    }).then(r => {
        if (r.ok) alert('✅ Статус обновлен');
    });
}

function toggleTask(taskId) {
    // TODO: реализовать API
}

function deleteTask(taskId) {
    if (confirm('Удалить задачу?')) {
        // TODO: реализовать API
    }
}

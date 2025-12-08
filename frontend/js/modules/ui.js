// UI Module - Отрисовка интерфейса
class UIModule {
    constructor() {
        this.container = document.getElementById('app-container');
    }

    // Отрисовать страницу Dashboard
    async renderDashboard() {
        const stats = STATE.state.stats;

        this.container.innerHTML = `
            <div class="page dashboard-page">
                <div class="page-header">
                    <h1>🚀 PANDORA Prompts Manager</h1>
                    <p class="subtitle">Профессиональный инструмент для работы с промптами и проектами</p>
                </div>

                <div class="stats-grid">
                    <div class="stat-card">
                        <div class="stat-icon">📝</div>
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
                </div>

                <div class="features-section">
                    <h2>✨ Возможности</h2>
                    <div class="features-grid">
                        <div class="feature-card">
                            <div class="feature-icon">💾</div>
                            <h3>Управление промптами</h3>
                            <p>Сохраняйте, редактируйте и организуйте все ваши промпты</p>
                        </div>

                        <div class="feature-card">
                            <div class="feature-icon">🤖</div>
                            <h3>Автотегирование</h3>
                            <p>Автоматическое распределение по категориям и генерация тегов</p>
                        </div>

                        <div class="feature-card">
                            <div class="feature-icon">🔍</div>
                            <h3>Умный поиск</h3>
                            <p>Быстро находите промпты по названию, тегам и содержимому</p>
                        </div>

                        <div class="feature-card">
                            <div class="feature-icon">📁</div>
                            <h3>Управление проектами</h3>
                            <p>Ведите задачи и процесс разработки каждого проекта</p>
                        </div>

                        <div class="feature-card">
                            <div class="feature-icon">📤</div>
                            <h3>Экспорт данных</h3>
                            <p>Экспортируйте промпты в TXT, JSON и другие форматы</p>
                        </div>

                        <div class="feature-card">
                            <div class="feature-icon">🔌</div>
                            <h3>Плагины и расширения</h3>
                            <p>Расширяйте функционал через систему плагинов</p>
                        </div>
                    </div>
                </div>

                <div class="quick-actions">
                    <h2>⚡ Быстрые действия</h2>
                    <button class="btn btn-large btn-primary" onclick="UI.renderPromptsPage()">
                        ➕ Добавить промпт
                    </button>
                    <button class="btn btn-large btn-primary" onclick="UI.renderProjectsPage()">
                        ➕ Создать проект
                    </button>
                </div>
            </div>
        `;
    }

    // Отрисовать страницу Промптов
    async renderPromptsPage() {
        const prompts = STATE.state.prompts;
        const categories = STATE.state.categories || [];

        this.container.innerHTML = `
            <div class="page prompts-page">
                <div class="page-header">
                    <h1>📝 Мои промпты</h1>
                    <button class="btn btn-primary" onclick="UI.showCreatePromptForm()">➕ Добавить новый</button>
                </div>

                <div class="filters-section">
                    <input type="text" class="filter-input" placeholder="🔍 Поиск промптов..." 
                           onkeyup="UI.filterPrompts(this.value)">
                    
                    <div class="category-filter">
                        <button class="filter-btn ${!STATE.state.selectedCategory ? 'active' : ''}" 
                                onclick="UI.filterByCategory(null)">
                            Все
                        </button>
                        ${categories.map(cat => `
                            <button class="filter-btn ${STATE.state.selectedCategory === cat ? 'active' : ''}" 
                                    onclick="UI.filterByCategory('${cat}')">
                                ${cat}
                            </button>
                        `).join('')}
                    </div>
                </div>

                <div class="prompts-grid" id="promptsContainer">
                    ${prompts.length === 0 ? `
                        <div class="empty-state">
                            <div class="empty-icon">📭</div>
                            <h3>Промптов не найдено</h3>
                            <p>Добавьте первый промпт, чтобы начать</p>
                            <button class="btn btn-primary" onclick="UI.showCreatePromptForm()">
                                ➕ Создать промпт
                            </button>
                        </div>
                    ` : prompts.map(prompt => `
                        <div class="prompt-card" onclick="MODAL.openPromptModal(${prompt.id})">
                            <div class="card-header">
                                <h3>${this.escapeHtml(prompt.title)}</h3>
                                <span class="category-badge">${prompt.category}</span>
                            </div>
                            <p class="card-description">${this.escapeHtml((prompt.description || '').substring(0, 100))}...</p>
                            <div class="card-footer">
                                <div class="card-meta">
                                    <span class="meta-item">🏷️ ${prompt.tags?.length || 0}</span>
                                    <span class="meta-item">👁️ ${prompt.usage_count || 0}</span>
                                </div>
                                <div class="card-actions">
                                    <button class="btn-icon" onclick="event.stopPropagation(); MODAL.copyPromptContent(${prompt.id})" title="Копировать">📋</button>
                                    <button class="btn-icon" onclick="event.stopPropagation(); UI.deletePrompt(${prompt.id})" title="Удалить">🗑️</button>
                                </div>
                            </div>
                        </div>
                    `).join('')}
                </div>
            </div>
        `;
    }

    // Отрисовать страницу Проектов
    async renderProjectsPage() {
        const projects = STATE.state.projects;

        this.container.innerHTML = `
            <div class="page projects-page">
                <div class="page-header">
                    <h1>📁 Мои проекты</h1>
                    <button class="btn btn-primary" onclick="UI.showCreateProjectForm()">➕ Создать новый</button>
                </div>

                <div class="projects-grid" id="projectsContainer">
                    ${projects.length === 0 ? `
                        <div class="empty-state">
                            <div class="empty-icon">📭</div>
                            <h3>Проектов не найдено</h3>
                            <p>Создайте первый проект для начала работы</p>
                            <button class="btn btn-primary" onclick="UI.showCreateProjectForm()">
                                ➕ Создать проект
                            </button>
                        </div>
                    ` : projects.map(project => `
                        <div class="project-card" onclick="MODAL.openProjectModal(${project.id})">
                            <div class="card-header">
                                <h3>📁 ${this.escapeHtml(project.name)}</h3>
                                <span class="status-badge status-${project.status}">${project.status}</span>
                            </div>
                            <p class="card-description">${this.escapeHtml((project.description || '').substring(0, 100))}...</p>
                            <div class="card-footer">
                                <div class="card-meta">
                                    <span class="meta-item">📅 ${new Date(project.created_at).toLocaleDateString('ru-RU')}</span>
                                </div>
                                <div class="card-actions">
                                    <button class="btn-icon" onclick="event.stopPropagation(); UI.deleteProject(${project.id})" title="Удалить">🗑️</button>
                                </div>
                            </div>
                        </div>
                    `).join('')}
                </div>
            </div>
        `;
    }

    // Показать форму создания промпта
    showCreatePromptForm() {
        const modal = document.createElement('div');
        modal.className = 'modal-overlay';
        modal.innerHTML = `
            <div class="modal">
                <div class="modal-header">
                    <h2>➕ Новый промпт</h2>
                    <button class="btn-icon close" onclick="this.closest('.modal-overlay').remove()">✕</button>
                </div>

                <form id="createPromptForm" class="form-large">
                    <div class="form-group">
                        <label>Название *</label>
                        <input type="text" class="form-input" id="newPromptTitle" required>
                    </div>

                    <div class="form-group">
                        <label>Содержание *</label>
                        <textarea class="form-input form-textarea-large" id="newPromptContent" required></textarea>
                    </div>

                    <div class="form-group">
                        <label>Описание</label>
                        <textarea class="form-input" id="newPromptDescription"></textarea>
                    </div>

                    <div class="form-group">
                        <label>Категория</label>
                        <select class="form-input" id="newPromptCategory">
                            <option value="development">Development</option>
                            <option value="writing">Writing</option>
                            <option value="analysis">Analysis</option>
                            <option value="business">Business</option>
                            <option value="creative">Creative</option>
                        </select>
                    </div>

                    <div class="form-actions">
                        <button type="submit" class="btn btn-primary">✅ Создать</button>
                        <button type="button" class="btn btn-secondary" onclick="this.closest('.modal-overlay').remove()">Отмена</button>
                    </div>
                </form>
            </div>
        `;

        document.body.appendChild(modal);

        document.getElementById('createPromptForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            const title = document.getElementById('newPromptTitle').value;
            const content = document.getElementById('newPromptContent').value;
            const description = document.getElementById('newPromptDescription').value;
            const category = document.getElementById('newPromptCategory').value;

            try {
                await API.createPrompt({ title, content, description, category });
                await STATE.loadPrompts();
                modal.remove();
                this.renderPromptsPage();
                alert('✅ Промпт создан!');
            } catch (error) {
                console.error('Ошибка при создании промпта:', error);
                alert('Ошибка при создании промпта');
            }
        });
    }

    // Показать форму создания проекта
    showCreateProjectForm() {
        const modal = document.createElement('div');
        modal.className = 'modal-overlay';
        modal.innerHTML = `
            <div class="modal">
                <div class="modal-header">
                    <h2>➕ Новый проект</h2>
                    <button class="btn-icon close" onclick="this.closest('.modal-overlay').remove()">✕</button>
                </div>

                <form id="createProjectForm" class="form-large">
                    <div class="form-group">
                        <label>Название *</label>
                        <input type="text" class="form-input" id="newProjectName" required>
                    </div>

                    <div class="form-group">
                        <label>Описание</label>
                        <textarea class="form-input" id="newProjectDescription"></textarea>
                    </div>

                    <div class="form-actions">
                        <button type="submit" class="btn btn-primary">✅ Создать</button>
                        <button type="button" class="btn btn-secondary" onclick="this.closest('.modal-overlay').remove()">Отмена</button>
                    </div>
                </form>
            </div>
        `;

        document.body.appendChild(modal);

        document.getElementById('createProjectForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            const name = document.getElementById('newProjectName').value;
            const description = document.getElementById('newProjectDescription').value;

            try {
                const project = await API.createProject({ name, description });
                await API.createProjectStructure(project.id);
                await STATE.loadProjects();
                modal.remove();
                this.renderProjectsPage();
                alert('✅ Проект создан!');
            } catch (error) {
                console.error('Ошибка при создании проекта:', error);
                alert('Ошибка при создании проекта');
            }
        });
    }

    // Фильтровать промпты
    filterPrompts(query) {
        STATE.setSearchQuery(query);
        const filtered = STATE.searchPrompts(query);
        const container = document.getElementById('promptsContainer');

        container.innerHTML = filtered.length === 0 ? `
            <div class="empty-state">
                <p>Промптов не найдено</p>
            </div>
        ` : filtered.map(prompt => `
            <div class="prompt-card" onclick="MODAL.openPromptModal(${prompt.id})">
                <div class="card-header">
                    <h3>${this.escapeHtml(prompt.title)}</h3>
                    <span class="category-badge">${prompt.category}</span>
                </div>
                <p class="card-description">${this.escapeHtml((prompt.description || '').substring(0, 100))}...</p>
            </div>
        `).join('');
    }

    // Фильтровать по категории
    filterByCategory(category) {
        STATE.selectCategory(category);
        this.renderPromptsPage();
    }

    // Удалить промпт
    async deletePrompt(id) {
        if (confirm('Вы уверены?')) {
            try {
                await API.deletePrompt(id);
                await STATE.loadPrompts();
                this.renderPromptsPage();
            } catch (error) {
                console.error('Ошибка:', error);
            }
        }
    }

    // Удалить проект
    async deleteProject(id) {
        if (confirm('Вы уверены?')) {
            try {
                await API.deleteProject(id);
                await STATE.loadProjects();
                this.renderProjectsPage();
            } catch (error) {
                console.error('Ошибка:', error);
            }
        }
    }

    // Экранировать HTML
    escapeHtml(text) {
        if (!text) return '';
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    // Отрисовать страницу Настроек
    async renderSettingsPage() {
        this.container.innerHTML = `
            <div class="page settings-page">
                <div class="page-header">
                    <h1>⚙️ Настройки</h1>
                </div>

                <div class="settings-card">
                    <h2>📊 Информация о приложении</h2>
                    <div class="info-group">
                        <span class="info-label">Версия:</span>
                        <span class="info-value">v2.0.0</span>
                    </div>
                    <div class="info-group">
                        <span class="info-label">Автор:</span>
                        <span class="info-value">PANDORA Team</span>
                    </div>
                    <div class="info-group">
                        <span class="info-label">Сервер:</span>
                        <span class="info-value">http://127.0.0.1:8000</span>
                    </div>
                </div>

                <div class="settings-card">
                    <h2>💾 Управление данными</h2>
                    <button class="btn btn-primary" onclick="UI.exportAllData()">📤 Экспортировать все данные</button>
                    <button class="btn btn-secondary" onclick="UI.clearDatabase()">🗑️ Очистить базу данных</button>
                </div>

                <div class="settings-card">
                    <h2>🔌 Плагины и расширения</h2>
                    <p>В этом разделе будут доступны плагины и расширения для PANDORA.</p>
                    <p style="color: #999; font-size: 0.9rem;">Функция плагинов будет добавлена в следующей версии</p>
                </div>

                <div class="settings-card">
                    <h2>❓ Справка</h2>
                    <p><strong>Горячие клавиши:</strong></p>
                    <ul style="margin-left: 1rem; color: #666;">
                        <li>Ctrl+K - Поиск</li>
                        <li>Ctrl+N - Новый промпт</li>
                        <li>Ctrl+P - Новый проект</li>
                        <li>Escape - Закрыть модаль</li>
                    </ul>
                </div>
            </div>
        `;
    }

    // Экспортировать все данные
    async exportAllData() {
        try {
            const prompts = STATE.state.prompts;
            const projects = STATE.state.projects;
            
            const data = {
                version: '2.0.0',
                exportDate: new Date().toISOString(),
                prompts,
                projects,
                stats: STATE.state.stats
            };

            const json = JSON.stringify(data, null, 2);
            const blob = new Blob([json], { type: 'application/json' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `pandora-backup-${Date.now()}.json`;
            a.click();
            URL.revokeObjectURL(url);

            alert('✅ Данные экспортированы успешно!');
        } catch (error) {
            console.error('Ошибка при экспорте:', error);
            alert('Ошибка при экспорте данных');
        }
    }

    // Очистить базу данных
    async clearDatabase() {
        if (confirm('⚠️ ВНИМАНИЕ! Это удалит ВСЕ промпты и проекты. Вы уверены?')) {
            if (confirm('Это действие необратимо. Нажмите ОК для подтверждения.')) {
                try {
                    // Очищаем всех промптов и проектов
                    for (const prompt of STATE.state.prompts) {
                        await API.deletePrompt(prompt.id);
                    }
                    for (const project of STATE.state.projects) {
                        await API.deleteProject(project.id);
                    }

                    await STATE.initialize();
                    this.renderSettingsPage();
                    alert('✅ База данных очищена!');
                } catch (error) {
                    console.error('Ошибка:', error);
                    alert('Ошибка при очистке БД');
                }
            }
        }
    }


// Экспортируем единственный экземпляр
const UI = new UIModule();

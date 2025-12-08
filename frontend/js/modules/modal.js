// Modal Module - Управление модальными окнами
class ModalModule {
    constructor() {
        this.currentModal = null;
        this.init();
    }

    init() {
        // Закрытие модали при клике на фон
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('modal-overlay')) {
                this.closeModal();
            }
        });

        // Закрытие модали на Escape
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                this.closeModal();
            }
        });
    }

    // Открыть модальное окно промпта
    async openPromptModal(promptId) {
        try {
            const prompt = await API.getPromptById(promptId);
            if (!prompt) throw new Error('Промпт не найден');

            const modal = document.createElement('div');
            modal.className = 'modal-overlay';
            modal.innerHTML = `
                <div class="modal modal-large">
                    <div class="modal-header">
                        <h2>${this.escapeHtml(prompt.title)}</h2>
                        <div class="modal-buttons">
                            <button class="btn-icon" title="Копировать" onclick="MODAL.copyPromptContent('${promptId}')">📋</button>
                            <button class="btn-icon" title="Перевести" onclick="MODAL.translatePrompt('${promptId}')">🌐</button>
                            <button class="btn-icon" title="Экспортировать" onclick="MODAL.exportPrompt('${promptId}')">📤</button>
                            <button class="btn-icon close" onclick="MODAL.closeModal()">✕</button>
                        </div>
                    </div>

                    <div class="modal-tabs">
                        <button class="tab-btn active" data-tab="view">👁️ Просмотр</button>
                        <button class="tab-btn" data-tab="edit">✏️ Редактирование</button>
                        <button class="tab-btn" data-tab="keywords">🔑 Ключевые слова</button>
                    </div>

                    <div class="modal-content">
                        <!-- Вкладка: Просмотр -->
                        <div class="tab-content active" data-tab="view">
                            <div class="prompt-meta">
                                <div class="meta-item">
                                    <span class="meta-label">📂 Категория:</span>
                                    <span class="meta-value badge">${this.escapeHtml(prompt.category)}</span>
                                </div>
                                <div class="meta-item">
                                    <span class="meta-label">📅 Создан:</span>
                                    <span class="meta-value">${new Date(prompt.created_at).toLocaleDateString('ru-RU')}</span>
                                </div>
                                <div class="meta-item">
                                    <span class="meta-label">📊 Использований:</span>
                                    <span class="meta-value">${prompt.usage_count || 0}</span>
                                </div>
                            </div>

                            ${prompt.description ? `
                                <div class="section">
                                    <h4>Описание</h4>
                                    <div class="text-content">${this.escapeHtml(prompt.description)}</div>
                                </div>
                            ` : ''}

                            <div class="section">
                                <h4>Содержание</h4>
                                <div class="code-block">
                                    <div class="code-content">${this.escapeHtml(prompt.content)}</div>
                                    <button class="btn-copy" onclick="MODAL.copyPromptContent('${promptId}')">Копировать</button>
                                </div>
                            </div>

                            ${prompt.tags && prompt.tags.length > 0 ? `
                                <div class="section">
                                    <h4>Теги</h4>
                                    <div class="tags-list">
                                        ${prompt.tags.map(tag => `
                                            <span class="tag" style="background-color: ${tag.color || '#3B82F6'}">${this.escapeHtml(tag.name)}</span>
                                        `).join('')}
                                    </div>
                                </div>
                            ` : ''}
                        </div>

                        <!-- Вкладка: Редактирование -->
                        <div class="tab-content" data-tab="edit">
                            <form class="edit-form" id="editPromptForm">
                                <div class="form-group">
                                    <label>Название</label>
                                    <input type="text" class="form-input" value="${this.escapeHtml(prompt.title)}" id="editTitle">
                                </div>

                                <div class="form-group">
                                    <label>Категория</label>
                                    <select class="form-input" id="editCategory">
                                        <option value="${prompt.category}">${prompt.category}</option>
                                        <option value="development">development</option>
                                        <option value="writing">writing</option>
                                        <option value="analysis">analysis</option>
                                        <option value="business">business</option>
                                        <option value="creative">creative</option>
                                    </select>
                                </div>

                                <div class="form-group">
                                    <label>Описание</label>
                                    <textarea class="form-input" id="editDescription">${this.escapeHtml(prompt.description || '')}</textarea>
                                </div>

                                <div class="form-group">
                                    <label>Содержание</label>
                                    <textarea class="form-input form-textarea-large" id="editContent">${this.escapeHtml(prompt.content)}</textarea>
                                </div>

                                <div class="form-actions">
                                    <button type="submit" class="btn btn-primary">💾 Сохранить</button>
                                    <button type="button" class="btn btn-secondary" onclick="MODAL.closeModal()">Отмена</button>
                                </div>
                            </form>
                        </div>

                        <!-- Вкладка: Ключевые слова -->
                        <div class="tab-content" data-tab="keywords">
                            <div class="keywords-section">
                                <button class="btn btn-primary" onclick="MODAL.extractKeywordsForPrompt('${promptId}')">
                                    🔍 Извлечь ключевые слова
                                </button>
                                <div id="keywordsResult" style="margin-top: 20px;"></div>
                            </div>
                        </div>
                    </div>
                </div>
            `;

            document.body.appendChild(modal);
            this.currentModal = modal;

            // Обработчик табов
            modal.querySelectorAll('.tab-btn').forEach(btn => {
                btn.addEventListener('click', () => this.switchTab(btn.dataset.tab));
            });

            // Обработчик редактирования
            document.getElementById('editPromptForm').addEventListener('submit', async (e) => {
                e.preventDefault();
                await this.savePromptChanges(promptId);
            });

        } catch (error) {
            console.error('Ошибка при открытии модали промпта:', error);
            alert('Ошибка при загрузке промпта');
        }
    }

    // Открыть модальное окно проекта
    async openProjectModal(projectId) {
        try {
            const project = await API.getProjectById(projectId);
            if (!project) throw new Error('Проект не найден');

            const modal = document.createElement('div');
            modal.className = 'modal-overlay';
            modal.innerHTML = `
                <div class="modal modal-large">
                    <div class="modal-header">
                        <h2>📁 ${this.escapeHtml(project.name)}</h2>
                        <button class="btn-icon close" onclick="MODAL.closeModal()">✕</button>
                    </div>

                    <div class="modal-tabs">
                        <button class="tab-btn active" data-tab="tasks">✓ Задачи</button>
                        <button class="tab-btn" data-tab="process">📝 Процесс</button>
                        <button class="tab-btn" data-tab="info">ℹ️ Информация</button>
                    </div>

                    <div class="modal-content">
                        <!-- Вкладка: Задачи -->
                        <div class="tab-content active" data-tab="tasks">
                            <textarea class="form-input form-textarea-large" id="projectTasks" placeholder="Введите задачи..."></textarea>
                            <button class="btn btn-primary" onclick="MODAL.saveProjectTasks('${projectId}')">💾 Сохранить</button>
                        </div>

                        <!-- Вкладка: Процесс -->
                        <div class="tab-content" data-tab="process">
                            <textarea class="form-input form-textarea-large" id="projectProcess" placeholder="Введите описание процесса разработки..."></textarea>
                            <button class="btn btn-primary" onclick="MODAL.saveProjectProcess('${projectId}')">💾 Сохранить</button>
                        </div>

                        <!-- Вкладка: Информация -->
                        <div class="tab-content" data-tab="info">
                            <div class="project-info">
                                <h4>О проекте</h4>
                                <p><strong>Описание:</strong> ${this.escapeHtml(project.description || 'Нет описания')}</p>
                                <p><strong>Статус:</strong> <span class="badge">${project.status}</span></p>
                                <p><strong>Создан:</strong> ${new Date(project.created_at).toLocaleDateString('ru-RU')}</p>
                            </div>
                        </div>
                    </div>
                </div>
            `;

            document.body.appendChild(modal);
            this.currentModal = modal;

            // Загружаем файлы проекта
            const tasksData = await API.getProjectTasks(projectId);
            const processData = await API.getProjectProcess(projectId);

            document.getElementById('projectTasks').value = tasksData.content || '';
            document.getElementById('projectProcess').value = processData.content || '';

            // Обработчик табов
            modal.querySelectorAll('.tab-btn').forEach(btn => {
                btn.addEventListener('click', () => this.switchTab(btn.dataset.tab));
            });

        } catch (error) {
            console.error('Ошибка при открытии модали проекта:', error);
            alert('Ошибка при загрузке проекта');
        }
    }

    // Переключение вкладок
    switchTab(tabName) {
        const modal = this.currentModal || document.querySelector('.modal');
        
        modal.querySelectorAll('.tab-btn').forEach(btn => {
            btn.classList.toggle('active', btn.dataset.tab === tabName);
        });

        modal.querySelectorAll('.tab-content').forEach(content => {
            content.classList.toggle('active', content.dataset.tab === tabName);
        });
    }

    // Копировать содержимое промпта
    async copyPromptContent(promptId) {
        try {
            const prompt = await API.getPromptById(promptId);
            navigator.clipboard.writeText(prompt.content);
            alert('✅ Промпт скопирован в буфер обмена!');
        } catch (error) {
            console.error('Ошибка при копировании:', error);
        }
    }

    // Извлечь ключевые слова
    async extractKeywordsForPrompt(promptId) {
        try {
            const prompt = await API.getPromptById(promptId);
            const data = await API.extractKeywords(prompt.content);

            const resultDiv = document.getElementById('keywordsResult');
            resultDiv.innerHTML = `
                <h4>Найдено ${data.keywords.length} ключевых слов:</h4>
                <div class="keywords-cloud">
                    ${data.keywords.map((kw, i) => `
                        <span class="keyword-pill" style="background-color: hsl(${i * 10}, 70%, 50%)">${this.escapeHtml(kw)}</span>
                    `).join('')}
                </div>
            `;
        } catch (error) {
            console.error('Ошибка при извлечении ключевых слов:', error);
        }
    }

    // Сохранить изменения промпта
    async savePromptChanges(promptId) {
        try {
            const title = document.getElementById('editTitle').value;
            const category = document.getElementById('editCategory').value;
            const description = document.getElementById('editDescription').value;
            const content = document.getElementById('editContent').value;

            await API.updatePrompt(promptId, {
                title,
                category,
                description,
                content
            });

            alert('✅ Промпт сохранен!');
            await STATE.loadPrompts();
            this.closeModal();
        } catch (error) {
            console.error('Ошибка при сохранении:', error);
            alert('Ошибка при сохранении промпта');
        }
    }

    // Сохранить задачи проекта
    async saveProjectTasks(projectId) {
        try {
            const content = document.getElementById('projectTasks').value;
            await API.updateProjectTasks(projectId, content);
            alert('✅ Задачи сохранены!');
        } catch (error) {
            console.error('Ошибка при сохранении задач:', error);
        }
    }

    // Сохранить процесс проекта
    async saveProjectProcess(projectId) {
        try {
            const content = document.getElementById('projectProcess').value;
            await API.updateProjectProcess(projectId, content);
            alert('✅ Процесс сохранен!');
        } catch (error) {
            console.error('Ошибка при сохранении процесса:', error);
        }
    }

    // Экспортировать промпт
    async exportPrompt(promptId) {
        try {
            const result = await API.exportPromptTxt(promptId);
            alert('✅ Промпт экспортирован: ' + result.file_path);
        } catch (error) {
            console.error('Ошибка при экспорте:', error);
        }
    }

    // Перевести промпт (placeholder)
    async translatePrompt(promptId) {
        alert('🌐 Функция перевода будет добавлена в следующей версии');
    }

    // Закрыть модальное окно
    closeModal() {
        if (this.currentModal) {
            this.currentModal.remove();
            this.currentModal = null;
        }
    }

    // Экранировать HTML
    escapeHtml(text) {
        if (!text) return '';
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
}

// Экспортируем единственный экземпляр
const MODAL = new ModalModule();

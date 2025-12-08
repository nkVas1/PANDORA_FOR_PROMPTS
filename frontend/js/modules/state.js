// State Module - Управление состоянием приложения
class StateModule {
    constructor() {
        this.state = {
            currentPage: 'dashboard',
            currentProject: null,
            currentPrompt: null,
            selectedCategory: null,
            searchQuery: '',
            prompts: [],
            projects: [],
            categories: [],
            tags: [],
            stats: {}
        };

        this.listeners = [];
    }

    // Подписка на изменения состояния
    subscribe(callback) {
        this.listeners.push(callback);
    }

    // Уведомление всех слушателей об изменении состояния
    notify() {
        this.listeners.forEach(callback => callback(this.state));
    }

    // Обновление состояния
    setState(updates) {
        this.state = { ...this.state, ...updates };
        this.notify();
    }

    // Переход на страницу
    goToPage(page) {
        this.setState({ currentPage: page });
        window.location.hash = `#${page}`;
    }

    // Выбор промпта
    selectPrompt(prompt) {
        this.setState({ currentPrompt: prompt });
    }

    // Выбор проекта
    selectProject(project) {
        this.setState({ currentProject: project });
    }

    // Выбор категории для фильтрации
    selectCategory(category) {
        this.setState({ selectedCategory: category });
    }

    // Установка поискового запроса
    setSearchQuery(query) {
        this.setState({ searchQuery: query });
    }

    // Загрузка всех промптов
    async loadPrompts() {
        try {
            const prompts = await API.getPrompts();
            this.setState({ prompts });
            return prompts;
        } catch (error) {
            console.error('Ошибка при загрузке промптов:', error);
            return [];
        }
    }

    // Загрузка всех проектов
    async loadProjects() {
        try {
            const projects = await API.getProjects();
            this.setState({ projects });
            return projects;
        } catch (error) {
            console.error('Ошибка при загрузке проектов:', error);
            return [];
        }
    }

    // Загрузка статистики
    async loadStats() {
        try {
            const stats = await API.getStats();
            this.setState({ stats });
            return stats;
        } catch (error) {
            console.error('Ошибка при загрузке статистики:', error);
            return {};
        }
    }

    // Загрузка категорий
    async loadCategories() {
        try {
            const categories = await API.getCategories();
            this.setState({ categories });
            return categories;
        } catch (error) {
            console.error('Ошибка при загрузке категорий:', error);
            return [];
        }
    }

    // Загрузка всех данных при инициализации
    async initialize() {
        console.log('🚀 Инициализирую приложение...');
        await Promise.all([
            this.loadPrompts(),
            this.loadProjects(),
            this.loadStats(),
            this.loadCategories()
        ]);
        console.log('✅ Приложение инициализировано');
    }

    // Получить текущее состояние
    getState() {
        return { ...this.state };
    }

    // Получить промпты по категории
    getPromptsByCategory(category) {
        return this.state.prompts.filter(p => p.category === category);
    }

    // Поиск промптов
    searchPrompts(query) {
        if (!query) return this.state.prompts;
        
        const q = query.toLowerCase();
        return this.state.prompts.filter(p => 
            p.title.toLowerCase().includes(q) ||
            p.content.toLowerCase().includes(q) ||
            (p.description && p.description.toLowerCase().includes(q))
        );
    }
}

// Экспортируем единственный экземпляр
const STATE = new StateModule();

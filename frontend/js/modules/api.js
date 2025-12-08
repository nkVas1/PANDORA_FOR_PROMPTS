// API Module - Работа с backend API
class APIModule {
    constructor() {
        this.baseURL = 'http://127.0.0.1:8000/api';
    }

    // ===== PROMPTS =====
    async getPrompts() {
        const response = await fetch(`${this.baseURL}/prompts`);
        return response.json();
    }

    async getPromptById(id) {
        const response = await fetch(`${this.baseURL}/prompts/${id}`);
        return response.json();
    }

    async createPrompt(data) {
        const response = await fetch(`${this.baseURL}/prompts`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        return response.json();
    }

    async updatePrompt(id, data) {
        const response = await fetch(`${this.baseURL}/prompts/${id}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        return response.json();
    }

    async deletePrompt(id) {
        const response = await fetch(`${this.baseURL}/prompts/${id}`, {
            method: 'DELETE'
        });
        return response.json();
    }

    async searchPrompts(query, category = null) {
        let url = `${this.baseURL}/prompts/search?q=${encodeURIComponent(query)}`;
        if (category) url += `&category=${category}`;
        const response = await fetch(url);
        return response.json();
    }

    async getPromptsByCategory(category) {
        const response = await fetch(`${this.baseURL}/prompts/by-category/${category}`);
        return response.json();
    }

    async autoTagPrompt(id) {
        const response = await fetch(`${this.baseURL}/prompts/${id}/auto-tag`, {
            method: 'POST'
        });
        return response.json();
    }

    async extractKeywords(content) {
        const response = await fetch(`${this.baseURL}/prompts/extract-keywords`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ content })
        });
        return response.json();
    }

    async exportPromptTxt(id) {
        const response = await fetch(`${this.baseURL}/prompts/${id}/export-txt`, {
            method: 'POST'
        });
        return response.json();
    }

    // ===== PROJECTS =====
    async getProjects() {
        const response = await fetch(`${this.baseURL}/projects`);
        return response.json();
    }

    async getProjectById(id) {
        const response = await fetch(`${this.baseURL}/projects/${id}`);
        return response.json();
    }

    async createProject(data) {
        const response = await fetch(`${this.baseURL}/projects`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        return response.json();
    }

    async updateProject(id, data) {
        const response = await fetch(`${this.baseURL}/projects/${id}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        return response.json();
    }

    async deleteProject(id) {
        const response = await fetch(`${this.baseURL}/projects/${id}`, {
            method: 'DELETE'
        });
        return response.json();
    }

    async createProjectStructure(id) {
        const response = await fetch(`${this.baseURL}/projects/${id}/create-structure`, {
            method: 'POST'
        });
        return response.json();
    }

    // ===== PROJECT FILES =====
    async getProjectTasks(id) {
        const response = await fetch(`${this.baseURL}/projects/${id}/tasks`);
        return response.json();
    }

    async updateProjectTasks(id, content) {
        const response = await fetch(`${this.baseURL}/projects/${id}/tasks`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ content })
        });
        return response.json();
    }

    async getProjectProcess(id) {
        const response = await fetch(`${this.baseURL}/projects/${id}/process`);
        return response.json();
    }

    async updateProjectProcess(id, content) {
        const response = await fetch(`${this.baseURL}/projects/${id}/process`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ content })
        });
        return response.json();
    }

    // ===== STATS =====
    async getStats() {
        const response = await fetch(`${this.baseURL}/stats`);
        return response.json();
    }

    async getCategories() {
        const response = await fetch(`${this.baseURL}/prompts/categories`);
        return response.json();
    }

    // ===== TAGS =====
    async getTags() {
        const response = await fetch(`${this.baseURL}/tags`);
        return response.json();
    }

    async createTag(data) {
        const response = await fetch(`${this.baseURL}/tags`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        return response.json();
    }
}

// Экспортируем единственный экземпляр
const API = new APIModule();

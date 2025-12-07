import axios from 'axios'

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000/api'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Prompts API
export const promptsApi = {
  getAll: (skip = 0, limit = 100) =>
    api.get('/prompts', { params: { skip, limit } }),
  get: (id: number) =>
    api.get(`/prompts/${id}`),
  create: (data: any) =>
    api.post('/prompts', data),
  update: (id: number, data: any) =>
    api.put(`/prompts/${id}`, data),
  delete: (id: number) =>
    api.delete(`/prompts/${id}`),
  search: (q: string, category?: string, tags?: string[]) =>
    api.get('/prompts/search', { params: { q, category, tags } }),
  use: (id: number) =>
    api.post(`/prompts/${id}/use`),
  autoTag: (id: number) =>
    api.post(`/prompts/${id}/auto-tag`),
}

// Tags API
export const tagsApi = {
  getAll: () =>
    api.get('/tags'),
  create: (data: any) =>
    api.post('/tags', data),
  delete: (id: number) =>
    api.delete(`/tags/${id}`),
}

// Projects API
export const projectsApi = {
  getAll: () =>
    api.get('/projects'),
  get: (id: number) =>
    api.get(`/projects/${id}`),
  create: (data: any) =>
    api.post('/projects', data),
  update: (id: number, data: any) =>
    api.put(`/projects/${id}`, data),
  delete: (id: number) =>
    api.delete(`/projects/${id}`),
  addProcessEntry: (id: number, entry: string) =>
    api.post(`/projects/${id}/process`, { entry }),
  addTask: (id: number, data: any) =>
    api.post(`/projects/${id}/tasks`, data),
  updateTask: (id: number, data: any) =>
    api.put(`/tasks/${id}`, data),
}

// Import API
export const importApi = {
  importJson: (file: File, sourceName: string) => {
    const formData = new FormData()
    formData.append('file', file)
    formData.append('source_name', sourceName)
    return api.post('/import/json', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
  },
  importBatch: (data: any) =>
    api.post('/import/batch', data),
}

// Stats API
export const statsApi = {
  get: () =>
    api.get('/stats'),
}

export default api

import { create } from 'zustand'

interface Prompt {
  id: number
  title: string
  content: string
  description?: string
  category: string
  tags: Tag[]
  usage_count: number
  created_at: string
  updated_at: string
}

interface Tag {
  id: number
  name: string
  color: string
  usage_count: number
}

interface Project {
  id: number
  name: string
  description?: string
  status: string
  created_at: string
  updated_at: string
}

interface PromptStore {
  prompts: Prompt[]
  selectedPrompt: Prompt | null
  tags: Tag[]
  projects: Project[]
  isLoading: boolean
  error: string | null

  setPrompts: (prompts: Prompt[]) => void
  setSelectedPrompt: (prompt: Prompt | null) => void
  setTags: (tags: Tag[]) => void
  setProjects: (projects: Project[]) => void
  setLoading: (loading: boolean) => void
  setError: (error: string | null) => void
}

export const usePromptStore = create<PromptStore>((set) => ({
  prompts: [],
  selectedPrompt: null,
  tags: [],
  projects: [],
  isLoading: false,
  error: null,

  setPrompts: (prompts) => set({ prompts }),
  setSelectedPrompt: (selectedPrompt) => set({ selectedPrompt }),
  setTags: (tags) => set({ tags }),
  setProjects: (projects) => set({ projects }),
  setLoading: (isLoading) => set({ isLoading }),
  setError: (error) => set({ error }),
}))

interface ViewStore {
  currentView: 'prompts' | 'projects' | 'settings'
  sidebarOpen: boolean
  searchQuery: string
  selectedCategory: string | null

  setCurrentView: (view: 'prompts' | 'projects' | 'settings') => void
  setSidebarOpen: (open: boolean) => void
  setSearchQuery: (query: string) => void
  setSelectedCategory: (category: string | null) => void
}

export const useViewStore = create<ViewStore>((set) => ({
  currentView: 'prompts',
  sidebarOpen: true,
  searchQuery: '',
  selectedCategory: null,

  setCurrentView: (currentView) => set({ currentView }),
  setSidebarOpen: (sidebarOpen) => set({ sidebarOpen }),
  setSearchQuery: (searchQuery) => set({ searchQuery }),
  setSelectedCategory: (selectedCategory) => set({ selectedCategory }),
}))

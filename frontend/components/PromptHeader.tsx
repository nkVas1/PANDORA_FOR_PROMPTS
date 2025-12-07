'use client'

import { Search, Filter, Plus } from 'lucide-react'
import { Button } from './Button'
import { useState } from 'react'

interface PromptHeaderProps {
  onSearch: (query: string) => void
  onFilterClick: () => void
  onAddClick: () => void
  totalCount: number
}

export function PromptHeader({
  onSearch,
  onFilterClick,
  onAddClick,
  totalCount,
}: PromptHeaderProps) {
  const [searchQuery, setSearchQuery] = useState('')

  const handleSearch = (e: React.ChangeEvent<HTMLInputElement>) => {
    const query = e.target.value
    setSearchQuery(query)
    onSearch(query)
  }

  return (
    <div className="bg-dark-800 border-b border-dark-700 p-6 space-y-4">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-white">Промпты</h1>
          <p className="text-dark-400 mt-1">Всего: {totalCount} промптов</p>
        </div>
        <Button onClick={onAddClick} className="flex items-center gap-2">
          <Plus size={20} />
          Добавить
        </Button>
      </div>

      <div className="flex items-center gap-3">
        <div className="flex-1 relative">
          <Search className="absolute left-3 top-3 text-dark-500" size={20} />
          <input
            type="text"
            placeholder="Поиск промптов..."
            value={searchQuery}
            onChange={handleSearch}
            className="w-full bg-dark-700 text-white placeholder-dark-500 rounded-lg pl-10 pr-4 py-2 border border-dark-600 focus:border-primary-500 focus:outline-none transition-smooth"
          />
        </div>
        <Button
          onClick={onFilterClick}
          variant="secondary"
          className="flex items-center gap-2"
        >
          <Filter size={20} />
          Фильтры
        </Button>
      </div>
    </div>
  )
}

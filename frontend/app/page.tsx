'use client'

import { useEffect, useState } from 'react'
import { promptsApi, statsApi } from '@/lib/api'
import { Card } from '@/components/Card'
import { Button } from '@/components/Button'

export default function Home() {
  const [stats, setStats] = useState<any>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadStats()
  }, [])

  const loadStats = async () => {
    try {
      const response = await statsApi.get()
      setStats(response.data)
    } catch (error) {
      console.error('Error loading stats:', error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-dark-900">
      {/* Header */}
      <div className="bg-gradient-to-r from-primary-600 to-primary-800 px-8 py-12">
        <h1 className="text-4xl font-bold text-white mb-4">PANDORA Prompts Manager</h1>
        <p className="text-primary-100 text-lg">
          Профессиональный инструмент для управления, структуризации и распределения промптов
        </p>
      </div>

      {/* Stats Section */}
      <div className="max-w-7xl mx-auto px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-12">
          {loading ? (
            <div className="col-span-4 text-center text-dark-400">Загрузка...</div>
          ) : (
            <>
              <Card>
                <div className="text-center">
                  <div className="text-4xl font-bold text-primary-500 mb-2">
                    {stats?.total_prompts || 0}
                  </div>
                  <div className="text-dark-400">Всего промптов</div>
                </div>
              </Card>
              <Card>
                <div className="text-center">
                  <div className="text-4xl font-bold text-green-500 mb-2">
                    {stats?.total_tags || 0}
                  </div>
                  <div className="text-dark-400">Тегов</div>
                </div>
              </Card>
              <Card>
                <div className="text-center">
                  <div className="text-4xl font-bold text-blue-500 mb-2">
                    {stats?.total_projects || 0}
                  </div>
                  <div className="text-dark-400">Проектов</div>
                </div>
              </Card>
              <Card>
                <div className="text-center">
                  <div className="text-4xl font-bold text-purple-500 mb-2">
                    {stats?.total_prompts ? Math.round((stats?.total_prompts / 1000) * 100) / 100 : 0}K
                  </div>
                  <div className="text-dark-400">Использовано</div>
                </div>
              </Card>
            </>
          )}
        </div>

        {/* Features */}
        <div className="mb-12">
          <h2 className="text-2xl font-bold text-white mb-6">Возможности</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {[
              {
                title: 'Управление промптами',
                description: 'Сохраняйте, категоризируйте и структурируйте все ваши промпты в одном месте',
              },
              {
                title: 'Автотегирование',
                description: 'Автоматическое распределение по категориям и генерация релевантных тегов',
              },
              {
                title: 'Поиск и фильтрация',
                description: 'Быстро находите нужные промпты по ключевым словам, тегам и категориям',
              },
              {
                title: 'Управление проектами',
                description: 'Ведите процесс разработки и список задач для каждого проекта',
              },
              {
                title: 'Массовый импорт',
                description: 'Загружайте промпты пакетом из JSON файлов и различных источников',
              },
              {
                title: 'Локальное хранилище',
                description: 'Все данные хранятся локально на вашем компьютере, никакой облака',
              },
            ].map((feature, idx) => (
              <Card key={idx} hoverable>
                <h3 className="text-lg font-semibold text-white mb-2">{feature.title}</h3>
                <p className="text-dark-400">{feature.description}</p>
              </Card>
            ))}
          </div>
        </div>

        {/* CTA */}
        <div className="bg-dark-800 rounded-lg border border-dark-700 p-8 text-center">
          <h2 className="text-2xl font-bold text-white mb-4">Готовы начать?</h2>
          <p className="text-dark-400 mb-6">Перейдите в раздел "Промпты" чтобы начать управлять вашей базой</p>
          <Button size="lg">Перейти к промптам</Button>
        </div>
      </div>
    </div>
  )
}

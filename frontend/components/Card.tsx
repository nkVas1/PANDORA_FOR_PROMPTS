'use client'

import { ReactNode } from 'react'

interface CardProps {
  children: ReactNode
  className?: string
  onClick?: () => void
  hoverable?: boolean
}

export function Card({
  children,
  className = '',
  onClick,
  hoverable = false,
}: CardProps) {
  return (
    <div
      onClick={onClick}
      className={`
        bg-dark-800 rounded-lg border border-dark-700 p-6
        ${hoverable ? 'hover:border-primary-500 hover:shadow-lg hover:shadow-primary-500/20 transition-smooth cursor-pointer' : ''}
        ${className}
      `}
    >
      {children}
    </div>
  )
}

'use client'

import { ReactNode } from 'react'

interface TextareaProps {
  label?: string
  placeholder?: string
  value: string
  onChange: (value: string) => void
  rows?: number
  required?: boolean
  error?: string
  className?: string
}

export function Textarea({
  label,
  placeholder,
  value,
  onChange,
  rows = 4,
  required = false,
  error,
  className = '',
}: TextareaProps) {
  return (
    <div className="w-full">
      {label && (
        <label className="block text-sm font-medium text-white mb-2">
          {label}
          {required && <span className="text-red-500">*</span>}
        </label>
      )}
      <textarea
        placeholder={placeholder}
        value={value}
        onChange={(e) => onChange(e.target.value)}
        rows={rows}
        className={`
          w-full px-4 py-2 bg-dark-700 text-white placeholder-dark-500
          rounded-lg border border-dark-600 focus:border-primary-500 
          focus:outline-none transition-smooth resize-none
          ${error ? 'border-red-500' : ''}
          ${className}
        `}
      />
      {error && <p className="text-red-500 text-sm mt-1">{error}</p>}
    </div>
  )
}

'use client'

interface TagProps {
  name: string
  color?: string
  onRemove?: () => void
  clickable?: boolean
  onClick?: () => void
}

export function Tag({
  name,
  color = '#3B82F6',
  onRemove,
  clickable = false,
  onClick,
}: TagProps) {
  return (
    <div
      className={`
        inline-flex items-center gap-2 px-3 py-1 rounded-full text-sm font-medium
        ${clickable ? 'cursor-pointer hover:opacity-80' : ''}
        transition-smooth
      `}
      style={{ backgroundColor: color + '20', color: color, borderColor: color }}
      onClick={onClick}
    >
      <span>{name}</span>
      {onRemove && (
        <button
          onClick={(e) => {
            e.stopPropagation()
            onRemove()
          }}
          className="ml-1 hover:opacity-70"
        >
          ×
        </button>
      )}
    </div>
  )
}

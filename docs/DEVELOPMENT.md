# PANDORA Development Guide

Руководство для разработчиков, которые хотят участвовать в развитии проекта.

## Структура проекта

```
PANDORA_FOR_PROMPTS/
├── backend/                 # Python FastAPI Backend
│   ├── app/
│   │   ├── api/            # REST API routes
│   │   ├── models/         # Database models and Pydantic schemas
│   │   ├── services/       # Business logic layer
│   │   ├── db/             # Database configuration
│   │   ├── utils/          # Utility modules
│   │   ├── config.py       # Configuration
│   │   └── main.py         # FastAPI application factory
│   ├── requirements.txt    # Python dependencies
│   └── run.py             # Run backend server
│
├── frontend/                # Next.js Frontend
│   ├── app/               # Next.js App Router (pages)
│   ├── components/        # Reusable React components
│   ├── lib/              # Utilities, API clients, hooks
│   ├── styles/           # Global and component styles
│   ├── package.json      # npm dependencies
│   └── tsconfig.json     # TypeScript configuration
│
├── data/                  # Local data storage
│   ├── prompts/          # Exported prompts
│   ├── imports/          # Imported data
│   └── projects/         # Project data
│
├── docs/                  # Documentation
│   ├── API.md            # API reference
│   ├── SETUP.md          # Setup instructions
│   └── DEVELOPMENT.md    # This file
│
├── start.py              # Main starter script
├── build.py              # Build script for exe
├── import_data.py        # Import sample data
├── .env.example          # Environment variables template
├── .gitignore            # Git ignore rules
├── README.md             # Project README
└── requirements.txt      # Python dependencies for root (if needed)
```

## Technology Stack

### Backend
- **Framework**: FastAPI 0.104.1
- **Database**: SQLite with SQLAlchemy ORM
- **Server**: Uvicorn
- **Validation**: Pydantic
- **Python**: 3.9+

### Frontend
- **Framework**: Next.js 15.x
- **UI Library**: React 19.x
- **Styling**: Tailwind CSS 3.x
- **State Management**: Zustand
- **HTTP Client**: Axios
- **JavaScript**: TypeScript + ES2020

## Development Setup

### 1. Clone Repository

```bash
git clone https://github.com/yourusername/PANDORA_FOR_PROMPTS.git
cd PANDORA_FOR_PROMPTS
```

### 2. Setup Python Environment

```bash
# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install backend dependencies
cd backend
pip install -r requirements.txt
cd ..
```

### 3. Setup Node Environment

```bash
cd frontend
npm install
cd ..
```

### 4. Create .env file

```bash
cp .env.example .env
# Edit .env if needed
```

## Running in Development

### Option 1: Automatic (Recommended)

```bash
python start.py
```

### Option 2: Separate Terminals

**Terminal 1 - Backend:**
```bash
cd backend
python run.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

## Code Structure

### Backend Architecture

```
app/
├── api/
│   └── routes.py          # All API endpoints
├── models/
│   ├── __init__.py
│   └── schemas.py         # Pydantic models
├── db/
│   ├── __init__.py        # Database setup
│   └── models.py          # SQLAlchemy models
├── services/
│   ├── __init__.py
│   └── database.py        # Business logic
├── utils/
│   ├── __init__.py
│   ├── auto_tagger.py    # Auto-tagging logic
│   └── importer.py       # Import utilities
├── config.py              # Configuration
└── main.py               # FastAPI app
```

### Frontend Architecture

```
app/                       # Next.js pages
├── page.tsx              # Home page
├── prompts/              # Prompts pages
├── projects/             # Projects pages
└── layout.tsx            # Root layout

components/               # Reusable components
├── Button.tsx           # Button component
├── Card.tsx             # Card component
├── Input.tsx            # Input component
├── Tag.tsx              # Tag component
├── Modal.tsx            # Modal component
└── PromptHeader.tsx     # Prompt header

lib/
├── api.ts               # API client
└── store.ts             # Zustand stores

styles/
└── globals.css          # Global styles
```

## API Development

### Adding a New Endpoint

1. **Create Model** (`app/models/schemas.py`):
```python
class MyModel(BaseModel):
    id: int
    name: str
    value: str
```

2. **Create Service** (`app/services/database.py`):
```python
class MyService:
    @staticmethod
    def create_my_item(db: Session, item: MyModel):
        db_item = DbMyModel(name=item.name)
        db.add(db_item)
        db.commit()
        return db_item
```

3. **Add Route** (`app/api/routes.py`):
```python
@router.post("/my-items", response_model=MyModel)
def create_my_item(item: MyModel, db: Session = Depends(get_db)):
    return MyService.create_my_item(db, item)
```

### Testing API

Use FastAPI's built-in docs:
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

Or use tools:
- **curl**: `curl http://127.0.0.1:8000/api/prompts`
- **Postman**: Import from `/docs` endpoint
- **Python requests**: See docs/API.md

## Frontend Development

### Creating a New Component

```tsx
// components/MyComponent.tsx
'use client'

import { useState } from 'react'

interface MyComponentProps {
  title: string
  onSubmit: (value: string) => void
}

export function MyComponent({ title, onSubmit }: MyComponentProps) {
  const [value, setValue] = useState('')

  return (
    <div className="bg-dark-800 p-6 rounded-lg border border-dark-700">
      <h2 className="text-lg font-bold text-white mb-4">{title}</h2>
      <input
        type="text"
        value={value}
        onChange={(e) => setValue(e.target.value)}
        className="w-full bg-dark-700 text-white rounded px-3 py-2"
      />
      <button
        onClick={() => onSubmit(value)}
        className="mt-4 bg-primary-600 text-white px-4 py-2 rounded hover:bg-primary-700"
      >
        Submit
      </button>
    </div>
  )
}
```

### Using API in Components

```tsx
'use client'

import { useEffect, useState } from 'react'
import { promptsApi } from '@/lib/api'

export function PromptsList() {
  const [prompts, setPrompts] = useState([])

  useEffect(() => {
    loadPrompts()
  }, [])

  const loadPrompts = async () => {
    try {
      const response = await promptsApi.getAll()
      setPrompts(response.data)
    } catch (error) {
      console.error('Error:', error)
    }
  }

  return (
    <div>
      {prompts.map((prompt) => (
        <div key={prompt.id}>{prompt.title}</div>
      ))}
    </div>
  )
}
```

## Git Workflow

### Commit Messages

Use descriptive commit messages in English or Russian:

```
[TYPE] Brief description

TYPE can be:
- feat:     New feature
- fix:      Bug fix
- docs:     Documentation
- style:    Code formatting
- refactor: Code refactoring
- perf:     Performance improvement
- test:     Test addition
- build:    Build configuration
- ci:       CI/CD configuration
- chore:    Other changes

Example:
feat: Add auto-tagging for prompts (Добавлено автотегирование)
fix: Correct API error handling (Исправлена обработка ошибок API)
```

### Pull Request Process

1. Create a feature branch: `git checkout -b feature/my-feature`
2. Make your changes
3. Test thoroughly
4. Commit with descriptive messages
5. Push: `git push origin feature/my-feature`
6. Create Pull Request with description

## Testing

### Backend Tests

```bash
cd backend
pytest
```

### Frontend Tests

```bash
cd frontend
npm test
```

## Performance Tips

### Backend
- Use pagination for large result sets
- Add indexes to frequently queried fields
- Cache expensive operations
- Use lazy loading where appropriate

### Frontend
- Use React.memo for expensive components
- Implement code splitting
- Optimize images and assets
- Use Next.js Image component

## Debugging

### Backend

Add print statements or use Python debugger:
```python
import pdb
pdb.set_trace()
```

Or use logging:
```python
import logging
logger = logging.getLogger(__name__)
logger.debug("Debug message")
```

### Frontend

Use browser DevTools:
- Chrome/Firefox F12
- React DevTools Extension
- Network tab for API debugging

## Common Tasks

### Add a new database model

1. Update `app/db/models.py`
2. Run migration (if needed)
3. Update `app/models/schemas.py`
4. Create service methods
5. Add API routes

### Add a new page

1. Create file in `frontend/app/[name]/page.tsx`
2. Create components in `frontend/components/`
3. Update navigation
4. Test in browser

### Update dependencies

Backend:
```bash
cd backend
pip install --upgrade package-name
pip freeze > requirements.txt
```

Frontend:
```bash
cd frontend
npm update package-name
npm install
```

## Troubleshooting

### Backend won't start
- Check port 8000 is free
- Verify Python 3.9+ installed
- Check requirements installed: `pip install -r requirements.txt`

### Frontend won't start
- Check Node.js 18+ installed
- Delete `node_modules` and `npm install` again
- Check port 3000 is free

### Database locked error
- Close all connections
- Delete `data/*.db*` files
- Restart application

## Resources

- FastAPI Docs: https://fastapi.tiangolo.com/
- Next.js Docs: https://nextjs.org/docs
- SQLAlchemy Docs: https://docs.sqlalchemy.org/
- Tailwind CSS: https://tailwindcss.com/docs
- React Docs: https://react.dev/

## Questions?

Create an issue or discussion on GitHub for questions or clarifications.

Good luck developing! 🚀

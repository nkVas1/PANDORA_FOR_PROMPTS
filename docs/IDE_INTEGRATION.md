# 🔧 IDE Integration Guide - PANDORA for PROMPTS

Гайд по интеграции PANDORA с популярными IDE для удобной разработки и отладки.

## VS Code

### 1. Расширения

Рекомендуемые расширения для разработки:

**Python:**
```
- Pylance (ID: ms-python.vscode-pylance)
- Python (ID: ms-python.python)
- Pytest Explorer (ID: littlefoxteam.vscode-python-test-adapter)
```

**Frontend/TypeScript:**
```
- ES7+ React/Redux/React-Native snippets (ID: dsznajder.es7-react-js-snippets)
- Tailwind CSS IntelliSense (ID: bradlc.vscode-tailwindcss)
- TypeScript Vue Plugin (ID: Vue.vscode-typescript-vue-plugin)
```

**Git & Productivity:**
```
- GitLens (ID: eamodio.gitlens)
- Thunder Client (ID: rangav.vscode-thunder-client)
- REST Client (ID: humao.rest-client)
```

### 2. Конфигурация VS Code

Создайте `.vscode/settings.json`:

```json
{
  "python.defaultInterpreterPath": "${workspaceFolder}/backend/.venv/bin/python",
  "python.linting.enabled": true,
  "python.linting.pylintEnabled": true,
  "python.linting.pylintPath": "${workspaceFolder}/backend/.venv/bin/pylint",
  "python.formatting.provider": "black",
  "python.formatting.blackPath": "${workspaceFolder}/backend/.venv/bin/black",
  "[python]": {
    "editor.formatOnSave": true,
    "editor.defaultFormatter": "ms-python.python"
  },
  "[typescript]": {
    "editor.formatOnSave": true,
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  "[json]": {
    "editor.formatOnSave": true
  },
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": true
  },
  "tailwindCSS.experimental.classRegex": [
    ["clsx\\(([^)]*)\\)", "(?:'|\"|`)([^']*)(?:'|\"|`)"]
  ]
}
```

### 3. Launch Configurations

Создайте `.vscode/launch.json`:

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Backend (FastAPI)",
      "type": "python",
      "request": "launch",
      "program": "${workspaceFolder}/backend/run.py",
      "console": "integratedTerminal",
      "justMyCode": true,
      "env": {
        "PYTHONPATH": "${workspaceFolder}/backend"
      },
      "cwd": "${workspaceFolder}/backend"
    },
    {
      "name": "Backend Tests",
      "type": "python",
      "request": "launch",
      "module": "pytest",
      "console": "integratedTerminal",
      "cwd": "${workspaceFolder}/backend",
      "args": ["-v", "tests/"]
    }
  ]
}
```

### 4. Tasks

Создайте `.vscode/tasks.json`:

```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Start Application",
      "type": "shell",
      "command": "python",
      "args": ["start.py"],
      "group": {
        "kind": "test",
        "isDefault": true
      },
      "presentation": {
        "echo": true,
        "reveal": "always",
        "panel": "new",
        "focus": false
      }
    },
    {
      "label": "Install Backend Deps",
      "type": "shell",
      "command": "pip",
      "args": ["install", "-r", "backend/requirements.txt"]
    },
    {
      "label": "Install Frontend Deps",
      "type": "shell",
      "command": "npm",
      "args": ["install"],
      "options": {
        "cwd": "${workspaceFolder}/frontend"
      }
    }
  ]
}
```

### 5. Workspace Settings

Создайте `PANDORA_FOR_PROMPTS-main.code-workspace`:

```json
{
  "folders": [
    {
      "path": ".",
      "name": "Root"
    },
    {
      "path": "backend",
      "name": "Backend (FastAPI)"
    },
    {
      "path": "frontend",
      "name": "Frontend (Next.js)"
    }
  ],
  "settings": {
    "python.linting.enabled": true,
    "editor.formatOnSave": true,
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  }
}
```

Открыть: `code PANDORA_FOR_PROMPTS-main.code-workspace`

---

## PyCharm / IntelliJ IDEA

### 1. Project Setup

**File → Open:**
```
Select: PANDORA_FOR_PROMPTS-main folder
```

### 2. Python Interpreter

**Settings → Project → Python Interpreter:**
```
1. Click ⚙️
2. Add → Add Local Interpreter
3. Select: backend/.venv/bin/python
```

### 3. FastAPI Support

**Settings → Languages & Frameworks → Python → FastAPI:**
```
Enable FastAPI support
```

### 4. Run Configurations

**Run → Edit Configurations:**

```
Name: FastAPI Server
Script path: backend/run.py
Python interpreter: Project interpreter
Working directory: /backend
```

### 5. Debugging

```
Set breakpoints in backend code
F9 to debug
F8 to step
```

---

## Sublime Text 3

### 1. Packages

Install Package Control, then:

```
Ctrl+Shift+P → Install Package

- Python
- TypeScript
- Tailwind CSS Autocomplete
- REST Client
- GitGutter
```

### 2. Project File

Создайте `PANDORA.sublime-project`:

```json
{
  "folders": [
    {
      "path": ".",
      "name": "PANDORA",
      "folder_exclude_patterns": [
        "node_modules",
        "__pycache__",
        ".next",
        "dist"
      ]
    }
  ],
  "settings": {
    "python_interpreter": "./backend/.venv/bin/python",
    "translate_tabs_to_spaces": true,
    "tab_size": 2
  }
}
```

### 3. Build System

**Tools → Build System → New Build System:**

```json
{
  "cmd": ["python", "start.py"],
  "shell": true,
  "working_dir": "$project_path"
}
```

---

## Visual Studio (Windows)

### 1. Open Folder

**File → Open → Folder:**
```
Select: PANDORA_FOR_PROMPTS-main
```

### 2. Python Environment

**Tools → Python → Python Environments:**
```
1. Add Environment
2. Existing environment
3. Select: backend/.venv
```

### 3. Launch Configuration

**Debug → Start Debug:**
```
Select backend/run.py as startup file
```

---

## GitHub Codespaces (Cloud IDE)

### 1. Создание Codespace

GitHub → Code → Codespaces → Create codespace on main

### 2. Инициализация

```bash
# Inside Codespace
python start.py
```

### 3. Портосы

GitHub автоматически пробросит:
- 8000 (Backend)
- 3000 (Frontend)

### 4. Окончание работы

```bash
Ctrl+C
```

Codespace сохранит все изменения.

---

## Neovim / Vim

### 1. Конфиг

Создайте ~/.config/nvim/init.vim:

```vim
" Python
autocmd FileType python setlocal omnifunc=pythoncomplete#Complete
let g:python3_host_prog = '/path/to/backend/.venv/bin/python'

" LSP
Plug 'neovim/nvim-lspconfig'
Plug 'ms-jpq/coc-jedi'

" Treesitter
Plug 'nvim-treesitter/nvim-treesitter'
```

### 2. Запуск

```bash
cd backend
nvim app/main.py
```

### 3. Команды

```
:!python run.py           # Запуск сервера
:!pytest tests/           # Тесты
```

---

## Docker Development Container

### 1. Конфиг

Создайте `.devcontainer/devcontainer.json`:

```json
{
  "image": "python:3.9",
  "customizations": {
    "vscode": {
      "extensions": [
        "ms-python.python",
        "ms-python.vscode-pylance",
        "esbenp.prettier-vscode"
      ],
      "settings": {
        "python.defaultInterpreterPath": "/usr/local/bin/python"
      }
    }
  },
  "postCreateCommand": "pip install -r backend/requirements.txt && npm install --prefix frontend",
  "forwardPorts": [8000, 3000]
}
```

### 2. VS Code

Install Remote - Containers extension, then:

```
Ctrl+Shift+P → Remote-Containers: Reopen in Container
```

---

## EditorConfig

Создайте `.editorconfig`:

```ini
# EditorConfig helps maintain consistent coding styles for multiple developers
root = true

[*]
indent_style = space
indent_size = 2
end_of_line = lf
charset = utf-8
trim_trailing_whitespace = true
insert_final_newline = true

[*.py]
indent_size = 4
max_line_length = 88

[*.md]
trim_trailing_whitespace = false
max_line_length = off

[Makefile]
indent_style = tab
```

---

## Debugging Tips

### Backend Debugging

```python
# backend/app/main.py
import pdb; pdb.set_trace()  # Breakpoint
```

Или используйте debugger в VS Code.

### Frontend Debugging

```javascript
// frontend/components/Button.tsx
debugger;  // Breakpoint в DevTools
```

**F12 → Sources → Set Breakpoints**

### Network Debugging

Use Thunder Client или REST Client расширения:

```rest
### Get all prompts
GET http://127.0.0.1:8000/api/prompts
Authorization: Bearer YOUR_TOKEN

### Create prompt
POST http://127.0.0.1:8000/api/prompts
Content-Type: application/json

{
  "title": "Test Prompt",
  "content": "Test content"
}
```

---

## Performance Monitoring

### Backend

```python
# requirements.txt
fastapi-profiler
```

### Frontend

Chrome DevTools:
- **Performance** tab
- **Network** tab
- **Console** for errors

---

## 🎯 Рекомендуемая Setup

Для оптимальной разработки PANDORA рекомендуется:

1. **IDE**: VS Code (best experience)
2. **Extensions**: Python, TypeScript, Tailwind, GitLens
3. **Shell**: PowerShell или Bash (WSL)
4. **Git GUI**: GitKraken или Git Extensions
5. **API Testing**: Thunder Client или Postman
6. **Database**: DBeaver (для SQLite)

---

## ✅ Чек-лист Setup

- [ ] Git установлен и скофигурирован
- [ ] Python 3.9+ установлен
- [ ] Node.js 18+ установлен
- [ ] IDE выбран и установлен
- [ ] Расширения установлены
- [ ] Interpreter configured
- [ ] `.vscode` folder настроен
- [ ] Запущено `python start.py` успешно
- [ ] Frontend доступен на http://127.0.0.1:3000
- [ ] Backend доступен на http://127.0.0.1:8000

---

## 🔗 Полезные ссылки

- [VS Code Python](https://code.visualstudio.com/docs/languages/python)
- [PyCharm FastAPI](https://www.jetbrains.com/help/pycharm/fastapi.html)
- [Sublime Python](https://docs.sublimetext.io/reference/build_systems/exec.html)
- [Neovim LSP](https://neovim.io/doc/user/lsp.html)
- [Remote Containers](https://code.visualstudio.com/docs/remote/containers)

---

## 💡 Pro Tips

1. Используйте **Ctrl+P** (VS Code) для быстрого открытия файлов
2. Настройте **format on save** для автоматического форматирования
3. Используйте **ESC** для выхода из debugger
4. Комбинируйте **localhost tunneling** для удаленной отладки
5. Включайте **logging** для трейсирования проблем

---

Выбирайте IDE по вкусу и начинайте разработку! 🚀

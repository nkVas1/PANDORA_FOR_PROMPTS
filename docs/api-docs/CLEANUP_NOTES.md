# Cleanup & Organization Notes

## Структурные улучшения проекта

### Старые файлы которые нужно архивировать:

#### HTML файлы (frontend/)
- `index-backup-old.html` → archive/deprecated/
- `index_backup.html` → archive/deprecated/
- `index-v2.html` → archive/deprecated/
- `index_v2.html` → archive/deprecated/
- `advanced_features.html` → archive/deprecated/

#### Скрипты запуска (корень)
- `start.py` → archive/deprecated/
- `start_v2.py` → archive/deprecated/
- `launcher.py` → archive/deprecated/ (если start.py, то и этот)
- `build.py` → archive/deprecated/
- `build_debug.log` → archive/deprecated/logs/
- `build_final.log` → archive/deprecated/logs/
- И все остальные build*.log файлы

#### Документация (корень) - перенести в docs/
- `BUGFIX_SUMMARY.md` → docs/bugfixes/
- `BUGFIX_v1_0_3.md` → docs/bugfixes/
- `BUILD_REPORT_v2.0.md` → docs/build-reports/
- `CHANGELOG_v1.3.0.md` → docs/
- `CHANGELOG_v1_0_1.md` → docs/
- `DESIGN_VISION_v2.0.md` → docs/design/
- `PHASE2_COMPLETE.md` → docs/history/
- `PHASE3_SESSION_COMPLETE.md` → docs/history/
- `PHASE4_COMPLETION_SUMMARY.md` → docs/history/
- `PHASE4_README.md` → docs/
- `QUICK_RUN.md` → docs/
- `QUICK_START.md` → docs/
- `QUICK_START_v1_0_3.md` → docs/history/
- `QUICK_START_v2.0.md` → docs/
- `SESSION_COMPLETE_v1.3.0.md` → docs/history/
- `RESTORATION_GUIDE.md` → docs/
- `START_HERE.md` → docs/getting-started/
- `SYSTEM_RECOVERY.md` → docs/
- `TROUBLESHOOTING.md` → docs/help/
- `UPDATE_v1_0_1.md` → docs/history/
- И остальные...

#### Файлы которые можно удалить
- `*.log` файлы (build.log, rebuild.log, etc)
- `*.exe.log` файлы
- Все скрипты тестирования которые дублируют функциональность

#### Файлы для .gitignore
```
# Build artifacts
dist/
build/
PANDORA_v2.0.exe
*.spec
*.pyc
__pycache__/

# Logs
logs/
*.log

# Virtual environment
venv/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Database
*.db
.env
```

## Приоритет выполнения

1. **Сейчас (Critical)**: Архивировать старые файлы, очистить корень
2. **Следующая итерация**: Перемещение документации в docs/
3. **Потом**: Добавить тесты и CI/CD

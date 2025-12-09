# Deployment Guide - PANDORA

## 📦 Подготовка к развертыванию

### 1. Окружение

```bash
# Убедитесь что используете правильную версию Python
python --version  # Should be 3.10 or higher

# Создайте production окружение
python -m venv venv_prod
.\venv_prod\Scripts\Activate.ps1  # Windows
source venv_prod/bin/activate     # Linux/Mac
```

### 2. Зависимости

```bash
# Установите зависимости
pip install -r requirements.txt

# Проверьте что всё установилось
pip list | grep FastAPI
pip list | grep SQLAlchemy
```

### 3. Конфиг

Создайте `.env` файл:

```bash
# Backend
DATABASE_URL=postgresql://user:password@localhost:5432/pandora
LOG_LEVEL=INFO
SECRET_KEY=your-secret-key-here
JWT_ALGORITHM=HS256

# Frontend
API_BASE_URL=http://localhost:8000/api

# Telegram (опционально)
TELEGRAM_BOT_TOKEN=your-token-here
```

## 🏗️ Production Build

### Windows EXE

```bash
# Установите PyInstaller (уже в requirements.txt)
pip install pyinstaller

# Соберите exe
python build_exe_v2.py

# Проверьте что exe создан
ls -la dist/PANDORA_v2.0.exe
```

### Linux/macOS Binary

```bash
# Установите зависимости для вашей ОС
# Debian/Ubuntu:
sudo apt-get install python3-dev libgtk-3-dev

# macOS:
brew install gtk4

# Соберите binary
pyinstaller --onefile \
  --windowed \
  --icon=frontend/images/logo.png \
  --name=PANDORA \
  launcher_final.py
```

## 🗄️ Database Setup

### Development (SQLite)

```bash
# База уже создаётся автоматически
python backend/app/main.py

# Проверьте что создалась
ls -la data/
```

### Production (PostgreSQL)

```bash
# 1. Установите PostgreSQL
# Windows: Download from https://www.postgresql.org/download/windows/
# Linux: sudo apt-get install postgresql postgresql-contrib
# macOS: brew install postgresql@15

# 2. Создайте базу и пользователя
psql -U postgres -c "CREATE DATABASE pandora;"
psql -U postgres -c "CREATE USER pandora_user WITH PASSWORD 'secure_password';"
psql -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE pandora TO pandora_user;"

# 3. Запустите миграции (если используется Alembic)
alembic upgrade head

# 4. Обновите .env
DATABASE_URL=postgresql://pandora_user:secure_password@localhost:5432/pandora
```

## 🚀 Запуск приложения

### Local Development

```bash
# Terminal 1: Backend
python backend/app/main.py
# Доступно на: http://localhost:8000

# Terminal 2: Desktop App
python launcher_final.py

# Terminal 3 (optional): Tests
pytest --watch
```

### Production Server

```bash
# Установите gunicorn (WSGI server)
pip install gunicorn

# Запустите backend с несколькими workers
gunicorn \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  backend.app.main:app

# Или используйте systemd сервис (смотрите ниже)
```

### Docker

```bash
# Соберите образ
docker build -t pandora:latest .

# Запустите контейнер
docker run -d \
  --name pandora \
  -p 8000:8000 \
  -v $(pwd)/data:/app/data \
  -e DATABASE_URL=postgresql://user:pass@db:5432/pandora \
  pandora:latest

# Проверьте статус
docker logs pandora
docker ps | grep pandora
```

## 🛡️ Security Checklist

- [ ] Измените `SECRET_KEY` в .env на случайное значение
- [ ] Установите `DEBUG=False` в production
- [ ] Используйте HTTPS (SSL/TLS сертификат)
- [ ] Включите CORS только для доверенных origin
- [ ] Установите rate limiting
- [ ] Регулярно обновляйте зависимости
- [ ] Используйте strong password для БД
- [ ] Включите логирование и мониторинг
- [ ] Регулярно делайте backup БД

### HTTPS Setup

```bash
# Используйте certbot для Let's Encrypt сертификата
sudo apt-get install certbot python3-certbot-nginx

# Получите сертификат
sudo certbot certonly --standalone -d your-domain.com

# Используйте в nginx/apache конфиге
ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;
```

## 📊 Мониторинг

### Logfile Monitoring

```bash
# Смотрите логи в реальном времени
tail -f logs/app.log

# Парсируйте JSON логи
tail -f logs/app.log | python -m json.tool

# Ошибки
tail -f logs/errors.log
```

### Application Monitoring

```python
# Добавьте метрики (промежуточное ПО)
from prometheus_client import Counter, Histogram

request_count = Counter('http_requests_total', 'Total HTTP requests')
request_duration = Histogram('http_request_duration_seconds', 'HTTP request duration')

@app.middleware("http")
async def add_metrics(request, call_next):
    request_count.inc()
    # ... timing code
    return response
```

### Database Monitoring

```bash
# PostgreSQL логи
tail -f /var/log/postgresql/postgresql.log

# Проверьте размер базы
psql -U pandora_user -d pandora -c "SELECT pg_size_pretty(pg_database_size('pandora'));"

# Актуальные статистики
psql -U pandora_user -d pandora -c "SELECT * FROM pg_stat_activity;"
```

## 🔄 Continuous Deployment

### GitHub Actions

Смотрите `.github/workflows/tests.yml`:

```yaml
name: Tests & Build
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
      - run: pip install -r requirements.txt
      - run: pytest backend/tests/
      
  build-exe:
    needs: test
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
      - run: pip install -r requirements.txt
      - run: python build_exe_v2.py
      - uses: actions/upload-artifact@v3
```

### Manual Deployment Steps

```bash
# 1. Pull latest code
git pull origin main

# 2. Install dependencies
pip install -r requirements.txt --upgrade

# 3. Run migrations (if needed)
alembic upgrade head

# 4. Run tests
pytest backend/tests/

# 5. Build if exe needed
python build_exe_v2.py

# 6. Restart service
sudo systemctl restart pandora

# 7. Verify
curl http://localhost:8000/health
```

## 🐛 Troubleshooting

### Port Already in Use

```bash
# Найдите процесс использующий порт 8000
lsof -i :8000  # macOS/Linux
Get-Process | Where-Object {$_.Port -eq 8000}  # Windows

# Убейте процесс
kill -9 <PID>  # macOS/Linux
Stop-Process -Id <PID> -Force  # Windows
```

### Database Connection Error

```bash
# Проверьте что БД запущена
psql -U postgres -c "\list"  # PostgreSQL

# Проверьте DATABASE_URL в .env
# Формат: postgresql://user:password@host:port/database

# Тестируйте подключение
python -c "from sqlalchemy import create_engine; engine = create_engine(os.getenv('DATABASE_URL')); engine.connect()"
```

### Memory Issues

```bash
# Проверьте использование памяти
ps aux | grep python

# Оптимизируйте gunicorn workers
# Рекомендуется: 2-4 * CPU cores
gunicorn --workers 8 --max-requests 1000 ...
```

### Slow Queries

```bash
# PostgreSQL slow log
ALTER SYSTEM SET log_min_duration_statement = 1000;  # > 1 second
SELECT pg_reload_conf();

# Проверьте индексы
\d+ prompts  # в psql

# Добавьте индекс если нужно
CREATE INDEX idx_prompts_category ON prompts(category);
```

## 📈 Performance Optimization

### API Optimization

```python
# 1. Используйте pagination
@router.get("/api/prompts")
async def get_prompts(skip: int = 0, limit: int = 50):
    return db.query(Prompt).offset(skip).limit(limit).all()

# 2. Выбирайте только нужные поля
@router.get("/api/prompts/list")
async def get_prompts_list():
    return db.query(Prompt.id, Prompt.title).all()

# 3. Используйте кешування
from fastapi_cache2 import FastAPICache2
@cached(namespace="prompts", expire=300)  # 5 min cache
async def get_prompts():
    ...
```

### Database Optimization

```python
# 1. Добавьте индексы
class Prompt(Base):
    __table_args__ = (
        Index('idx_title', 'title'),
        Index('idx_category', 'category'),
        Index('idx_created_at', 'created_at'),
    )

# 2. Используйте connection pooling
engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=10,
    max_overflow=20,
)

# 3. Оптимизируйте запросы
# BAD: N+1 queries
for prompt in db.query(Prompt).all():
    for tag in prompt.tags:  # БД запрос для каждого промпта!
        pass

# GOOD: Eager loading
db.query(Prompt).options(joinedload(Prompt.tags)).all()
```

## 🔐 Backup & Recovery

### Автоматический backup

```bash
# Cron job для ежедневного backup
# Добавьте в crontab (crontab -e)
0 2 * * * pg_dump pandora > /backups/pandora_$(date +\%Y\%m\%d).sql

# Или используйте специализированный инструмент
pip install pgbackups
pgbackups schedule --database-url=$DATABASE_URL
```

### Restore из backup

```bash
# PostgreSQL restore
psql pandora < /backups/pandora_20240101.sql

# Или с pg_restore (для binary format)
pg_restore -d pandora /backups/pandora_20240101.dump
```

## 📋 Systemd Service (Linux)

Создайте файл `/etc/systemd/system/pandora.service`:

```ini
[Unit]
Description=PANDORA Application
After=network.target postgresql.service

[Service]
Type=notify
User=pandora
WorkingDirectory=/home/pandora/PANDORA_FOR_PROMPTS
Environment="PATH=/home/pandora/venv_prod/bin"
Environment="DATABASE_URL=postgresql://pandora_user:password@localhost/pandora"
ExecStart=/home/pandora/venv_prod/bin/gunicorn \
    --workers 4 \
    --bind 127.0.0.1:8000 \
    backend.app.main:app
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Активируйте:

```bash
sudo systemctl enable pandora
sudo systemctl start pandora
sudo systemctl status pandora
```

## 🚢 Nginx Configuration

Конфиг для Nginx в `/etc/nginx/sites-available/pandora`:

```nginx
upstream pandora_app {
    server 127.0.0.1:8000;
}

server {
    listen 80;
    server_name pandora.example.com;

    client_max_body_size 10M;

    location / {
        proxy_pass http://pandora_app;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /home/pandora/PANDORA_FOR_PROMPTS/frontend/;
        expires 30d;
    }
}
```

Активируйте:

```bash
sudo ln -s /etc/nginx/sites-available/pandora /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

## ✅ Deployment Checklist

- [ ] Все тесты проходят
- [ ] .env файл создан с production значениями
- [ ] Database создана и migrations применены
- [ ] Логирование настроено
- [ ] SSL сертификат установлен
- [ ] Backup система настроена
- [ ] Мониторинг активирован
- [ ] Rate limiting включен
- [ ] CORS правильно настроен
- [ ] Healthcheck endpoint работает
- [ ] Логи проверены
- [ ] Performance тесты пройдены

---

**Последнее обновление**: 2024-12-20  
**Версия**: 2.0  
**Совместимость**: Python 3.10+, PostgreSQL 12+, nginx 1.18+

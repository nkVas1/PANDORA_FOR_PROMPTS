from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse, PlainTextResponse
from pathlib import Path
from app.config import settings
from app.api.routes import router
import threading
import os

# Database initialization flag
_db_initialized = False
_db_init_lock = threading.Lock()

# Create FastAPI app (database will be initialized on first request)
app = FastAPI(
    title=settings.API_TITLE,
    version=settings.API_VERSION,
    description="Professional prompt management system with auto-tagging and project tracking",
    docs_url="/docs",
    openapi_url="/openapi.json"
)

# Add initialization middleware
@app.middleware("http")
async def init_db_middleware(request: Request, call_next):
    """Initialize database on first request"""
    global _db_initialized
    
    if not _db_initialized:
        with _db_init_lock:
            if not _db_initialized:
                try:
                    from app.services.db_initializer import DatabaseInitializer
                    DatabaseInitializer.init_db()
                    _db_initialized = True
                except Exception as e:
                    print(f"[DB] Initialization error: {e}")
    
    response = await call_next(request)
    return response

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For local development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(router)

# Mount static files for frontend
import sys


def resolve_frontend_dir() -> Path:
    """Resolve frontend directory in both dev and frozen (PyInstaller) modes."""
    # If running as PyInstaller bundle, try _MEIPASS first
    if getattr(sys, 'frozen', False):
        meipass = getattr(sys, '_MEIPASS', None)
        if meipass:
            candidate = Path(meipass) / "frontend"
            if candidate.exists():
                return candidate

        # Fallback: try relative to executable
        candidate = Path(sys.executable).parent / "frontend"
        if candidate.exists():
            return candidate

    # Development mode: assume project layout
    candidate = Path(__file__).parent.parent.parent / "frontend"
    return candidate


frontend_dir = resolve_frontend_dir()
print(f"[STATIC] Frontend directory resolved to: {frontend_dir}")
print(f"[STATIC] Frontend dir exists: {frontend_dir.exists()}")

# Mount static directories FIRST (before catch-all route)
# Mount CSS
css_dir = frontend_dir / "css"
if css_dir.exists():
    try:
        app.mount("/css", StaticFiles(directory=str(css_dir)), name="css")
        print(f"[STATIC] ✓ Mounted /css → {css_dir}")
    except Exception as e:
        print(f"[STATIC] Failed to mount /css: {e}")
else:
    print(f"[STATIC] CSS dir not found at {css_dir}")

# Mount JS
js_dir = frontend_dir / "js"
if js_dir.exists():
    try:
        app.mount("/js", StaticFiles(directory=str(js_dir)), name="js")
        print(f"[STATIC] ✓ Mounted /js → {js_dir}")
    except Exception as e:
        print(f"[STATIC] Failed to mount /js: {e}")
else:
    print(f"[STATIC] JS dir not found at {js_dir}")

# Mount static files directory if it exists
static_dir = frontend_dir / "static"
if static_dir.exists():
    try:
        app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")
        print(f"[STATIC] ✓ Mounted /static → {static_dir}")
    except Exception as e:
        print(f"[STATIC] Failed to mount /static: {e}")

# Mount styles directory if it exists
styles_dir = frontend_dir / "styles"
if styles_dir.exists():
    try:
        app.mount("/styles", StaticFiles(directory=str(styles_dir)), name="styles")
        print(f"[STATIC] ✓ Mounted /styles → {styles_dir}")
    except Exception as e:
        print(f"[STATIC] Failed to mount /styles: {e}")

# ROOT route - serve index.html
@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve main HTML page"""
    index_path = frontend_dir / "index.html"
    if index_path.exists():
        try:
            content = index_path.read_text(encoding='utf-8')
            print(f"[STATIC] ✓ Serving index.html from {index_path}")
            return content
        except Exception as e:
            print(f"[STATIC] Error reading index.html: {e}")
            return get_index_html_fallback()
    else:
        print(f"[STATIC] index.html not found at {index_path}")
        return get_index_html_fallback()

# Catch-all for individual static files (MUST BE AFTER api/router and root route)
@app.get("/{file_path:path}", response_class=HTMLResponse)
async def serve_static(file_path: str):
    """Serve static files from frontend directory (catch-all for non-API routes)"""
    try:
        # Skip if this looks like an API endpoint (shouldn't happen but safety measure)
        if file_path.startswith(('api/', 'docs', 'openapi.json', 'health')):
            return PlainTextResponse("Not found", status_code=404)
        
        static_path = frontend_dir / file_path

        # Security check: prevent directory traversal
        try:
            static_resolved = static_path.resolve()
            frontend_resolved = frontend_dir.resolve()
            if not str(static_resolved).startswith(str(frontend_resolved)):
                print(f"[STATIC] 🚫 Security violation: {static_path}")
                return PlainTextResponse("Forbidden", status_code=403)
        except Exception as e:
            print(f"[STATIC] Path resolution error: {e}")
            return PlainTextResponse("Invalid path", status_code=400)

        # Check if file exists
        if static_path.exists() and static_path.is_file():
            print(f"[STATIC] ✓ Serving {file_path}")
            return FileResponse(static_path)

        # If not found, try to serve index.html for SPA routing
        # This allows React Router / Vue Router to handle the route client-side
        index_path = frontend_dir / "index.html"
        if index_path.exists():
            print(f"[STATIC] Route not found ({file_path}), serving index.html for SPA routing")
            try:
                return index_path.read_text(encoding='utf-8')
            except Exception as e:
                print(f"[STATIC] Error serving fallback index.html: {e}")
                return get_index_html_fallback()

        # Helpful debug: log the attempted path
        print(f"[STATIC] ✗ Not found: {static_path} (requested: {file_path})")
        return PlainTextResponse("Not found", status_code=404)
    except Exception as e:
        print(f"[STATIC] Error serving {file_path}: {e}")
        return PlainTextResponse("Internal error", status_code=500)


def get_index_html_fallback() -> str:
    """Get fallback HTML content if file doesn't exist"""
    return """
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>PANDORA - Prompt Manager</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                display: flex;
                justify-content: center;
                align-items: center;
                color: #333;
            }
            .container {
                background: white;
                border-radius: 16px;
                box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
                padding: 60px 40px;
                max-width: 600px;
                text-align: center;
                animation: slideUp 0.6s ease-out;
            }
            @keyframes slideUp {
                from {
                    opacity: 0;
                    transform: translateY(30px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }
            h1 {
                font-size: 2.5em;
                margin-bottom: 10px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
            }
            .subtitle {
                font-size: 1.1em;
                color: #666;
                margin-bottom: 40px;
            }
            .status {
                background: #f0f4ff;
                border-left: 4px solid #667eea;
                padding: 20px;
                margin-bottom: 30px;
                border-radius: 8px;
                text-align: left;
            }
            .status-item {
                display: flex;
                align-items: center;
                margin: 10px 0;
                font-size: 0.95em;
            }
            .status-icon {
                font-size: 1.3em;
                margin-right: 12px;
            }
            .api-link {
                display: inline-block;
                margin-top: 30px;
                padding: 12px 24px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                text-decoration: none;
                border-radius: 8px;
                font-weight: 600;
                transition: transform 0.3s, box-shadow 0.3s;
                box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
            }
            .api-link:hover {
                transform: translateY(-2px);
                box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
            }
            .features {
                margin-top: 40px;
                text-align: left;
                background: #f9f9f9;
                padding: 20px;
                border-radius: 8px;
            }
            .features h3 {
                margin-bottom: 15px;
                color: #667eea;
            }
            .feature-list {
                list-style: none;
            }
            .feature-list li {
                padding: 8px 0;
                color: #555;
            }
            .feature-list li:before {
                content: "✓ ";
                color: #764ba2;
                font-weight: bold;
                margin-right: 8px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🚀 PANDORA</h1>
            <p class="subtitle">Professional Prompt Management System</p>
            
            <div class="status">
                <div class="status-item">
                    <span class="status-icon">🟢</span>
                    <span><strong>Backend Status:</strong> Running</span>
                </div>
                <div class="status-item">
                    <span class="status-icon">📦</span>
                    <span><strong>API Server:</strong> http://127.0.0.1:8000</span>
                </div>
                <div class="status-item">
                    <span class="status-icon">📚</span>
                    <span><strong>API Documentation:</strong> Available at /docs</span>
                </div>
            </div>
            
            <div class="features">
                <h3>Features</h3>
                <ul class="feature-list">
                    <li>Professional Prompt Management</li>
                    <li>Auto-Tagging System</li>
                    <li>Project Tracking</li>
                    <li>REST API Integration</li>
                    <li>Real-time Synchronization</li>
                    <li>Advanced Search & Filter</li>
                </ul>
            </div>
            
            <a href="/docs" class="api-link">📖 API Documentation</a>
        </div>
    </body>
    </html>
    """


@app.get("/health")
async def health_check():
    """Health check endpoint returning DB and basic stats."""
    try:
        from app.db.database import DATA_DIR
        from app.db.database import SessionLocal
        from app.db.models import Prompt, Tag

        db_file = DATA_DIR / 'pandora.db'
        info = {
            'status': 'healthy',
            'db_path': str(db_file),
            'db_exists': db_file.exists(),
            'db_size': db_file.stat().st_size if db_file.exists() else 0,
        }

        # Try to get counts if DB is available
        if db_file.exists():
            db = SessionLocal()
            try:
                info['total_prompts'] = db.query(Prompt).count()
                info['total_tags'] = db.query(Tag).count()
            except Exception as e:
                info['db_error'] = str(e)
            finally:
                db.close()

        return info
    except Exception as e:
        print(f"[HEALTH] Error building health info: {e}")
        return {"status": "unhealthy", "error": str(e)}


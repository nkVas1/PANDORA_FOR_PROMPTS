from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pathlib import Path
from app.config import settings
from app.api.routes import router

# Create FastAPI app
app = FastAPI(
    title=settings.API_TITLE,
    version=settings.API_VERSION,
    description="Professional prompt management system with auto-tagging and project tracking",
    docs_url="/docs",
    openapi_url="/openapi.json"
)

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


@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve main HTML page"""
    return get_index_html()


def get_index_html() -> str:
    """Get HTML content from file or return default"""
    html_path = Path(__file__).parent.parent.parent / "frontend" / "index.html"
    if html_path.exists():
        return html_path.read_text(encoding='utf-8')
    
    # Fallback HTML if file doesn't exist
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
    """Health check endpoint"""
    return {"status": "healthy"}


import os
from pathlib import Path
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Настройки приложения"""
    
    # API
    API_TITLE: str = "PANDORA Prompts Manager API"
    API_VERSION: str = "1.0.0"
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    
    # Server
    HOST: str = os.getenv("HOST", "127.0.0.1")
    PORT: int = int(os.getenv("PORT", "8000"))
    API_HOST: str = os.getenv("API_HOST", "127.0.0.1")
    API_PORT: int = int(os.getenv("API_PORT", "8000"))
    
    # Database
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", 
        f"sqlite:///{Path(__file__).parent.parent.parent / 'data' / 'pandora.db'}"
    )
    
    # Paths
    DATA_DIR: Path = Path(__file__).parent.parent.parent / "data"
    PROMPTS_DIR: Path = DATA_DIR / "prompts"
    IMPORTS_DIR: Path = DATA_DIR / "imports"
    PROJECTS_DIR: Path = DATA_DIR / "projects"
    
    # AI Model for auto-tagging
    TAGGING_MODEL: str = os.getenv("TAGGING_MODEL", "cpu")  # or "gpu"
    MAX_TAGS_PER_PROMPT: int = 10
    MIN_TAG_CONFIDENCE: float = 0.5
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"  # Игнорируем дополнительные переменные из .env


settings = Settings()

# Create required directories
settings.DATA_DIR.mkdir(exist_ok=True)
settings.PROMPTS_DIR.mkdir(exist_ok=True)
settings.IMPORTS_DIR.mkdir(exist_ok=True)
settings.PROJECTS_DIR.mkdir(exist_ok=True)

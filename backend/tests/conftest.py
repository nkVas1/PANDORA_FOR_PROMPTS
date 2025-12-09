"""
Pytest configuration and fixtures for PANDORA tests
"""

import pytest
import tempfile
from pathlib import Path
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Импортируем app и models
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from backend.app.main import app
from backend.app.database import Base, get_db


@pytest.fixture(scope="session")
def test_db():
    """Создаёт временную БД для тестов"""
    # Используем SQLite в памяти для быстрых тестов
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False}
    )
    
    # Создаём все таблицы
    Base.metadata.create_all(bind=engine)
    
    return engine


@pytest.fixture(scope="function")
def db_session(test_db):
    """Создаёт новую сессию БД для каждого теста"""
    connection = test_db.connect()
    transaction = connection.begin()
    
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_db)
    session = SessionLocal(bind=connection)
    
    yield session
    
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
def client(db_session):
    """Создаёт TestClient с тестовой БД"""
    def override_get_db():
        yield db_session
    
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as test_client:
        yield test_client
    
    app.dependency_overrides.clear()


@pytest.fixture
def sample_prompt_data():
    """Пример данных промпта для тестов"""
    return {
        "title": "Test Prompt",
        "content": "This is a test prompt content",
        "category": "general",
        "tags": []
    }


@pytest.fixture
def sample_project_data():
    """Пример данных проекта для тестов"""
    return {
        "name": "Test Project",
        "description": "A test project",
        "status": "active"
    }

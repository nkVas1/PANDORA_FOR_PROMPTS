# -*- coding: utf-8 -*-
"""
Конфигурация базы данных и сессия SQLAlchemy.
"""

import os
import sys
import shutil
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool

# Определяем путь к БД
# Для exe ищем data в папке с exe, для разработки - в корне проекта
if getattr(sys, 'frozen', False):
    # Запущено как exe (PyInstaller). Используем _MEIPASS при его наличии,
    # иначе берем папку с исполняемым файлом.
    base_candidate = getattr(sys, '_MEIPASS', None)
    if base_candidate:
        BASE_DIR = Path(base_candidate)
    else:
        BASE_DIR = Path(sys.executable).parent
else:
    # Разработка - идем вверх на 4 уровня
    BASE_DIR = Path(__file__).parent.parent.parent.parent

DATA_DIR = BASE_DIR / "data"

# Логируем для отладки
try:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
except Exception as e:
    print(f"[DB] Failed to create data dir at {DATA_DIR}: {e}")

# Правильный путь для SQLite URL
db_path = DATA_DIR / 'pandora.db'
DATABASE_URL = f"sqlite:///{str(db_path).replace(chr(92), '/')}"

def _attempt_copy_prebuilt_db(target_path: Path) -> bool:
    """Попытаться найти и скопировать предсозданную базу данных в целевой путь.
    Возвращает True если скопировали.
    """
    pre_built_sources = []

    # Стандартные места в исходном проекте
    pre_built_sources.append(BASE_DIR / "frontend" / "pandora.db")
    pre_built_sources.append(Path(__file__).parent.parent.parent / "frontend" / "pandora.db")
    pre_built_sources.append(Path(__file__).parent.parent.parent.parent / "frontend" / "pandora.db")

    # Если упаковано PyInstaller, _MEIPASS может содержать файлы
    if getattr(sys, 'frozen', False):
        meipass = getattr(sys, '_MEIPASS', None)
        if meipass:
            pre_built_sources.append(Path(meipass) / "frontend" / "pandora.db")
            pre_built_sources.append(Path(meipass) / "data" / "pandora.db")

    # Также проверяем соседние места (dist layout)
    pre_built_sources.append(Path(__file__).parent.parent / "frontend" / "pandora.db")

    tried = set()
    for source in pre_built_sources:
        try:
            if not source or source in tried:
                continue
            tried.add(source)
            if source.exists() and source.is_file():
                size = source.stat().st_size
                if size < 1024:  # слишком маленький, пропускаем
                    continue
                try:
                    target_path.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(source, target_path)
                    print(f"[DB] Copied pre-built database from {source} -> {target_path} (size={size})")
                    return True
                except Exception as e:
                    print(f"[DB] Failed to copy from {source}: {e}")
        except Exception:
            continue

    return False


# Если БД не существует, копируем готовую (если она есть в распределении)
if not db_path.exists():
    try:
        copied = _attempt_copy_prebuilt_db(db_path)
        if not copied:
            print(f"[DB] No pre-built database found for target {db_path}")
    except Exception as e:
        print(f"[DB] Error while attempting to copy pre-built DB: {e}")

# Создаем engine с правильными параметрами для SQLite
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
    echo=False
)

# Создаем SessionLocal factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Session:
    """Dependency для получения сессии БД"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

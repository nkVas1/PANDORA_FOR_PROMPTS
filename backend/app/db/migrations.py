#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Database migrations для добавления новых полей к существующей БД
"""

import sqlite3
from pathlib import Path
from datetime import datetime


def get_db_path():
    """Получить путь к БД"""
    # Пытаемся найти БД в разных местах
    possible_paths = [
        Path(__file__).parent.parent.parent.parent / "data" / "pandora.db",
        Path(__file__).parent.parent.parent / "frontend" / "pandora.db",
        Path(__file__).parent.parent.parent.parent / "frontend" / "pandora.db",
    ]
    
    for path in possible_paths:
        if path.exists():
            return path
    
    # По умолчанию
    return Path(__file__).parent.parent.parent.parent / "data" / "pandora.db"


def add_column_if_not_exists(conn, table: str, column: str, column_type: str):
    """Добавить колонку в таблицу если её нет"""
    cursor = conn.cursor()
    
    # Проверяем есть ли колонка
    cursor.execute(f"PRAGMA table_info({table})")
    columns = {row[1] for row in cursor.fetchall()}
    
    if column not in columns:
        print(f"  Adding column: {table}.{column} ({column_type})")
        cursor.execute(f"ALTER TABLE {table} ADD COLUMN {column} {column_type}")
        conn.commit()
        return True
    else:
        print(f"  Column already exists: {table}.{column}")
        return False


def migrate_database():
    """Миграция БД: добавление новых полей для расширенных метаданных"""
    db_path = get_db_path()
    
    if not db_path.exists():
        print(f"Database not found at {db_path}")
        return False
    
    print(f"[Migration] Connecting to database: {db_path}")
    
    try:
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        
        print("[Migration] Adding new columns to prompts table...")
        
        # Новые колонки с их типами
        new_columns = [
            ("subcategory", "VARCHAR(50)"),
            ("emoji", "VARCHAR(10)"),
            ("difficulty", "VARCHAR(50) DEFAULT 'intermediate'"),
            ("context_window", "VARCHAR(50)"),
            ("models", "TEXT"),  # JSON array
            ("use_cases", "TEXT"),  # JSON array
            ("examples", "TEXT"),  # JSON array
            ("changelog", "TEXT"),
            ("rating", "REAL DEFAULT 0.0"),
            ("author", "VARCHAR(255)"),
            ("author_url", "VARCHAR(500)"),
            ("keywords", "TEXT"),  # JSON array
            ("is_featured", "BOOLEAN DEFAULT 0"),
            ("is_experimental", "BOOLEAN DEFAULT 0"),
        ]
        
        for col_name, col_type in new_columns:
            add_column_if_not_exists(conn, "prompts", col_name, col_type)
        
        # Обновляем ячейки с default значениями где они NULL
        print("[Migration] Updating NULL values with defaults...")
        updates = [
            ("UPDATE prompts SET difficulty = 'intermediate' WHERE difficulty IS NULL", "difficulty"),
            ("UPDATE prompts SET rating = 0.0 WHERE rating IS NULL", "rating"),
            ("UPDATE prompts SET is_featured = 0 WHERE is_featured IS NULL", "is_featured"),
            ("UPDATE prompts SET is_experimental = 0 WHERE is_experimental IS NULL", "is_experimental"),
        ]
        
        for update_sql, field_name in updates:
            try:
                cursor.execute(update_sql)
                conn.commit()
                print(f"  Updated {field_name}")
            except Exception as e:
                print(f"  Warning: Could not update {field_name}: {e}")
        
        conn.close()
        print("[Migration] ✓ Database migration completed successfully!")
        return True
        
    except Exception as e:
        print(f"[Migration] ✗ Error during migration: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    migrate_database()

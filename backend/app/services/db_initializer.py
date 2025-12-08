# -*- coding: utf-8 -*-
"""
Сервис инициализации базы данных и импорта промптов при запуске.
"""

import os
import json
from pathlib import Path
from typing import Optional
from sqlalchemy import inspect
from sqlalchemy.orm import Session

from app.db.models import Prompt, Tag, Base
from app.db.database import engine
from app.services.references_importer import ReferencesImporter


class DatabaseInitializer:
    """Инициализирует БД и импортирует все промпты"""
    
    @staticmethod
    def init_db():
        """Инициализирует БД и создает таблицы если их нет"""
        print("[DB] Initializing database...")
        
        # Создаем таблицы если их нет
        Base.metadata.create_all(bind=engine)
        
        # Проверяем, пустая ли БД
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        
        if 'prompts' in tables:
            from app.db.database import SessionLocal
            db = SessionLocal()
            prompt_count = db.query(Prompt).count()
            db.close()
            
            if prompt_count > 0:
                print(f"[DB] Database already initialized ({prompt_count} prompts)")
                return

        # Попытка скопировать предсозданную базу данных, если она присутствует
        try:
            from app.db.database import _attempt_copy_prebuilt_db, DATA_DIR
            target_db = DATA_DIR / 'pandora.db'
            if not target_db.exists():
                copied = False
                try:
                    copied = _attempt_copy_prebuilt_db(target_db)
                except Exception as e:
                    print(f"[DB] Error during prebuilt DB copy attempt: {e}")

                if copied:
                    print("[DB] Prebuilt database copied, skipping import.")
                    return
        except Exception:
            # Если импорт не удался или функции нет, продолжаем как обычно
            pass

        print("[DB] Starting import from references...")
        DatabaseInitializer.import_references_prompts()
    
    @staticmethod
    def import_references_prompts():
        """Импортирует все промпты из references в БД"""
        from app.db.database import SessionLocal
        
        # Получаем все промпты из references
        prompts_data, stats = ReferencesImporter.import_all_references()
        
        if not prompts_data:
            print("[DB] Failed to import prompts")
            return
        
        # Сохраняем в БД
        db = SessionLocal()
        try:
            added = 0
            skipped = 0
            
            for prompt_data in prompts_data:
                # Проверяем, есть ли уже такой промпт
                existing = db.query(Prompt).filter(
                    Prompt.title == prompt_data['title'],
                    Prompt.imported_from == prompt_data.get('imported_from', '')
                ).first()
                
                if existing:
                    skipped += 1
                    continue
                
                # Создаем теги если их нет
                tags = []
                for tag_name in prompt_data.get('tags', []):
                    if tag_name:
                        tag = db.query(Tag).filter(Tag.name == tag_name).first()
                        if not tag:
                            tag = Tag(name=tag_name)
                            db.add(tag)
                            db.flush()
                        tags.append(tag)
                
                # Создаем промпт
                prompt = Prompt(
                    title=prompt_data['title'][:255],
                    content=prompt_data['content'],
                    description=prompt_data.get('description', '')[:500],
                    category=prompt_data.get('category', 'development'),
                    imported_from=prompt_data.get('imported_from', 'references'),
                    tags=tags
                )
                
                db.add(prompt)
                added += 1
                
                # Коммитим батчами для производительности
                if added % 50 == 0:
                    db.commit()
                    print(f"  [DB] Added {added} prompts...")
            
            # Финальный коммит
            db.commit()
            
            print(f"\n[DB] Import completed!")
            print(f"   Added: {added}")
            print(f"   Skipped: {skipped}")
            
            # Выводим статистику по категориям
            category_stats = {}
            prompts = db.query(Prompt).all()
            for prompt in prompts:
                category_stats[prompt.category] = category_stats.get(prompt.category, 0) + 1
            
            print(f"\n[DB] Statistics by category:")
            for category in sorted(category_stats.keys()):
                count = category_stats[category]
                print(f"   {category:20} {count:4} prompts")
        
        except Exception as e:
            db.rollback()
            print(f"[DB ERROR] Import failed: {e}")
        finally:
            db.close()
    
    @staticmethod
    def clear_and_reimport():
        """Очищает БД и заново импортирует промпты"""
        from app.db.database import SessionLocal
        
        print("[DB] Clearing database...")
        db = SessionLocal()
        
        try:
            db.query(Prompt).delete()
            db.query(Tag).delete()
            db.commit()
            print("[DB] Database cleared")
            
            DatabaseInitializer.import_references_prompts()
        except Exception as e:
            db.rollback()
            print(f"[DB ERROR] Clear failed: {e}")
        finally:
            db.close()

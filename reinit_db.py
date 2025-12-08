#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Reinitialize database with all prompts from references folder
"""

import sys
import os

# Force UTF-8 encoding on Windows
if sys.platform == 'win32':
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    if sys.stdout:
        try:
            sys.stdout.reconfigure(encoding='utf-8')
        except:
            pass

sys.path.insert(0, 'backend')

from pathlib import Path
from app.db.database import engine, SessionLocal
from app.db.models import Base, Prompt, Project, Tag
from app.services.db_initializer import DatabaseInitializer

print("[DB] Initializing database...")

# Initialize database and import prompts
DatabaseInitializer.init_db()

# Verify
with SessionLocal() as db:
    total_prompts = db.query(Prompt).count()
    total_tags = db.query(Tag).count()
    total_projects = db.query(Project).count()
    
    print("\n[STATS] Database statistics:")
    print(f"  Prompts: {total_prompts}")
    print(f"  Tags: {total_tags}")
    print(f"  Projects: {total_projects}")
    
    if total_prompts > 0:
        print(f"\n[OK] Database initialized successfully!")
    else:
        print(f"\n[WARNING] No prompts imported!")


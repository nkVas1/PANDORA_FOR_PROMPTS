#!/usr/bin/env python
# -*- coding: utf-8 -*-

from backend.app.services.db_initializer import DatabaseInitializer

print("🔧 Инициализирую БД...")
DatabaseInitializer.init_db()

#!/usr/bin/env python
# -*- coding: utf-8 -*-

from backend.app.services.references_importer import ReferencesImporter

print("🔍 Проверяю импорт промптов...")
prompts, stats = ReferencesImporter.import_all_references()

print(f"\n📊 Статистика:")
print(f"Total prompts: {len(prompts)}")
print(f"\nStats по источникам:")
for source, count in sorted(stats.items()):
    print(f"  {source}: {count}")

if prompts:
    print(f"\n✅ Примеры промптов:")
    for i, p in enumerate(prompts[:5], 1):
        print(f"  {i}. {p.get('title', 'N/A')} [{p.get('category', 'N/A')}]")
else:
    print("\n❌ Промпты не найдены!")
    
    # Проверим структуру
    import os
    from pathlib import Path
    ref_dir = ReferencesImporter.find_references_dir()
    print(f"\n🔍 Проверяю структуру в {ref_dir}:")
    if ref_dir.exists():
        for item in os.listdir(ref_dir):
            item_path = ref_dir / item
            print(f"  {'📁' if os.path.isdir(item_path) else '📄'} {item}")

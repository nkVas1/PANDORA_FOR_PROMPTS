import sqlite3

db_path = 'data/pandora.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Счёт промптов
cursor.execute('SELECT COUNT(*) FROM prompts')
count = cursor.fetchone()[0]
print(f"📊 ВСЕГО ПРОМПТОВ В БД: {count}")

# Счёт по категориям
print("\n📂 ПРОМПТЫ ПО КАТЕГОРИЯМ:")
cursor.execute('SELECT category, COUNT(*) as cnt FROM prompts GROUP BY category ORDER BY cnt DESC')
categories = cursor.fetchall()
for category, cnt in categories:
    print(f"   {category}: {cnt}")

# Источники
print("\n📚 ПРОМПТЫ ПО ИСТОЧНИКАМ:")
cursor.execute('SELECT imported_from, COUNT(*) as cnt FROM prompts GROUP BY imported_from ORDER BY cnt DESC')
sources = cursor.fetchall()
for source, cnt in sources:
    print(f"   {source}: {cnt}")

# Примеры промптов
print("\n📝 ПРИМЕРЫ ПРОМПТОВ:")
cursor.execute('SELECT title, category FROM prompts LIMIT 10')
samples = cursor.fetchall()
for i, (title, category) in enumerate(samples, 1):
    print(f"   {i}. {title[:50]}... [{category}]")

conn.close()

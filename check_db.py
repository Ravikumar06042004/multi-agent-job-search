import sqlite3
import os

db_paths = ["jobs.db", "data/jobs.db"]

for path in db_paths:
    print(f"Checking: {path}")
    if os.path.exists(path):
        conn = sqlite3.connect(path)
        cursor = conn.cursor()

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()

        print("Tables:", tables)

        conn.close()
    else:
        print("Database not found")

    print("-" * 40)
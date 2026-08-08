import sqlite3
import os

DB_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "data",
    "jobs.db"
)

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

try:
    cursor.execute(
        "ALTER TABLE jobs ADD COLUMN description TEXT"
    )
    print("description column added.")
except sqlite3.OperationalError:
    print("description column already exists.")

conn.commit()
conn.close()
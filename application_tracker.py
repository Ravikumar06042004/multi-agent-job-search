import sqlite3
from datetime import datetime

DB_PATH = "data/jobs.db"

def create_application_table():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company TEXT,
            role TEXT,
            applied_date TEXT,
            status TEXT
        )
        """
    )

    conn.commit()
    conn.close()

def add_application(company, role, status="Applied"):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO applications (company, role, applied_date, status)
        VALUES (?, ?, ?, ?)
        """,
        (company, role, datetime.now().strftime("%Y-%m-%d"), status),
    )

    conn.commit()
    conn.close()

def get_applications():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT company, role, applied_date, status
        FROM applications
        ORDER BY applied_date DESC
        """
    )

    rows = cursor.fetchall()
    conn.close()

    return rows

if __name__ == "__main__":
    create_application_table()

    add_application(
        "BlueSprings",
        "AI Engineer",
        "Applied"
    )

    apps = get_applications()

    for app in apps:
        print(app)
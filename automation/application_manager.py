import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "jobs.db")


def get_connection():
    return sqlite3.connect(DB_PATH)


def initialize():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            job_id INTEGER UNIQUE,
            company TEXT,
            role TEXT,
            resume_path TEXT,
            status TEXT,
            applied_at TEXT,
            notes TEXT
        )
        """
    )

    conn.commit()
    conn.close()


def populate_from_jobs():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, company, role, resume_path
        FROM jobs
        WHERE match_score >= 40
        ORDER BY match_score DESC
        LIMIT 10
        """
    )

    jobs = cursor.fetchall()

    for job_id, company, role, resume_path in jobs:
        cursor.execute(
            """
            INSERT OR IGNORE INTO applications
            (job_id, company, role, resume_path, status)
            VALUES (?, ?, ?, ?, 'Ready')
            """,
            (job_id, company, role, resume_path)
        )

    conn.commit()
    conn.close()


def summary():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM applications WHERE status='Ready'")
    ready = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM applications WHERE status='Applied'")
    applied = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM applications WHERE status='Interview'")
    interview = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM applications WHERE status='Offer'")
    offer = cursor.fetchone()[0]

    conn.close()

    return {
        "Ready": ready,
        "Applied": applied,
        "Interview": interview,
        "Offer": offer
    }


def list_applications():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT company, role, status
        FROM applications
        ORDER BY id DESC
        """
    )

    rows = cursor.fetchall()
    conn.close()

    return rows


if __name__ == "__main__":
    initialize()
    populate_from_jobs()
    print("Application manager initialized.")
    print(summary())
    print(list_applications())
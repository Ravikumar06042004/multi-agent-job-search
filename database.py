import sqlite3

DB_PATH = "data/jobs.db"


def create_database():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            job_id TEXT UNIQUE,
            company TEXT,
            role TEXT,
            location TEXT,
            skills TEXT,
            experience TEXT,
            match_score REAL,
            resume_path TEXT
        )
        """
    )

    conn.commit()
    conn.close()

    print("Database created successfully!")


def save_job(job_id, company, role, location, skills, experience, match_score, resume_path):

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT OR IGNORE INTO jobs
        (
            job_id,
            company,
            role,
            location,
            skills,
            experience,
            match_score,
            resume_path
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            job_id,
            company,
            role,
            location,
            ", ".join(skills),
            experience,
            match_score,
            resume_path,
        ),
    )

    conn.commit()
    conn.close()


if __name__ == "__main__":
    create_database()
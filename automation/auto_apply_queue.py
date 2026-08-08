import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "jobs.db")


def queue_jobs():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, company, role, resume_path
        FROM jobs
        WHERE resume_path IS NOT NULL
        """
    )

    jobs = cursor.fetchall()

    queued = 0

    for job_id, company, role, resume_path in jobs:
        cursor.execute(
            "SELECT id FROM applications WHERE job_id = ?",
            (job_id,)
        )

        exists = cursor.fetchone()

        if not exists:
            cursor.execute(
                """
                INSERT INTO applications
                (job_id, company, role, resume_path, status, applied_at, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    job_id,
                    company,
                    role,
                    resume_path,
                    "Ready",
                    None,
                    ""
                )
            )

            queued += 1

    conn.commit()
    conn.close()

    print(f"Queued {queued} jobs for application.")


if __name__ == "__main__":
    queue_jobs()
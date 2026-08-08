import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "jobs.db")

VALID_STATUSES = [
    "Ready",
    "Applied",
    "Interview",
    "Offer",
    "Rejected"
]


def ensure_status_column():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        cursor.execute("ALTER TABLE jobs ADD COLUMN application_status TEXT DEFAULT 'Ready'")
    except sqlite3.OperationalError:
        pass

    conn.commit()
    conn.close()


def mark_status(job_id, status):
    if status not in VALID_STATUSES:
        print("Invalid status.")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE jobs SET application_status=? WHERE id=?",
        (status, job_id)
    )

    conn.commit()
    conn.close()

    print(f"Job {job_id} updated to {status}.")


def show_summary():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    ensure_status_column()

    print("\nApplication Tracker Summary")
    print("=" * 40)

    for status in VALID_STATUSES:
        cursor.execute(
            "SELECT COUNT(*) FROM jobs WHERE application_status=?",
            (status,)
        )
        count = cursor.fetchone()[0]
        print(f"{status:10}: {count}")

    print("\nTop tracked jobs")
    print("-" * 40)

    cursor.execute(
        """
        SELECT id, company, role, match_score, application_status
        FROM jobs
        ORDER BY match_score DESC
        LIMIT 10
        """
    )

    rows = cursor.fetchall()

    for job_id, company, role, score, status in rows:
        print(f"{job_id:2} | {score:5.1f}% | {status:10} | {company} | {role}")

    conn.close()


if __name__ == "__main__":
    ensure_status_column()
    show_summary()
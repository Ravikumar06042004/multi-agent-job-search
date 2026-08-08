import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "jobs.db")

THRESHOLD = 40.0  # Minimum match score


def create_priority_queue():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT company, role, match_score
        FROM jobs
        WHERE match_score >= ?
        ORDER BY match_score DESC
        LIMIT 10
        """,
        (THRESHOLD,)
    )

    jobs = cursor.fetchall()

    print("Top AI Job Matches")
    print("=" * 60)

    for company, role, score in jobs:
        print(f"{score}% | {company} | {role}")

    conn.close()


if __name__ == "__main__":
    create_priority_queue()
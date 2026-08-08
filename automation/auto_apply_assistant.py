import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "jobs.db")


def prepare_applications():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT company, role, match_score, resume_path
        FROM jobs
        LIMIT 5
        """
    )

    jobs = cursor.fetchall()
    conn.close()

    print("Top matched jobs")
    print("=" * 60)

    for company, role, score, resume_path in jobs:
        print(f"Company: {company}")
        print(f"Role: {role}")
        print(f"Raw Score: {score}")
        print(f"Resume: {resume_path}")
        print("-" * 60)

    print(f"Prepared {len(jobs)} applications.")


if __name__ == "__main__":
    prepare_applications()
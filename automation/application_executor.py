import sqlite3
import os
import json

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "jobs.db")
OUTPUT_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "application_queue.json")


def build_application_queue():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT company, role, match_score, resume_path, job_url
        FROM jobs
        WHERE match_score >= 40
        ORDER BY match_score DESC
        LIMIT 10
        """
    )

    jobs = cursor.fetchall()
    conn.close()

    queue = []

    for company, role, score, resume_path, job_url in jobs:
        queue.append(
            {
                "company": company,
                "role": role,
                "match_score": score,
                "resume_path": resume_path,
                "job_url": job_url,
                "status": "Ready"
            }
        )

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(queue, f, indent=2)

    print(f"Prepared application queue for {len(queue)} jobs.")


if __name__ == "__main__":
    build_application_queue()
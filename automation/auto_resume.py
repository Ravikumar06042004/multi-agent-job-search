import sqlite3
import os
import sys

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from resume_tailor import tailor_resume

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "jobs.db")


def auto_generate_resumes():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, company, role
        FROM jobs
        WHERE resume_path IS NULL
        """
    )

    jobs = cursor.fetchall()

    generated = 0

    for job_id, company, role in jobs:
        try:
            print(f"Generating resume for: {company}")

            # Use role as a simple job description
            job_description = role

            resume_path = tailor_resume(job_description, company)

            cursor.execute(
                "UPDATE jobs SET resume_path = ? WHERE id = ?",
                (resume_path, job_id)
            )

            generated += 1

        except Exception as e:
            print(f"Failed: {company}")
            print(e)

    conn.commit()
    conn.close()

    print(f"Generated resumes for {generated} jobs.")


if __name__ == "__main__":
    auto_generate_resumes()
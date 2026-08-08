import sqlite3
import os
import re

DB_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "data",
    "jobs.db"
)

RESUME_SKILLS = {
    "python",
    "fastapi",
    "sql",
    "mysql",
    "rag",
    "llm",
    "langchain",
    "docker",
    "git",
    "api",
    "machine learning",
    "ai",
    "genai",
    "aws",
    "azure",
    "spark",
    "airflow"
}


def extract_keywords(text):
    if not text:
        return set()

    text = text.lower()

    words = re.findall(
        r"[a-zA-Z0-9+#.-]+",
        text
    )

    return set(words)


def calculate_match(job_text):
    job_keywords = extract_keywords(job_text)

    if not job_keywords:
        return 0

    matched = RESUME_SKILLS.intersection(job_keywords)

    score = (len(matched) / len(job_keywords)) * 100

    return round(min(score, 100), 2)

def update_match_scores():

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT 
            id,
            role,
            company,
            skills,
            description
        FROM jobs
        """
    )

    jobs = cursor.fetchall()

    updated = 0

    for job in jobs:

        job_id, role, company, skills, description = job

        full_text = f"""
        {role}
        {company}
        {skills}
        {description}
        """

        score = calculate_match(full_text)

        cursor.execute(
            """
            UPDATE jobs
            SET match_score=?
            WHERE id=?
            """,
            (score, job_id)
        )

        updated += 1


    conn.commit()
    conn.close()

    print(f"Updated match scores for {updated} jobs.")


if __name__ == "__main__":
    update_match_scores()
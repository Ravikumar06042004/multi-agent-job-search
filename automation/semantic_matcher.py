import sqlite3
import os
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from pypdf import PdfReader

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "jobs.db")
RESUME_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "resumes", "master_resume.pdf")

model = SentenceTransformer("all-MiniLM-L6-v2")


def read_resume():
    reader = PdfReader(RESUME_PATH)
    text = ""
    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted + "\n"
    return text


def update_semantic_scores():
    resume_text = read_resume()
    resume_embedding = model.encode([resume_text])

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, role, company, job_description
        FROM jobs
        """
    )

    jobs = cursor.fetchall()

    updated = 0

    for job_id, role, company, job_description in jobs:
        if job_description:
            job_text = job_description
        else:
            job_text = f"{role} {company}"

        job_embedding = model.encode([job_text])

        similarity = cosine_similarity(resume_embedding, job_embedding)[0][0]
        score = float(round(similarity * 100, 2))

        cursor.execute(
            "UPDATE jobs SET match_score=? WHERE id=?",
            (score, job_id)
        )

        updated += 1

    conn.commit()
    conn.close()

    print(f"Semantic match updated for {updated} jobs.")


if __name__ == "__main__":
    update_semantic_scores()
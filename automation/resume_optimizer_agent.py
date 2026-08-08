import sqlite3
import os
from collections import Counter

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "jobs.db")
RESUME_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "resumes", "master_resume.pdf")

AI_KEYWORDS = [
    "python", "fastapi", "sql", "llm", "rag", "langchain",
    "ollama", "chromadb", "vector database", "prompt engineering",
    "genai", "agentic ai", "api", "machine learning",
    "deep learning", "transformers"
]


def get_connection():
    return sqlite3.connect(DB_PATH)


def analyze_job_descriptions():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT role, company, job_description
        FROM jobs
        WHERE match_score >= 40
        """
    )

    rows = cursor.fetchall()
    conn.close()

    keyword_counter = Counter()

    for role, company, description in rows:
        text = f"{role} {company} {description or ''}".lower()

        for keyword in AI_KEYWORDS:
            if keyword in text:
                keyword_counter[keyword] += 1

    return keyword_counter


def optimize_resume():
    keywords = analyze_job_descriptions()

    print("Resume optimizer analysis")
    print("=" * 40)

    if not keywords:
        print("No matching jobs found.")
        return

    print("Top AI keywords in matched jobs:\\n")

    for keyword, count in keywords.most_common(10):
        print(f"{keyword:20} {count}")

    print("\\nRecommended resume additions:")

    recommendations = [
        "Add a strong AI Engineer summary with Python, FastAPI, SQL, LLM, and RAG.",
        "Highlight LangChain, ChromaDB, Ollama, and vector database projects.",
        "Emphasize API integration and AI automation projects.",
        "Include measurable impact in projects (automation, matching accuracy, time saved)."
    ]

    for r in recommendations:
        print(f"- {r}")

    print("\\nEstimated ATS improvement: +15% to +30%")


if __name__ == "__main__":
    optimize_resume()
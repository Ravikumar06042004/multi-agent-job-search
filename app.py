from fastapi import FastAPI
from pydantic import BaseModel
from pipeline import run_pipeline
from application_tracker import create_application_table, get_applications, add_application
import sqlite3
import os

app = FastAPI(title="Multi-Agent Job Search API")

DB_PATH = "data/jobs.db"

# ---------------- Home ----------------

@app.get("/")
def home():
    return {"message": "Multi-Agent Job Search System is running"}

# ---------------- Run Pipeline ----------------

@app.post("/run-pipeline")
def run():
    run_pipeline()
    return {"status": "Pipeline executed successfully"}

# ---------------- Get Jobs ----------------

@app.get("/jobs")
def get_jobs():
    if not os.path.exists(DB_PATH):
        return {"error": f"Database not found: {DB_PATH}"}

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT company, role, location, skills, experience, match_score, resume_path
        FROM jobs
        ORDER BY match_score DESC
        """
    )

    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]

# ---------------- Get Applications ----------------

@app.get("/applications")
def applications():
    create_application_table()
    apps = get_applications()

    return [
        {
            "company": app[0],
            "role": app[1],
            "applied_date": app[2],
            "status": app[3]
        }
        for app in apps
    ]

# ---------------- Apply to a Job ----------------

class ApplicationRequest(BaseModel):
    company: str
    role: str

@app.post("/apply")
def apply_job(request: ApplicationRequest):
    create_application_table()

    add_application(
        company=request.company,
        role=request.role,
        status="Applied"
    )

    return {
        "message": "Application added successfully",
        "company": request.company,
        "role": request.role,
        "status": "Applied"
    }
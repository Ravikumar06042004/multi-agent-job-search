import sqlite3
import os
import smtplib
from email.mime.text import MIMEText

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "jobs.db")

# Replace with your email credentials
SENDER_EMAIL = "b.y.ravi987@gmail.com"
APP_PASSWORD = "ddiy sbhq olpk xifo"
RECEIVER_EMAIL = "b.y.ravi987@gmail.com"


def get_summary():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM jobs")
    total_jobs = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM jobs WHERE resume_path IS NOT NULL")
    resumes_generated = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM applications WHERE status='Ready'")
    ready_jobs = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM applications WHERE status='Applied'")
    applied_jobs = cursor.fetchone()[0]

    cursor.execute(
        "SELECT company, role FROM applications ORDER BY id DESC LIMIT 10"
    )
    recent = cursor.fetchall()

    conn.close()

    return total_jobs, resumes_generated, ready_jobs, applied_jobs, recent


def send_email():
    total_jobs, resumes_generated, ready_jobs, applied_jobs, recent = get_summary()

    body = f"""
Daily AI Job Report

Total Jobs: {total_jobs}
Resumes Generated: {resumes_generated}
Ready to Apply: {ready_jobs}
Applied Jobs: {applied_jobs}

Recent Jobs:
"""

    for company, role in recent:
        body += f"- {company} | {role}\n"

    msg = MIMEText(body)
    msg["Subject"] = "Daily AI Job Automation Report"
    msg["From"] = SENDER_EMAIL
    msg["To"] = RECEIVER_EMAIL

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(SENDER_EMAIL, APP_PASSWORD)
        server.send_message(msg)

    print("Email report sent successfully.")


if __name__ == "__main__":
    send_email()
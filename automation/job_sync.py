import json
import sqlite3
import os
import re

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "jobs.db")

FILES = [
    ("naukri_jobs.json", "Naukri"),
    ("linkedin_jobs.json", "LinkedIn")
]


def extract_plain_url(link):
    """Convert markdown links like [url](url) into plain URLs."""
    if not link:
        return ""

    match = re.search(r"\((https?://[^)]+)\)", link)
    if match:
        return match.group(1)

    if link.startswith("http"):
        return link

    return ""


def sync_jobs():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Add job_url column if it does not exist
    try:
        cursor.execute("ALTER TABLE jobs ADD COLUMN job_url TEXT")
    except sqlite3.OperationalError:
        pass

    added = 0
    updated = 0

    for filename, source in FILES:
        if not os.path.exists(filename):
            continue

        with open(filename, "r", encoding="utf-8") as f:
            jobs = json.load(f)

        for job in jobs:
            title = job.get("title", "")
            link = extract_plain_url(job.get("link", ""))

            # Extract company and role
            company = title
            role = title

            if " - " in title:
                parts = title.split(" - ", 1)
                company = parts[0].strip()
                role = parts[1].strip()

            cursor.execute(
                "SELECT id, job_url FROM jobs WHERE role=? AND company=?",
                (role, company)
            )

            existing = cursor.fetchone()

            if existing:
                job_id, existing_url = existing

                # Update missing job_url
                if link and (existing_url is None or existing_url == ""):
                    cursor.execute(
                        "UPDATE jobs SET job_url=? WHERE id=?",
                        (link, job_id)
                    )
                    updated += 1
            else:
                cursor.execute(
                    """
                    INSERT INTO jobs
                    (company, role, location, skills, experience,
                     match_score, resume_path, job_url)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        company,
                        role,
                        "Bangalore",
                        "",
                        "Not specified",
                        0.0,
                        None,
                        link
                    )
                )
                added += 1

    conn.commit()
    conn.close()

    print(f"Imported {added} new jobs into the database.")
    print(f"Updated {updated} job URLs.")


if __name__ == "__main__":
    sync_jobs()
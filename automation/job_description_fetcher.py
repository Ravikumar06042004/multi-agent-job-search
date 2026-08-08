import sqlite3
import os
import requests
from bs4 import BeautifulSoup

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "jobs.db")


def fetch_description(url):
    try:
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/137.0.0.0 Safari/537.36"
            )
        }

        response = requests.get(url, headers=headers, timeout=10)

        print(f"Fetching: {url}")
        print(f"Status: {response.status_code}")

        if response.status_code != 200:
            return ""

        soup = BeautifulSoup(response.text, "html.parser")
        text = soup.get_text(separator=" ", strip=True)

        return text[:5000]

    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return ""


def update_job_descriptions():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        cursor.execute("ALTER TABLE jobs ADD COLUMN job_description TEXT")
    except sqlite3.OperationalError:
        pass

    cursor.execute(
        """
        SELECT id, job_url
        FROM jobs
        WHERE job_url IS NOT NULL
        """
    )

    jobs = cursor.fetchall()

    print(f"Found {len(jobs)} jobs with URLs")

    updated = 0

    for job_id, url in jobs:
        description = fetch_description(url)

        if description:
            cursor.execute(
                "UPDATE jobs SET job_description=? WHERE id=?",
                (description, job_id)
            )
            updated += 1

    conn.commit()
    conn.close()

    print(f"Updated job descriptions for {updated} jobs.")


if __name__ == "__main__":
    update_job_descriptions()
import os
import requests
from dotenv import load_dotenv
from crewai.tools import tool
from job_parser import extract_job_description

load_dotenv()

SERPER_API_KEY = os.getenv("SERPER_API_KEY")

@tool
def search_jobs(skills: str, experience: str, location: str):
    """
    Search LinkedIn and Naukri jobs using Serper API
    and extract job descriptions.
    """

    query = f"{skills} jobs {location} LinkedIn OR Naukri"

    url = "https://google.serper.dev/search"

    headers = {
        "X-API-KEY": SERPER_API_KEY,
        "Content-Type": "application/json"
    }

    payload = {
        "q": query,
        "num": 5
    }

    response = requests.post(url, headers=headers, json=payload)
    data = response.json()

    jobs = []

    for item in data.get("organic", []):
        job_url = item.get("link")

        # Extract job description
        job_description = extract_job_description(job_url)

        jobs.append({
            "title": item.get("title"),
            "link": job_url,
            "snippet": item.get("snippet"),
            "description": job_description
        })

    return jobs

if __name__ == "__main__":
    result = search_jobs.run(
        skills="Python RAG LLM",
        experience="Fresher",
        location="Bangalore"
    )

    for i, job in enumerate(result, start=1):
        print("\n" + "=" * 80)
        print(f"Job {i}")
        print(f"Title: {job['title']}")
        print(f"Link: {job['link']}")
        print(f"Snippet: {job['snippet']}")
        print(f"Description Preview:\n{job['description'][:500]}")
        print("=" * 80)
from tools import search_jobs
from resume_matcher import extract_text, calculate_match_score
from resume_tailor import tailor_resume
from job_analyzer import analyze_job
from database import save_job, create_database

import hashlib


RESUME_PATH = "resumes/master_resume.pdf"


def run_pipeline():

    # Ensure database exists
    create_database()

    print("Searching jobs...")

    jobs = search_jobs.run(
        skills="Python RAG LLM",
        experience="Fresher",
        location="Bangalore"
    )

    resume_text = extract_text(RESUME_PATH)

    print("\nJob analysis:\n")


    for i, job in enumerate(jobs, start=1):

        jd = job.get("description") or job.get("snippet", "")


        # Create unique job ID
        job_unique_text = (
            job.get("title", "") +
            jd
        )

        job_id = hashlib.md5(
            job_unique_text.encode()
        ).hexdigest()


        analysis = analyze_job(jd)

        score = calculate_match_score(
            resume_text,
            jd
        )


        print(f"{i}. {job.get('title', 'Unknown Company')}")
        print(f"Required Skills : {analysis['skills']}")
        print(f"Experience      : {analysis['experience']}")
        print(f"Match Score     : {score}%")


        resume_path = None


        if score >= 15:

            print("Generating tailored resume...")

            company = job.get(
                "title",
                "Company"
            )

            resume_path = tailor_resume(
                jd,
                company
            )


        # Save job in database
        save_job(
            job_id=job_id,
            company=job.get(
                "title",
                "Unknown Company"
            ),
            role=job.get(
                "title",
                "Unknown Role"
            ),
            location="Bangalore",
            skills=analysis["skills"],
            experience=analysis["experience"],
            match_score=score,
            resume_path=resume_path,
        )


        print("Saved to database.")
        print("-" * 70)



if __name__ == "__main__":
    run_pipeline()
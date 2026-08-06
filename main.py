from tools import search_jobs
from resume_tailor import tailor_resume
from pdf_generator import generate_pdf
import re
import os


def clean_filename(name):
    return re.sub(r'[^a-zA-Z0-9_-]', '_', name)


def run_pipeline():

    skills = "Python RAG LLM"
    experience = "Fresher"
    location = "Bangalore"

    print("Searching jobs...\n")


    jobs = search_jobs.run(
        skills=skills,
        experience=experience,
        location=location
    )


    print(f"Found {len(jobs)} jobs\n")


    for i, job in enumerate(jobs, start=1):

        print(f"Processing Job {i}: {job['title']}")


        job_description = job.get(
            "description",
            ""
        )


        if len(job_description.strip()) < 100:
            print(
                "Skipping job description not available\n"
            )
            continue


        # Tailor Resume

        tailored_resume = tailor_resume(
            job_description
        )


        # File name

        company_name = clean_filename(
            job["title"][:40]
        )


        filename = (
            f"{company_name}_resume.pdf"
        )


        output_path = os.path.join(
            "resumes",
            filename
        )


        # Generate PDF

        generate_pdf(
            tailored_resume,
            output_path
        )


        print(
            f"Resume saved: {output_path}\n"
        )


    print(
        "Job search and resume generation completed!"
    )



if __name__ == "__main__":
    run_pipeline()
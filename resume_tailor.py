from pypdf import PdfReader
from pdf_generator import create_resume_pdf
import ollama
import os
import re

# Base directory of the project
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Absolute paths
RESUME_PATH = os.path.join(BASE_DIR, "resumes", "master_resume.pdf")
OUTPUT_DIR = os.path.join(BASE_DIR, "resumes", "tailored_resumes")


def read_resume():
    reader = PdfReader(RESUME_PATH)
    text = ""

    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted + "\n"

    return text


def safe_filename(name):
    return re.sub(r'[\\\\/:*?"<>|]', "", name).replace(" ", "_")


def tailor_resume(job_description, company_name):
    resume_text = read_resume()

    prompt = f"""
You are an ATS resume optimization expert.

Candidate resume:
{resume_text}

Job description:
{job_description}

Rewrite the resume summary, skills section, and professional profile to better
match the job description.

Rules:
- Keep the resume ATS-friendly.
- Do not invent experience.
- Use keywords from the job description where appropriate.
- Maintain a professional resume structure.
- Return only the resume content.
"""

    response = ollama.chat(
        model="llama3.2:3b",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    tailored = response["message"]["content"]

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    base_name = safe_filename(company_name)

    txt_path = os.path.join(OUTPUT_DIR, f"{base_name}_Resume.txt")
    pdf_path = os.path.join(OUTPUT_DIR, f"{base_name}_Resume.pdf")

    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(tailored)

    create_resume_pdf(tailored, pdf_path)

    print(f"Tailored resume saved to: {pdf_path}")

    return pdf_path


if __name__ == "__main__":
    sample_jd = """
Looking for a Python developer with experience in FastAPI, Docker,
SQL, RAG, LLM, LangChain, and API development.
"""

    tailor_resume(sample_jd, "Sample_Company")
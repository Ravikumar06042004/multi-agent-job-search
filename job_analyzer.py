import re

def analyze_job(job_description):
    text = job_description.lower()

    skills = []

    skill_list = [
        "python",
        "fastapi",
        "sql",
        "docker",
        "rag",
        "llm",
        "langchain",
        "llamaindex",
        "git",
        "aws",
        "azure"
    ]

    for skill in skill_list:
        if skill in text:
            skills.append(skill)

    exp_match = re.search(r"(\d+)\s*-\s*(\d+)\s*yrs", text)

    experience = exp_match.group(0) if exp_match else "Not specified"

    return {
        "skills": skills,
        "experience": experience
    }

if __name__ == "__main__":
    sample = "Looking for Python, FastAPI, Docker, RAG and LLM experience. 2-5 yrs required."

    result = analyze_job(sample)

    print(result)
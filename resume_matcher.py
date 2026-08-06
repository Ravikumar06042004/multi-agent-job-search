from pypdf import PdfReader
import re

def extract_text(pdf_path):
    reader = PdfReader(pdf_path)
    text = ''
    for page in reader.pages:
        content = page.extract_text()
        if content:
            text += content + ' '
    return text.lower()

def calculate_match_score(resume_text, job_description):
    resume_words = set(re.findall(r'\b[a-zA-Z0-9+#.]+\b', resume_text))
    jd_words = set(re.findall(r'\b[a-zA-Z0-9+#.]+\b', job_description.lower()))

    common = resume_words.intersection(jd_words)

    if len(jd_words) == 0:
        return 0

    score = (len(common) / len(jd_words)) * 100
    return round(score, 2)

if __name__ == '__main__':
    resume = extract_text('resumes/master_resume.pdf')

    sample_jd = '''
    Looking for a Python developer with experience in FastAPI, SQL, Docker,
    RAG, LLM, LangChain and API development.
    '''

    score = calculate_match_score(resume, sample_jd)
    print(f'Resume Match Score: {score}%')
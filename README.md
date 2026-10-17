# 🤖 Multi-Agent Job Search & Resume Automation System

> An AI-assisted job-search workflow that discovers relevant roles, evaluates job descriptions against a resume, generates tailored resume documents, and helps track applications.

[![Python](https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/API-FastAPI-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![LLM](https://img.shields.io/badge/AI-Ollama%20%7C%20LangChain-6B46C1)](https://ollama.com/)
[![Database](https://img.shields.io/badge/Database-SQLite-003B57?logo=sqlite&logoColor=white)](https://www.sqlite.org/)

## 📌 Overview

The **Multi-Agent Job Search & Resume Automation System** brings multiple stages of a job hunt into one Python workflow. It searches for job opportunities, extracts job descriptions, compares role requirements with a candidate resume, creates role-specific resume versions, and stores job/application information for review.

The project is organized into components so job discovery, analysis, resume matching, resume tailoring, data persistence, APIs, reporting, and browser workflows can be developed and tested separately.

## ✨ Key Features

- **Job discovery:** Retrieves job-search results using a configured search API such as Serper.
- **Job-description processing:** Extracts job-description text and identifies role requirements and relevant skills.
- **Resume-to-job matching:** Calculates relevance using resume/job text and configured semantic-matching components.
- **AI-assisted tailoring:** Uses a configured local LLM workflow (Ollama/LangChain) to help produce a job-specific resume.
- **ATS-friendly resume output:** Generates tailored resume documents for review before use.
- **Application tracking:** Persists job and application records in a SQL database.
- **API layer:** FastAPI endpoints expose pipeline and job/application operations; interactive API documentation is available through Swagger when the server is running.
- **Dashboard and notifications:** The project includes a dashboard/reporting workflow and email notifications where configured.
- **Browser-assisted workflows:** Browser automation may assist with job-site actions where implemented and configured.

## 🧱 Architecture

```text
Search API / Job Sources
          │
          ▼
   Job Discovery Tools
          │
          ▼
 Job Description Extraction
          │
          ▼
 Resume + Job Analysis
          │
          ▼
 Match Scoring / Semantic Ranking
          │
          ▼
 LLM-Assisted Resume Tailoring
          │
          ▼
 PDF Output + SQL Application Records
          │
          ▼
 FastAPI / Dashboard / Notifications
```

The exact path through the workflow depends on the configured modules, credentials, and enabled automation features.

## 🛠️ Technology Stack

- **Language:** Python
- **AI/LLM integration:** LangChain and Ollama
- **Job discovery:** Configured search API (e.g. Serper)
- **Matching:** Text processing, embeddings/semantic similarity where configured
- **Backend:** FastAPI
- **Data storage:** SQL/SQLite components
- **Dashboard and reporting:** Streamlit/dashboard components and email notifications where configured
- **Automation:** Browser automation tools used by the implementation
- **Version control:** Git and GitHub

> Keep this list aligned with the dependencies and modules currently enabled in the repository. Do not claim a tool is active if it is only an experiment or planned feature.

## 📂 Main Components

Typical project components include:

- `app.py` — API application entry point
- `pipeline.py` — coordinates job discovery and processing stages
- `agents.py` / agent modules — task-specific agent logic
- `tools.py` — reusable job-search and processing tools
- `database.py` — persistence helpers
- `resumes/` — master and generated resume documents, if present locally
- `automation/` — browser workflow scripts, if present

The repository layout may evolve as components are refactored.

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/Ravikumar06042004/multi-agent-job-search.git
cd multi-agent-job-search
```

### 2. Create and activate a virtual environment (Windows PowerShell)

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a local `.env` file based on the repository's `.env.example` (if included). Add the API key, model, email, and other configuration values required by the enabled features.

- Keep secrets in `.env` or a secret manager.
- Never commit real API keys, mailbox passwords, access tokens, or browser session data.
- Start Ollama and download the model specified by your local configuration if you use local LLM features.

### 5. Start the API

Check `app.py` and the project README/configuration for the intended launch command. A common FastAPI development command, **if the app object is named `app` in `app.py`**, is:

```powershell
uvicorn app:app --reload
```

Then visit `http://127.0.0.1:8000/docs` to inspect and test the API endpoints.

### 6. Run the dashboard (if enabled)

Check the dashboard entry-point file and use the launch command documented for that file. For Streamlit applications, the pattern is:

```powershell
streamlit run dashboard.py
```

Replace `dashboard.py` with the actual dashboard filename in this repository.

## 🔐 Responsible Automation

- Review every job match and generated resume before applying.
- Keep resume content truthful and do not invent skills, employment history, or qualifications.
- Respect job-platform terms of service and rate limits.
- Do not bypass CAPTCHA, identity checks, or other anti-bot verification. Pause and complete required verification manually.
- Use browser automation only for accounts and actions you are authorized to access.

## 🧪 Testing

If `pytest` and the project tests are installed, run:

```powershell
python -m pytest
```

Some tests may need environment variables, external services, or local model setup.

## 🗺️ Possible Future Improvements

- More robust job-source adapters and duplicate detection
- Transparent match-score explanations
- Better resume/job-description parsing tests
- Clear human approval checkpoints before submitting applications
- Improved error handling and observability for browser automation

## 👨‍💻 Author

**Ravi Kumar Bitra**

- GitHub: [Ravikumar06042004](https://github.com/Ravikumar06042004)
- Repository: [Multi-Agent Job Search](https://github.com/Ravikumar06042004/multi-agent-job-search)

## ⚠️ Disclaimer

This is a personal software project for job-search workflow assistance. Search results, relevance scores, and generated documents can contain errors. Always verify job details and review application materials yourself before submitting.

from crewai import Agent, LLM
from tools import search_jobs

# Local Ollama LLM
local_llm = LLM(
    model="ollama/llama3.2:3b",
    base_url="http://localhost:11434"
)

job_researcher = Agent(
    role="Job Market Researcher",
    goal="Find matching job listings based on skills, experience, and location.",
    backstory=(
        "You are an expert job researcher who searches LinkedIn and Naukri "
        "for relevant jobs and extracts the most important requirements."
    ),
    tools=[search_jobs],
    llm=local_llm,
    verbose=True
)

if __name__ == "__main__":
    print(job_researcher)
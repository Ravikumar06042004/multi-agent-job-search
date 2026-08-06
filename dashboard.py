import streamlit as st
import requests
import os

st.set_page_config(page_title="Multi-Agent Job Search Dashboard", layout="wide")

st.title("Multi-Agent Job Search Dashboard")
st.write("View job matches and generated resumes")

JOBS_API = "http://127.0.0.1:8000/jobs"

response = requests.get(JOBS_API)

if response.status_code == 200:
    jobs = response.json()

    st.subheader("Job Matches")

    for job in jobs:
        with st.container():
            st.markdown(f"### {job['company']}")
            st.write(f"**Role:** {job['role']}")
            st.write(f"**Location:** {job['location']}")
            st.write(f"**Skills:** {job['skills']}")
            st.write(f"**Experience:** {job['experience']}")
            st.write(f"**Match Score:** {job['match_score']}%")

            resume_path = job.get("resume_path")

            if resume_path and os.path.exists(resume_path):
                with open(resume_path, "rb") as file:
                    st.download_button(
                        label="Download Resume",
                        data=file,
                        file_name=os.path.basename(resume_path),
                        mime="application/pdf",
                        key=job["company"]
                    )
            else:
                st.warning("Resume not available")

            st.divider()

    st.success(f"Total Jobs: {len(jobs)}")

else:
    st.error("Could not connect to FastAPI backend.")
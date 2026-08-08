import streamlit as st
import sqlite3
import os
import pandas as pd

DB_PATH = os.path.join("data", "jobs.db")

st.set_page_config(page_title="AI Job Automation Dashboard", layout="wide")

st.title("AI Job Automation Dashboard")
st.write("Naukri + LinkedIn AI Job Tracking System")

conn = sqlite3.connect(DB_PATH)

jobs = pd.read_sql_query(
    """
    SELECT company, role, location, experience, match_score, resume_path
    FROM jobs
    ORDER BY id DESC
    """,
    conn
)

applications = pd.read_sql_query(
    """
    SELECT company, role, status, applied_at
    FROM applications
    ORDER BY id DESC
    """,
    conn
)

conn.close()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Jobs", len(jobs))

with col2:
    resumes = jobs["resume_path"].notna().sum()
    st.metric("Resumes Generated", int(resumes))

with col3:
    applied = len(applications[applications["status"] == "Applied"])
    st.metric("Applied Jobs", int(applied))

st.divider()

st.subheader("Job Matches")

for _, job in jobs.iterrows():
    with st.container(border=True):
        st.markdown(f"### {job['company']}")
        st.write(f"**Role:** {job['role']}")
        st.write(f"**Location:** {job['location']}")
        st.write(f"**Experience:** {job['experience']}")
        st.write(f"**Match Score:** {job['match_score']}%")

        if pd.notna(job['resume_path']):
            st.success("Tailored Resume Generated")
        else:
            st.warning("Resume Pending")

st.divider()

st.subheader("Application Queue")

if len(applications) == 0:
    st.info("No applications tracked yet.")
else:
    st.dataframe(applications, width="stretch")
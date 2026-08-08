import subprocess
import sys
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
AUTOMATION_DIR = os.path.join(BASE_DIR, "automation")


def run_script(script_name):
    script_path = os.path.join(AUTOMATION_DIR, script_name)

    print(f"\n{'=' * 60}")
    print(f"Running: {script_name}")
    print(f"{'=' * 60}")

    result = subprocess.run(
        [sys.executable, script_path],
        cwd=AUTOMATION_DIR
    )

    if result.returncode != 0:
        print(f"Failed: {script_name}")
        return False

    print(f"Completed: {script_name}")
    return True


def daily_pipeline():
    steps = [
    "naukri_search.py",
    "linkedin_search.py",
    "job_sync.py",
    "job_description_fetcher.py",
    "semantic_matcher.py",
    "auto_resume.py",
    "auto_apply_queue.py",
    "priority_queue.py",
    "application_tracker.py",
    "application_manager.py",
    "email_report.py"
   ]
    for step in steps:
        success = run_script(step)

        if not success:
            print(f"Pipeline stopped at {step}")
            return

    print("\nDaily job automation completed successfully.")


if __name__ == "__main__":
    daily_pipeline()
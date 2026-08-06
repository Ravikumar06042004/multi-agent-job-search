import requests
from bs4 import BeautifulSoup
import time
import random

def extract_job_description(url):
    try:
        # Random delay to avoid aggressive requests
        time.sleep(random.uniform(2, 5))

        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/138.0.0.0 Safari/537.36"
            )
        }

        response = requests.get(url, headers=headers, timeout=15)

        if response.status_code != 200:
            return f"Failed to fetch page (Status: {response.status_code})"

        soup = BeautifulSoup(response.text, "html.parser")

        # Extract visible text
        text = soup.get_text(separator=" ", strip=True)

        return text[:3000]

    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    url = "https://www.naukri.com/rag-jobs"
    jd = extract_job_description(url)
    print(jd)
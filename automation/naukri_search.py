from playwright.sync_api import sync_playwright
import json
import urllib.parse

SESSION_FILE = "naukri_session.json"
SEARCH_KEYWORDS = "Python RAG LLM AI Engineer"
LOCATION = "Bangalore"


def search_naukri_jobs():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)

        context = browser.new_context(storage_state=SESSION_FILE)
        page = context.new_page()

        keyword = urllib.parse.quote(SEARCH_KEYWORDS)
        location = urllib.parse.quote(LOCATION)

        search_url = f"https://www.naukri.com/{keyword}-jobs-in-{location.lower()}?k={keyword}&l={location}"

        page.goto(search_url)
        page.wait_for_timeout(5000)

        jobs = []

        job_cards = page.locator("a.title")
        count = min(job_cards.count(), 10)

        for i in range(count):
            title = job_cards.nth(i).inner_text()
            link = job_cards.nth(i).get_attribute("href")

            jobs.append({
                "title": title,
                "link": link
            })

        with open("naukri_jobs.json", "w", encoding="utf-8") as f:
            json.dump(jobs, f, indent=4)

        print(f"Found {count} jobs")
        print("Saved to naukri_jobs.json")

        page.wait_for_timeout(2000)
        browser.close()

if __name__ == "__main__":
    search_naukri_jobs()
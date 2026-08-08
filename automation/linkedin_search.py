from playwright.sync_api import sync_playwright
import json
import urllib.parse

SEARCH_KEYWORDS = "Python LLM RAG AI Engineer"
LOCATION = "Bangalore"


def linkedin_search():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)

        page = browser.new_page()

        keyword = urllib.parse.quote(SEARCH_KEYWORDS)
        location = urllib.parse.quote(LOCATION)

        url = (
            f"https://www.linkedin.com/jobs/search/?keywords={keyword}&location={location}"
        )

        page.goto(url)
        page.wait_for_timeout(5000)

        jobs = []

        cards = page.locator("a.base-card__full-link")
        count = min(cards.count(), 10)

        for i in range(count):
            title = cards.nth(i).inner_text()
            link = cards.nth(i).get_attribute("href")

            jobs.append({
                "title": title,
                "link": link,
                "source": "LinkedIn"
            })

        with open("linkedin_jobs.json", "w", encoding="utf-8") as f:
            json.dump(jobs, f, indent=4)

        print(f"LinkedIn: Found {count} jobs.")

        browser.close()


if __name__ == "__main__":
    linkedin_search()
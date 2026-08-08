from browser import BrowserManager
import os

NAUKRI_EMAIL = "b.y.ravi987@gmail.com"
NAUKRI_PASSWORD = "Kumar@59325"

SESSION_FILE = "naukri_session.json"

manager = BrowserManager(headless=False)
page = manager.start()

page.goto("https://www.naukri.com")

# Click Login
page.click("text=Login")
page.wait_for_timeout(2000)

# Fill credentials
page.fill('input[type="text"]', NAUKRI_EMAIL)
page.fill('input[type="password"]', NAUKRI_PASSWORD)

# Submit
page.click('button[type="submit"]')

# Wait for login
page.wait_for_timeout(5000)

# Save session
page.context.storage_state(path=SESSION_FILE)

print(f"Session saved successfully: {SESSION_FILE}")

input("Press Enter to close browser...")

manager.close()

from playwright.sync_api import sync_playwright


class BrowserManager:
    def __init__(self, headless=False):
        self.headless = headless
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None

    def start(self):
        self.playwright = sync_playwright().start()

        self.browser = self.playwright.chromium.launch(
            headless=self.headless,
            args=["--start-maximized"]
        )

        self.context = self.browser.new_context(
            viewport={"width": 1400, "height": 900}
        )

        self.page = self.context.new_page()
        return self.page

    def close(self):
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()


if __name__ == "__main__":
    manager = BrowserManager(headless=False)
    page = manager.start()

    page.goto("https://www.naukri.com")

    print("Browser opened successfully.")

    input("Press Enter to close browser...")

    manager.close()
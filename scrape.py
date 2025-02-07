
import time
import random
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

class WebsiteCrawler:
    def __init__(self, url, wait_time=10):
        """
        Initialize the WebsiteCrawler with bot evasion techniques.
        """
        self.url = url
        self.wait_time = wait_time
        self.driver = None
        self.title = None
        self.text = ""

        options = uc.ChromeOptions()
        options.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"  # Update if needed
        options.add_argument('--headless=new')  
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--remote-debugging-port=9222')  # Fixes "Chrome not reachable"
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-popup-blocking')
        options.add_argument('user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36')


        try:
            self.driver = uc.Chrome(options=options, use_subprocess=True)

            # Hide webdriver property
            self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
                "source": "Object.defineProperty(navigator, 'webdriver', { get: () => undefined })"
            })

            self._scrape_page()
        
        except Exception as e:
            print(f"Error occurred: {e}")
        
        finally:
            if self.driver:
                self.driver.quit()  # Ensures the driver quits properly

    def _scrape_page(self):
        """Handles loading the page, scrolling, and extracting content."""
        self.driver.get(self.url)

        # Simulate human-like scrolling to avoid bot detection
        for _ in range(random.randint(1, 3)):
            self.driver.execute_script("window.scrollBy(0, document.body.scrollHeight/3);")
            time.sleep(random.uniform(1, 2))

        try:
            # Wait for the <main> element to load (or fallback to <body>)
            element_locator = (By.CSS_SELECTOR, "main")
            WebDriverWait(self.driver, self.wait_time).until(
                EC.presence_of_element_located(element_locator)
            )
            content_element = self.driver.find_element(*element_locator)
        except:
            print("Warning: <main> not found, falling back to <body>")
            content_element = self.driver.find_element(By.CSS_SELECTOR, "body")

        # Extract and clean content
        soup = BeautifulSoup(content_element.get_attribute("outerHTML"), "html.parser")
        self.title = self.driver.title or "No title found"
        self.text = soup.get_text(separator="\n", strip=True)

    def get_clean_text(self):
        """Returns the extracted and cleaned text for LLM input."""
        return self.text

# Usage Example
if __name__ == "__main__":
    url = "https://edwarddonner.com/"
    crawler = WebsiteCrawler(url)
    print("Title:", crawler.title)
    print("Extracted Text:", crawler.get_clean_text())

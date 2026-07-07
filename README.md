# Website Summarizer with Streamlit, Selenium, and OpenAI

A Streamlit web app that takes a website URL, scrapes its content, and summarizes it using OpenAI's GPT-4o-mini.

## ✨ Features

- **Automated Web Scraping** – Uses **Selenium** and **BeautifulSoup** to extract website text dynamically.
- **Bot Evasion Techniques** – Implements **undetected_chromedriver** to bypass basic anti-bot mechanisms.
- **Chunked Summarization** – Splits large content into smaller parts to avoid token limits and ensure accurate summaries.
- **Streamlit Interface** – Provides an interactive UI for users to enter a URL and generate summaries easily.

## 📂 Project Structure

```bash
📦 ai_web_summarizer
│── scrape.py          # Web scraper using Selenium and BeautifulSoup
│── main.py            # Streamlit app for summarizing websites
│── .env                # Stores API key (not shared in version control)
│── requirements.txt    # Lists required dependencies
│── LICENSE             # MIT License
│── README.md           # Documentation
```

## 🛠️ Installation

### Set Up Your Environment

Create a virtual environment (using `venv` or Conda):

**Using `venv` (Recommended)**

```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate  # Windows
```

**Using conda**

```bash
conda create --name myenv python=3.11
conda activate myenv
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

Google Chrome must also be installed on your system — `undetected_chromedriver` will locate it automatically. If it's installed somewhere non-standard, set the `CHROME_BINARY_PATH` environment variable to its full path.

### Set Up Your OpenAI API Key

Create a `.env` file in the project folder and add your API key:

```ini
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxx
```

### Run the Application

```bash
streamlit run main.py
```

## 🚀 How It Works

1. The user enters a website URL in the Streamlit app.
2. `scrape.py` scrapes the content using Selenium and BeautifulSoup, handling bot evasion.
3. GPT-4o-mini processes the text — in chunks, if the page is long — and generates a summary in Markdown format.
4. The summarized output is displayed in the Streamlit UI.

## ⚡ Alternatives & Improvements

The current `WebsiteCrawler` implementation works well for many websites, but for high-scale scraping or heavily protected sites, adding proxies and captcha-solving services would improve success rates.

- **Proxy Services:** Providers like Bright Data, ScrapingAnt, or Oxylabs to handle advanced bot protection.
- **Captcha Solvers:** Services like 2Captcha or Anti-Captcha to automate solving CAPTCHA challenges.
- **Headless Browsers:** Tools like Puppeteer for more robust scraping.

## 📜 License

This project is licensed under the [MIT License](LICENSE).

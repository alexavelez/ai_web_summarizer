# Building a Website Summarizer with Streamlit, Selenium, and OpenAI

Have you ever wished you could build your apps and harness the amazing potential of large language models? I know I have! I'm super excited to share this project with you: a website summarizer built with Streamlit, Selenium, and the power of OpenAI's GPT-4o Mini. This project combines web scraping, large language models, and a user-friendly interface - a perfect blend of some of my favorite technologies.

<img width="904" alt="Screenshot 2025-02-06 at 8 20 41 PM" src="https://github.com/user-attachments/assets/3e0d85b7-728e-4516-9d7b-7c3651213147" />

## ✨ Features  

- **Automated Web Scraping** – Uses **Selenium** and **BeautifulSoup** to extract website text dynamically.  
- **Bot Evasion Techniques** – Implements **undetected_chromedriver** to bypass basic anti-bot mechanisms.  
- **Chunked Summarization** – Splits large content into smaller parts to avoid token limits and ensures accurate summaries.  
- **Streamlit Interface** – Provides an interactive UI for users to enter a URL and generate summaries easily.  

## 📂 Project Structure

```bash
📦 website-summarizer  
│── scrape.py          # Web scraper using Selenium and BeautifulSoup  
│── main.py            # Streamlit app for summarizing websites  
│── .env               # Stores API key (not shared in version control)  
│── requirements.txt   # Lists required dependencies  
│── README.md          # Documentation
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
conda create --name myenv python=3.9  
conda activate myenv
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Set Up OpenAI API Key
Create a .env file in the project folder and add your API key:

```ini
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxx
```

### Run the Application

```bash
streamlit run main.py
```

<img width="913" alt="Screenshot 2025-02-06 at 8 39 22 PM" src="https://github.com/user-attachments/assets/6bc976b6-53d9-42cf-b946-b5f1a5d989b1" />

## 🚀 How It Works

1. User enters a website URL in the Streamlit app.
2. `scrape.py` scrapes the content using Selenium and BeautifulSoup, handling bot evasion.
3. GPT-4o Mini processes the text and generates a summary in Markdown format.
4. The summarized output is displayed in the Streamlit UI.

## ⚡ Alternatives & Improvements

The current WebsiteCrawler implementation works well for many websites, but for high-scale scraping or heavily protected sites, adding proxies and captcha-solving services would improve success rates.

*   **Proxy Services:** Use providers like Bright Data, ScrapingAnt, or Oxylabs to handle advanced bot protection.
*   **Captcha Solvers:** Services like 2Captcha or Anti-Captcha can automate solving CAPTCHA challenges.
*   **Headless Browsers:** Use tools like Puppeteer for more robust scraping.

## 📜 License

This project is licensed under the MIT License.

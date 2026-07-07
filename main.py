
import os
from dotenv import load_dotenv
from openai import OpenAI
import scrape  # Import the WebsiteCrawler class from scrape.py
import streamlit as st
 
# Load environment variables
load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')
 
# Streamlit app
st.title("Website Summarizer")
 
# Validate the API key up front and stop with a clear message in the UI
# itself — a bare print() here would only show up in the server terminal,
# never in the browser, so a missing or malformed key would otherwise fail
# silently until someone clicks "Summarize" and gets a generic API error.
if not api_key:
    st.error("No OpenAI API key was found. Add OPENAI_API_KEY to a .env file in the project folder.")
    st.stop()
elif api_key.strip() != api_key:
    st.error("Your OpenAI API key appears to contain extra whitespace. Please check your .env file.")
    st.stop()
 
# Initialize OpenAI client
client = OpenAI(api_key=api_key)
 
def summarize_website(url):
    """Scrapes the website and generates a summary using OpenAI's GPT-4o Mini.
 
    Handles large websites by splitting content into smaller chunks,
    summarizing each chunk separately to avoid token overflow, then
    combining those summaries into one final summary.
    """
    crawler = scrape.WebsiteCrawler(url)
    full_text = crawler.get_clean_text()
 
    if not full_text:
        raise ValueError("No content could be extracted from that URL. The page may block automated access.")
 
    max_chunk_size = 4000  # Adjust based on GPT-4o-mini token limits
    chunks = [full_text[i:i + max_chunk_size] for i in range(0, len(full_text), max_chunk_size)]
 
    system_instructions = (
        "You are an assistant that analyzes website content and provides a short summary. "
        "Ignore navigation menus, sidebars, and irrelevant text. "
        "Respond in Markdown format."
    )
 
    summaries = []
    for chunk in chunks:
        prompt = f"""{system_instructions}
 
### Website Title: {crawler.title}
 
The following is a portion of the website's content. Summarize it in markdown:
---
{chunk}
"""
 
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_instructions},
                {"role": "user", "content": prompt}
            ]
        )
        summaries.append(response.choices[0].message.content.strip())
 
    # Combine all chunk summaries into a final summary
    final_prompt = (
        f"{system_instructions}\n\n"
        "### Combined Summary:\n"
        "Combine the following summaries into a single, concise summary:\n"
        "---\n"
        f"{chr(10).join(summaries)}"
    )
 
    final_response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_instructions},
            {"role": "user", "content": final_prompt}
        ]
    )
 
    return final_response.choices[0].message.content.strip()
 
url = st.text_input("Enter website URL:")
summarize_button = st.button("Summarize")
 
if summarize_button:
    if not url:
        st.warning("Please enter a URL.")
    else:
        with st.spinner("Summarizing..."):
            try:
                summary = summarize_website(url)
                st.write("Summary:")
                st.write(summary)
            except Exception as e:
                st.error(f"An error occurred: {e}")
 

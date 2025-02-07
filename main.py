import os
from dotenv import load_dotenv
from openai import OpenAI
import scrape  # Import the WebsiteCrawler class from scrape.py
import streamlit as st

# Load environment variables
load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')

# Validate API key
if not api_key:
    print("No API key was found - please check your .env file.")
elif not api_key.startswith("sk-proj-"):
    print("An API key was found, but it doesn't start with 'sk-proj-'. Please verify.")
elif api_key.strip() != api_key:
    print("An API key was found, but it might contain extra spaces. Please remove them.")
else:
    print("API key found and looks good!")

# Initialize OpenAI client
openai = OpenAI(api_key=api_key)

# Function to generate the user prompt for summarization
def user_prompt_for(website):
    """Generates a user prompt using website title and extracted content."""
    return f"""You are looking at a website titled: **{website.title}**

The contents of this website are as follows. Please provide a **short summary** of the website in markdown.
If it includes **news or announcements**, summarize those too.

---
{website.get_clean_text()}
"""

# Function to summarize website content using GPT-4o Mini.  Handles large websites by splitting content into smaller chunks. Summarizes each chunk separately, preventing token overflow
def summarize_website(url):
    """Scrapes the website and generates a summary using OpenAI's GPT-4o Mini."""
    crawler = scrape.WebsiteCrawler(url)  
    full_text = crawler.get_clean_text()

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

        # Use the ChatCompletion endpoint for each chunk
        response = openai.chat.completions.create(  # Updated line
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


    # Use the ChatCompletion endpoint for the final summary
    final_response = openai.chat.completions.create(  # Updated line
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_instructions},
            {"role": "user", "content": final_prompt}
        ]
    )

    return final_response.choices[0].message.content.strip()

# Streamlit app
st.title("Website Summarizer")

url = st.text_input("Enter website URL:")
summarize_button = st.button("Summarize")

if summarize_button:
    if not url:
        st.warning("Please enter a URL.")
    else:
        with st.spinner("Summarizing..."):  # Show a spinner while summarizing
            try:
                summary = summarize_website(url)
                st.write("Summary:")
                st.write(summary)  # Use st.write for Markdown rendering
            except Exception as e:
                st.error(f"An error occurred: {e}")  # Display errors in Streamlit
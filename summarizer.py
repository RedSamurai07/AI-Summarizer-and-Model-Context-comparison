import os
from openai import OpenAI
from dotenv import load_dotenv
from scrapper import fetch_website_contents

# Load environment variables from the .env file
load_dotenv()

# Initialize the OpenRouter client
client = OpenAI(
    base_url="https://openrouter.ai/api/v1", 
    api_key=os.getenv("OPENAI_API_KEY")
)  

system_prompt = """You analyze the contents of a website and
give a short, friendly summary. Ignore navigation menus.
Respond in markdown."""

def summarize(url: str) -> str:
    website = fetch_website_contents(url)
    
    # Check if the scrapper failed before sending to the LLM
    if website.startswith("Error fetching"):
        return website
        
    response = client.chat.completions.create(
        model="nvidia/nemotron-3.5-lightning:free",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Summarize this website:\n\n{website}"},
        ],
    )
    return str(response.choices[0].message.content)

if __name__ == "__main__":
    # Test the summarization pipeline
    test_url = "https://en.wikipedia.org/wiki/Retrieval-augmented_generation"
    print(f"Fetching and summarizing: {test_url}...\n")
    
    summary = summarize(test_url)
    print(summary)
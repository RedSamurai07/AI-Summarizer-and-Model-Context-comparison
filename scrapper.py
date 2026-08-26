import requests
from bs4 import BeautifulSoup

def fetch_website_contents(url: str) -> str:
    """
    Fetches HTML content and extracts readable text.
    Removes noisy elements to optimize LLM token usage.
    """
    # Using a standard User-Agent to avoid getting blocked by basic bot protections
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # Parse the raw HTML into a structured tree
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Decompose non-content tags to clean up the data context
        for element in soup(["script", "style", "nav", "footer", "noscript", "header"]):
            element.decompose()
            
        # Extract the remaining text and clean up excess whitespace
        clean_text = soup.get_text(separator=' ', strip=True)
        return clean_text
        
    except requests.exceptions.RequestException as e:
        return f"Error fetching the website: {str(e)}"
import requests
from bs4 import BeautifulSoup

def analyze_url(url):
    # This header tells the website "I am a real person using a Chrome browser"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status() # This will stop the script if we get a 403 or 404 error
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Clean up: Remove scripts and styles from analysis
        for script_or_style in soup(["script", "style"]):
            script_or_style.decompose()

        text = " ".join([p.text for p in soup.find_all('p')])
        headings = [h.text.strip() for h in soup.find_all(['h1', 'h2', 'h3']) if len(h.text.strip()) > 2]
        
        if not headings:
            headings = ["General Industry Trends"] # Fallback

        return {"content": text[:4000], "headings": headings}
        
    except Exception as e:
        print(f"Scraping Error: {e}")
        return {"content": "Could not retrieve content.", "headings": ["Error: Site Protected"]}
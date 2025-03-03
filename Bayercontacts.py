import requests
import re
import pandas as pd
from bs4 import BeautifulSoup
import os

# Replace with your own SerpAPI key (for Google Search scraping)
SERPAPI_KEY = os.getenv("SERP_API_KEY")

def google_search(query):
    """Fetch Google search results using SerpAPI."""
    url = f"https://serpapi.com/search"
    params = {
        "q": query,
        "api_key": SERPAPI_KEY,
        "num": 10  # Number of results
    }
    
    response = requests.get(url, params=params)
    data = response.json()
    
    # Extract URLs from search results
    urls = [result["link"] for result in data.get("organic_results", [])]
    return urls

def extract_emails(url):
    """Scrape a webpage for email addresses."""
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        # Extract emails using regex
        emails = set(re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", soup.text))
        return emails
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return set()

def find_emails(name, company="Bayer"):
    """Search for potential emails of a scientist from Google and scrape results."""
    search_queries = [
        f'"{name}" + "{company}" + "email"',
        f'"{name}" + "{company}" + site:researchgate.net',
        f'"{name}" + "{company}" + site:ncbi.nlm.nih.gov',
        f'"{name}" + "{company}" + site:sciencedirect.com',
        f'"{name}" + "{company}" + site:linkedin.com/contact'
    ]
    
    all_emails = set()
    
    for query in search_queries:
        print(f"Searching: {query}")
        urls = google_search(query)
        
        for url in urls:
            emails = extract_emails(url)
            if emails:
                all_emails.update(emails)
    
    return all_emails

# Step 1: Read your CSV sheet
df = pd.read_csv("Bayer_Scientists.csv")  # Replace with the actual path to your sheet

# Step 2: Add a new 'Emails' column if it doesn't exist
df["Emails"] = df["Name"].apply(lambda name: ", ".join(list(find_emails(name))))

# Step 3: Save the results back to CSV
df.to_csv("updated_sheet_with_emails.csv", index=False)

print("✅ Emails have been updated and saved to 'updated_sheet_with_emails.csv'!")

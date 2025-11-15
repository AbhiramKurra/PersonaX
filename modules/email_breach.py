import requests
from bs4 import BeautifulSoup
import re
from concurrent.futures import ThreadPoolExecutor

def search_pastebin(email):
    query = f"site:pastebin.com {email}"
    url = f"https://www.google.com/search?q={query}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
    }
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(resp.text, "lxml")
        links = [a["href"] for a in soup.find_all("a", href=True) if "pastebin.com" in a["href"]]
        return {"source": "Pastebin", "links": links}
    except Exception as e:
        return {"source": "Pastebin", "error": str(e)}

def search_ghostbin(email):
    query = f"site:ghostbin.co {email}"
    url = f"https://www.google.com/search?q={query}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
    }
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(resp.text, "lxml")
        links = [a["href"] for a in soup.find_all("a", href=True) if "ghostbin.co" in a["href"]]
        return {"source": "Ghostbin", "links": links}
    except Exception as e:
        return {"source": "Ghostbin", "error": str(e)}

def search_justpasteit(email):
    query = f"site:justpaste.it {email}"
    url = f"https://www.google.com/search?q={query}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
    }
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(resp.text, "lxml")
        links = [a["href"] for a in soup.find_all("a", href=True) if "justpaste.it" in a["href"]]
        return {"source": "JustPaste.it", "links": links}
    except Exception as e:
        return {"source": "JustPaste.it", "error": str(e)}

def search_rentry(email):
    query = f"site:rentry.co {email}"
    url = f"https://www.google.com/search?q={query}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
    }
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(resp.text, "lxml")
        links = [a["href"] for a in soup.find_all("a", href=True) if "rentry.co" in a["href"]]
        return {"source": "Rentry", "links": links}
    except Exception as e:
        return {"source": "Rentry", "error": str(e)}

def run(data):
    email = data.get("email")
    if not email:
        return "No email provided."

    # Validate email format
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_pattern, email):
        return {"error": "Invalid email format"}

    # List of search functions
    search_functions = [
        search_pastebin,
        search_ghostbin,
        search_justpasteit,
        search_rentry
    ]

    # Run searches in parallel
    with ThreadPoolExecutor(max_workers=4) as executor:
        results = list(executor.map(lambda f: f(email), search_functions))

    # Combine results
    combined_results = {
        "email": email,
        "sources_checked": len(search_functions),
        "results": results,
        "total_links": sum(len(r.get("links", [])) for r in results if "links" in r)
    }

    return combined_results 
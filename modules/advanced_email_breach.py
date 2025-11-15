import requests
from bs4 import BeautifulSoup
import re
from concurrent.futures import ThreadPoolExecutor
import json
import os

class AdvancedEmailBreach:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
        }

    def search_pastebin(self, email):
        """Search for email on Pastebin"""
        query = f"site:pastebin.com {email}"
        url = f"https://www.google.com/search?q={query}"
        try:
            resp = requests.get(url, headers=self.headers, timeout=10)
            soup = BeautifulSoup(resp.text, "lxml")
            links = [a["href"] for a in soup.find_all("a", href=True) if "pastebin.com" in a["href"]]
            return {"source": "Pastebin", "links": links}
        except Exception as e:
            return {"source": "Pastebin", "error": str(e)}

    def search_ghostbin(self, email):
        """Search for email on Ghostbin"""
        query = f"site:ghostbin.co {email}"
        url = f"https://www.google.com/search?q={query}"
        try:
            resp = requests.get(url, headers=self.headers, timeout=10)
            soup = BeautifulSoup(resp.text, "lxml")
            links = [a["href"] for a in soup.find_all("a", href=True) if "ghostbin.co" in a["href"]]
            return {"source": "Ghostbin", "links": links}
        except Exception as e:
            return {"source": "Ghostbin", "error": str(e)}

    def search_justpasteit(self, email):
        """Search for email on JustPaste.it"""
        query = f"site:justpaste.it {email}"
        url = f"https://www.google.com/search?q={query}"
        try:
            resp = requests.get(url, headers=self.headers, timeout=10)
            soup = BeautifulSoup(resp.text, "lxml")
            links = [a["href"] for a in soup.find_all("a", href=True) if "justpaste.it" in a["href"]]
            return {"source": "JustPaste.it", "links": links}
        except Exception as e:
            return {"source": "JustPaste.it", "error": str(e)}

    def search_rentry(self, email):
        """Search for email on Rentry"""
        query = f"site:rentry.co {email}"
        url = f"https://www.google.com/search?q={query}"
        try:
            resp = requests.get(url, headers=self.headers, timeout=10)
            soup = BeautifulSoup(resp.text, "lxml")
            links = [a["href"] for a in soup.find_all("a", href=True) if "rentry.co" in a["href"]]
            return {"source": "Rentry", "links": links}
        except Exception as e:
            return {"source": "Rentry", "error": str(e)}

    def search_breachdirectory(self, email):
        """Search for email on BreachDirectory"""
        try:
            url = f"https://breachdirectory.p.rapidapi.com/?func=auto&term={email}"
            headers = {
                'x-rapidapi-host': "breachdirectory.p.rapidapi.com",
                'x-rapidapi-key': "YOUR_RAPIDAPI_KEY"
            }
            response = requests.get(url, headers=headers, timeout=10)
            data = response.json()
            
            if data.get('result'):
                return {
                    "source": "BreachDirectory",
                    "breaches": [{
                        'source': breach.get('source', 'Unknown'),
                        'date': breach.get('date', 'Unknown'),
                        'details': breach.get('details', 'No details')
                    } for breach in data['result']]
                }
            return {"source": "BreachDirectory", "breaches": []}
        except Exception as e:
            return {"source": "BreachDirectory", "error": str(e)}

    def search_leakcheck(self, email):
        """Search for email on LeakCheck"""
        try:
            url = f"https://leakcheck.io/api/public?key=YOUR_API_KEY&check={email}&type=email"
            response = requests.get(url, headers=self.headers, timeout=10)
            data = response.json()
            
            if data.get('success'):
                return {
                    "source": "LeakCheck",
                    "breaches": [{
                        'source': breach.get('source', 'Unknown'),
                        'date': breach.get('date', 'Unknown'),
                        'details': breach.get('details', 'No details')
                    } for breach in data.get('result', [])]
                }
            return {"source": "LeakCheck", "breaches": []}
        except Exception as e:
            return {"source": "LeakCheck", "error": str(e)}

def run(data):
    email = data.get("email")
    if not email:
        return "No email provided."

    # Validate email format
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_pattern, email):
        return {"error": "Invalid email format"}

    hunter = AdvancedEmailBreach()
    
    # Run all checks in parallel
    with ThreadPoolExecutor(max_workers=6) as executor:
        pastebin_future = executor.submit(hunter.search_pastebin, email)
        ghostbin_future = executor.submit(hunter.search_ghostbin, email)
        justpasteit_future = executor.submit(hunter.search_justpasteit, email)
        rentry_future = executor.submit(hunter.search_rentry, email)
        breachdirectory_future = executor.submit(hunter.search_breachdirectory, email)
        leakcheck_future = executor.submit(hunter.search_leakcheck, email)
        
        results = [
            pastebin_future.result(),
            ghostbin_future.result(),
            justpasteit_future.result(),
            rentry_future.result(),
            breachdirectory_future.result(),
            leakcheck_future.result()
        ]

    # Combine results
    combined_results = {
        "email": email,
        "sources_checked": len(results),
        "results": results,
        "total_links": sum(len(r.get("links", [])) for r in results if "links" in r),
        "total_breaches": sum(len(r.get("breaches", [])) for r in results if "breaches" in r)
    }

    return combined_results 
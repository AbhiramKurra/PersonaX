import requests
from bs4 import BeautifulSoup
import json
from concurrent.futures import ThreadPoolExecutor
import os
import subprocess
import re
import time
from urllib.parse import urljoin

class AdvancedDarkWebScanner:
    def __init__(self):
        self.setup_tools()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
        }

    def setup_tools(self):
        """Setup required tools if not already present"""
        if not os.path.exists("tools"):
            os.makedirs("tools")

    def search_ahmia(self, query):
        """Search using Ahmia"""
        try:
            url = f"https://ahmia.fi/search/?q={query}"
            response = requests.get(url, headers=self.headers, timeout=10)
            soup = BeautifulSoup(response.text, 'lxml')
            
            results = []
            for result in soup.find_all('div', class_='result'):
                link = result.find('a')
                if link and 'href' in link.attrs:
                    results.append({
                        'url': link['href'],
                        'title': link.text if link.text else 'No title',
                        'source': 'Ahmia'
                    })
            
            return {"source": "Ahmia", "results": results}
        except Exception as e:
            return {"source": "Ahmia", "error": str(e)}

    def search_darksearch(self, query):
        """Search using DarkSearch"""
        try:
            url = f"https://darksearch.io/api/search?query={query}"
            response = requests.get(url, headers=self.headers, timeout=10)
            data = response.json()
            
            results = []
            for result in data.get('results', []):
                results.append({
                    'url': result.get('link', ''),
                    'title': result.get('title', 'No title'),
                    'source': 'DarkSearch'
                })
            
            return {"source": "DarkSearch", "results": results}
        except Exception as e:
            return {"source": "DarkSearch", "error": str(e)}

    def search_torch(self, query):
        """Search using Torch"""
        try:
            url = f"http://xmh57jrzrnw6insl.onion/torrents.php?search={query}"
            response = requests.get(url, headers=self.headers, timeout=10)
            soup = BeautifulSoup(response.text, 'lxml')
            
            results = []
            for result in soup.find_all('tr', class_='torrent'):
                link = result.find('a')
                if link and 'href' in link.attrs:
                    results.append({
                        'url': urljoin(url, link['href']),
                        'title': link.text if link.text else 'No title',
                        'source': 'Torch'
                    })
            
            return {"source": "Torch", "results": results}
        except Exception as e:
            return {"source": "Torch", "error": str(e)}

    def search_darknetlive(self, query):
        """Search using DarkNetLive"""
        try:
            url = f"https://darknetlive.com/search/{query}"
            response = requests.get(url, headers=self.headers, timeout=10)
            soup = BeautifulSoup(response.text, 'lxml')
            
            results = []
            for result in soup.find_all('article'):
                link = result.find('a')
                if link and 'href' in link.attrs:
                    results.append({
                        'url': urljoin(url, link['href']),
                        'title': link.text if link.text else 'No title',
                        'source': 'DarkNetLive'
                    })
            
            return {"source": "DarkNetLive", "results": results}
        except Exception as e:
            return {"source": "DarkNetLive", "error": str(e)}

    def search_darkfaucet(self, query):
        """Search using DarkFaucet"""
        try:
            url = f"https://darkfaucet.onion/search?q={query}"
            response = requests.get(url, headers=self.headers, timeout=10)
            soup = BeautifulSoup(response.text, 'lxml')
            
            results = []
            for result in soup.find_all('div', class_='result'):
                link = result.find('a')
                if link and 'href' in link.attrs:
                    results.append({
                        'url': urljoin(url, link['href']),
                        'title': link.text if link.text else 'No title',
                        'source': 'DarkFaucet'
                    })
            
            return {"source": "DarkFaucet", "results": results}
        except Exception as e:
            return {"source": "DarkFaucet", "error": str(e)}

    def check_marketplace(self, query):
        """Check various dark web marketplaces"""
        marketplaces = [
            "http://darkmarket.onion",
            "http://empiremarket.onion",
            "http://silkroad.onion",
            "http://alphabay.onion",
            "http://dreammarket.onion"
        ]
        
        results = []
        for marketplace in marketplaces:
            try:
                url = f"{marketplace}/search?q={query}"
                response = requests.get(url, headers=self.headers, timeout=10)
                soup = BeautifulSoup(response.text, 'lxml')
                
                for result in soup.find_all('div', class_='listing'):
                    link = result.find('a')
                    if link and 'href' in link.attrs:
                        results.append({
                            'url': urljoin(url, link['href']),
                            'title': link.text if link.text else 'No title',
                            'source': f'Marketplace: {marketplace}'
                        })
            except Exception as e:
                continue
        
        return {"source": "Marketplaces", "results": results}

def run(data):
    query = data.get("query")
    if not query:
        return "No query provided."

    scanner = AdvancedDarkWebScanner()
    
    # Run all searches in parallel
    with ThreadPoolExecutor(max_workers=6) as executor:
        ahmia_future = executor.submit(scanner.search_ahmia, query)
        darksearch_future = executor.submit(scanner.search_darksearch, query)
        torch_future = executor.submit(scanner.search_torch, query)
        darknetlive_future = executor.submit(scanner.search_darknetlive, query)
        darkfaucet_future = executor.submit(scanner.search_darkfaucet, query)
        marketplace_future = executor.submit(scanner.check_marketplace, query)
        
        results = [
            ahmia_future.result(),
            darksearch_future.result(),
            torch_future.result(),
            darknetlive_future.result(),
            darkfaucet_future.result(),
            marketplace_future.result()
        ]

    # Combine results
    combined_results = {
        "query": query,
        "sources_checked": len(results),
        "results": results,
        "total_matches": sum(len(r.get("results", [])) for r in results if "results" in r),
        "marketplace_matches": len(results[5].get("results", [])) if "results" in results[5] else 0
    }

    return combined_results 
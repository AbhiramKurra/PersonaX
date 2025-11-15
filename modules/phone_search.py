import requests
from bs4 import BeautifulSoup
import re
from concurrent.futures import ThreadPoolExecutor

def validate_phone(phone):
    # Remove any non-digit characters except '+' at the start
    phone = re.sub(r'[^\d+]', '', phone)
    
    # Handle Indian numbers
    if phone.startswith('+91'):
        # Remove +91 and check if remaining is 10 digits
        number = phone[3:]
        if len(number) == 10:
            return number
    elif phone.startswith('91'):
        # Remove 91 and check if remaining is 10 digits
        number = phone[2:]
        if len(number) == 10:
            return number
    elif len(phone) == 10:
        # Direct 10-digit number
        return phone
    
    return None

def format_phone_for_search(phone):
    """Format phone number for different search platforms"""
    # For Indian numbers, ensure proper formatting
    if len(phone) == 10:
        return {
            'with_country': f"+91{phone}",
            'without_country': phone,
            'with_spaces': f"{phone[:5]} {phone[5:]}",
            'with_dashes': f"{phone[:5]}-{phone[5:]}"
        }
    return {'without_country': phone}

def search_truecaller(phone):
    formats = format_phone_for_search(phone)
    url = f"https://www.truecaller.com/search/{formats['with_country']}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'lxml')
            # Look for name and location information
            name = soup.find('h1', class_='profile-name')
            location = soup.find('div', class_='profile-location')
            return {
                "source": "Truecaller",
                "name": name.text if name else "Not found",
                "location": location.text if location else "Not found",
                "url": url
            }
    except Exception as e:
        return {"source": "Truecaller", "error": str(e)}

def search_whitepages(phone):
    formats = format_phone_for_search(phone)
    url = f"https://www.whitepages.com/phone/{formats['with_country']}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'lxml')
            # Look for name and address information
            name = soup.find('div', class_='name')
            address = soup.find('div', class_='address')
            return {
                "source": "Whitepages",
                "name": name.text if name else "Not found",
                "address": address.text if address else "Not found",
                "url": url
            }
    except Exception as e:
        return {"source": "Whitepages", "error": str(e)}

def search_411(phone):
    formats = format_phone_for_search(phone)
    url = f"https://www.411.com/phone/{formats['with_country']}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'lxml')
            # Look for name and address information
            name = soup.find('div', class_='name')
            address = soup.find('div', class_='address')
            return {
                "source": "411",
                "name": name.text if name else "Not found",
                "address": address.text if address else "Not found",
                "url": url
            }
    except Exception as e:
        return {"source": "411", "error": str(e)}

def search_social_media(phone):
    formats = format_phone_for_search(phone)
    # Search for phone number in social media profiles
    sites = {
        "Facebook": f"https://www.facebook.com/search/top?q={formats['with_country']}",
        "LinkedIn": f"https://www.linkedin.com/search/results/people/?keywords={formats['with_country']}",
        "Twitter": f"https://twitter.com/search?q={formats['with_country']}",
        "Instagram": f"https://www.instagram.com/explore/tags/{formats['with_country']}/"
    }
    
    results = {}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
    }
    
    for site, url in sites.items():
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                results[site] = url
        except Exception as e:
            continue
    
    return {"source": "Social Media", "results": results}

def search_business_listings(phone):
    formats = format_phone_for_search(phone)
    # Search for phone number in business directories
    sites = {
        "Yellow Pages": f"https://www.yellowpages.com/search?search_terms={formats['with_country']}",
        "Yelp": f"https://www.yelp.com/search?find_desc={formats['with_country']}",
        "Google Business": f"https://www.google.com/search?q={formats['with_country']}"
    }
    
    results = {}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
    }
    
    for site, url in sites.items():
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                results[site] = url
        except Exception as e:
            continue
    
    return {"source": "Business Listings", "results": results}

def run(data):
    phone = data.get("phone")
    if not phone:
        return "No phone number provided."

    # Validate and format phone number
    formatted_phone = validate_phone(phone)
    if not formatted_phone:
        return {"error": "Invalid phone number format. Please enter a valid 10-digit Indian phone number with or without country code (+91 or 91)"}

    # List of search functions
    search_functions = [
        search_truecaller,
        search_whitepages,
        search_411,
        search_social_media,
        search_business_listings
    ]

    # Run searches in parallel
    with ThreadPoolExecutor(max_workers=5) as executor:
        results = list(executor.map(lambda f: f(formatted_phone), search_functions))

    # Combine results
    combined_results = {
        "phone": formatted_phone,
        "sources_checked": len(search_functions),
        "results": results
    }

    return combined_results 
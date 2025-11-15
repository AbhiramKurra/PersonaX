import subprocess
import json
import os
from concurrent.futures import ThreadPoolExecutor
import requests
from bs4 import BeautifulSoup

class AdvancedUsernameHunter:
    def __init__(self):
        self.maigret_path = "tools/maigret"
        self.sherlock_path = "tools/sherlock"
        self.setup_tools()

    def setup_tools(self):
        """Setup required tools if not already present"""
        if not os.path.exists("tools"):
            os.makedirs("tools")
        
        # Clone Maigret if not present
        if not os.path.exists(self.maigret_path):
            subprocess.run(["git", "clone", "https://github.com/soxoj/maigret.git", self.maigret_path])
        
        # Clone Sherlock if not present
        if not os.path.exists(self.sherlock_path):
            subprocess.run(["git", "clone", "https://github.com/sherlock-project/sherlock.git", self.sherlock_path])

    def run_maigret(self, username):
        """Run Maigret to find username across 500+ platforms"""
        try:
            result = subprocess.run(
                ["python", f"{self.maigret_path}/maigret.py", username, "--json"],
                capture_output=True,
                text=True
            )
            return json.loads(result.stdout)
        except Exception as e:
            return {"error": str(e)}

    def run_sherlock(self, username):
        """Run Sherlock for quick username checks"""
        try:
            result = subprocess.run(
                ["python", f"{self.sherlock_path}/sherlock/sherlock.py", username, "--json"],
                capture_output=True,
                text=True
            )
            return json.loads(result.stdout)
        except Exception as e:
            return {"error": str(e)}

    def check_additional_sources(self, username):
        """Check additional sources not covered by Maigret or Sherlock"""
        sources = {
            "GitHub": f"https://github.com/{username}",
            "GitLab": f"https://gitlab.com/{username}",
            "Bitbucket": f"https://bitbucket.org/{username}",
            "Dev.to": f"https://dev.to/{username}",
            "Medium": f"https://medium.com/@{username}",
            "StackOverflow": f"https://stackoverflow.com/users/{username}",
            "Reddit": f"https://www.reddit.com/user/{username}",
            "Twitter": f"https://twitter.com/{username}",
            "Instagram": f"https://instagram.com/{username}",
            "LinkedIn": f"https://linkedin.com/in/{username}",
            "Facebook": f"https://facebook.com/{username}",
            "TikTok": f"https://tiktok.com/@{username}",
            "YouTube": f"https://youtube.com/@{username}",
            "Twitch": f"https://twitch.tv/{username}",
            "Steam": f"https://steamcommunity.com/id/{username}",
            "Spotify": f"https://open.spotify.com/user/{username}",
            "SoundCloud": f"https://soundcloud.com/{username}",
            "Vimeo": f"https://vimeo.com/{username}",
            "Behance": f"https://behance.net/{username}",
            "Dribbble": f"https://dribbble.com/{username}",
            "Flickr": f"https://flickr.com/photos/{username}",
            "DeviantArt": f"https://deviantart.com/{username}",
            "Pinterest": f"https://pinterest.com/{username}",
            "Quora": f"https://quora.com/profile/{username}",
            "ProductHunt": f"https://producthunt.com/@{username}",
            "AngelList": f"https://angel.co/{username}",
            "Crunchbase": f"https://crunchbase.com/person/{username}",
            "About.me": f"https://about.me/{username}",
            "Keybase": f"https://keybase.io/{username}",
            "Slideshare": f"https://slideshare.net/{username}",
            "SpeakerDeck": f"https://speakerdeck.com/{username}",
            "CodePen": f"https://codepen.io/{username}",
            "Replit": f"https://replit.com/@{username}",
            "CodeSandbox": f"https://codesandbox.io/u/{username}",
            "Glitch": f"https://glitch.com/@{username}",
            "Kaggle": f"https://kaggle.com/{username}",
            "ResearchGate": f"https://researchgate.net/profile/{username}",
            "Academia.edu": f"https://academia.edu/{username}",
            "GoogleScholar": f"https://scholar.google.com/citations?user={username}",
            "ORCID": f"https://orcid.org/{username}",
            "Mendeley": f"https://mendeley.com/profiles/{username}",
            "SlideShare": f"https://slideshare.net/{username}",
            "SpeakerDeck": f"https://speakerdeck.com/{username}",
            "Prezi": f"https://prezi.com/u/{username}",
            "Scribd": f"https://scribd.com/{username}",
            "Issuu": f"https://issuu.com/{username}",
            "Behance": f"https://behance.net/{username}",
            "Dribbble": f"https://dribbble.com/{username}",
            "ArtStation": f"https://artstation.com/{username}",
            "DeviantArt": f"https://deviantart.com/{username}",
            "Flickr": f"https://flickr.com/photos/{username}",
            "500px": f"https://500px.com/{username}",
            "VSCO": f"https://vsco.co/{username}",
            "EyeEm": f"https://eyeem.com/u/{username}",
            "Pexels": f"https://pexels.com/@{username}",
            "Unsplash": f"https://unsplash.com/@{username}",
            "Shutterstock": f"https://shutterstock.com/g/{username}",
            "AdobeStock": f"https://stock.adobe.com/contributor/{username}",
            "iStock": f"https://istockphoto.com/portfolio/{username}",
            "Alamy": f"https://alamy.com/portfolio/{username}",
            "GettyImages": f"https://gettyimages.com/portfolio/{username}",
            "DepositPhotos": f"https://depositphotos.com/portfolio/{username}",
            "123RF": f"https://123rf.com/profile_{username}",
            "Dreamstime": f"https://dreamstime.com/{username}",
            "Bigstock": f"https://bigstockphoto.com/portfolio/{username}",
            "Pond5": f"https://pond5.com/artist/{username}",
            "AudioJungle": f"https://audiojungle.net/user/{username}",
            "Envato": f"https://envato.com/user/{username}",
            "CreativeMarket": f"https://creativemarket.com/{username}",
            "Gumroad": f"https://gumroad.com/{username}",
            "Patreon": f"https://patreon.com/{username}",
            "Ko-fi": f"https://ko-fi.com/{username}",
            "BuyMeACoffee": f"https://buymeacoffee.com/{username}",
            "Substack": f"https://substack.com/profile/{username}",
            "Medium": f"https://medium.com/@{username}",
            "WordPress": f"https://{username}.wordpress.com",
            "Blogger": f"https://{username}.blogspot.com",
            "Tumblr": f"https://{username}.tumblr.com",
            "Ghost": f"https://{username}.ghost.io",
            "Wix": f"https://{username}.wixsite.com",
            "Squarespace": f"https://{username}.squarespace.com",
            "Weebly": f"https://{username}.weebly.com",
            "Shopify": f"https://{username}.myshopify.com",
            "Etsy": f"https://etsy.com/shop/{username}",
            "Redbubble": f"https://redbubble.com/people/{username}",
            "Society6": f"https://society6.com/{username}",
            "Zazzle": f"https://zazzle.com/{username}",
            "CafePress": f"https://cafepress.com/{username}",
            "Spreadshirt": f"https://spreadshirt.com/shop/{username}",
            "Threadless": f"https://threadless.com/artist/{username}",
            "DesignByHumans": f"https://designbyhumans.com/shop/{username}",
            "Teespring": f"https://teespring.com/stores/{username}",
            "Printful": f"https://printful.com/{username}",
            "Printify": f"https://printify.com/{username}",
            "CustomInk": f"https://customink.com/{username}",
            "Vistaprint": f"https://vistaprint.com/{username}",
            "Shutterfly": f"https://shutterfly.com/{username}",
            "Snapfish": f"https://snapfish.com/{username}",
            "Walgreens": f"https://walgreens.com/{username}",
            "CVS": f"https://cvs.com/{username}",
            "Walmart": f"https://walmart.com/{username}",
            "Target": f"https://target.com/{username}",
            "Amazon": f"https://amazon.com/{username}",
            "eBay": f"https://ebay.com/usr/{username}",
            "Etsy": f"https://etsy.com/shop/{username}",
            "Poshmark": f"https://poshmark.com/closet/{username}",
            "Mercari": f"https://mercari.com/u/{username}",
            "Depop": f"https://depop.com/{username}",
            "Grailed": f"https://grailed.com/{username}",
            "StockX": f"https://stockx.com/{username}",
            "GOAT": f"https://goat.com/{username}",
            "FlightClub": f"https://flightclub.com/{username}",
            "StadiumGoods": f"https://stadiumgoods.com/{username}",
            "Klekt": f"https://klekt.com/{username}",
            "Bump": f"https://bump.com/{username}",
            "SoleSupremacy": f"https://solesupremacy.com/{username}",
            "UrbanNecessities": f"https://urbannecessities.com/{username}",
            "RIF": f"https://rif.la/{username}",
            "ProjectBlitz": f"https://projectblitz.com/{username}",
            "Kixify": f"https://kixify.com/{username}"
        }
        
        results = {}
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
        }
        
        with ThreadPoolExecutor(max_workers=10) as executor:
            def check_site(site_info):
                site_name, url = site_info
                try:
                    response = requests.get(url, headers=headers, timeout=5)
                    if response.status_code == 200:
                        return site_name, url
                except:
                    pass
                return None
            
            futures = [executor.submit(check_site, (site, url)) for site, url in sources.items()]
            for future in futures:
                result = future.result()
                if result:
                    site_name, url = result
                    results[site_name] = url
        
        return results

def run(data):
    username = data.get("username")
    if not username:
        return "No username provided."

    hunter = AdvancedUsernameHunter()
    
    # Run all checks in parallel
    with ThreadPoolExecutor(max_workers=3) as executor:
        maigret_future = executor.submit(hunter.run_maigret, username)
        sherlock_future = executor.submit(hunter.run_sherlock, username)
        additional_future = executor.submit(hunter.check_additional_sources, username)
        
        maigret_results = maigret_future.result()
        sherlock_results = sherlock_future.result()
        additional_results = additional_future.result()

    # Combine results
    combined_results = {
        "username": username,
        "maigret_results": maigret_results,
        "sherlock_results": sherlock_results,
        "additional_results": additional_results,
        "total_sources_checked": len(maigret_results) + len(sherlock_results) + len(additional_results)
    }

    return combined_results 
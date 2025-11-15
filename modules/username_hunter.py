import requests
import time
from concurrent.futures import ThreadPoolExecutor

def check_site(site_info):
    site_name, url, headers = site_info
    try:
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code == 200:
            return site_name, url, True
        return site_name, url, False
    except Exception as e:
        return site_name, url, False

def run(data):
    username = data.get("username")
    if not username:
        return "No username provided."

    sites = {
        "GitHub": f"https://github.com/{username}",
        "Reddit": f"https://www.reddit.com/user/{username}",
        "Twitter": f"https://twitter.com/{username}",
        "Instagram": f"https://instagram.com/{username}",
        "LinkedIn": f"https://linkedin.com/in/{username}",
        "Facebook": f"https://facebook.com/{username}",
        "TikTok": f"https://tiktok.com/@{username}",
        "YouTube": f"https://youtube.com/@{username}",
        "Medium": f"https://medium.com/@{username}",
        "Dev.to": f"https://dev.to/{username}",
        "Pinterest": f"https://pinterest.com/{username}",
        "Quora": f"https://quora.com/profile/{username}",
        "Steam": f"https://steamcommunity.com/id/{username}",
        "Spotify": f"https://open.spotify.com/user/{username}",
        "SoundCloud": f"https://soundcloud.com/{username}",
        "Twitch": f"https://twitch.tv/{username}",
        "Vimeo": f"https://vimeo.com/{username}",
        "Behance": f"https://behance.net/{username}",
        "Dribbble": f"https://dribbble.com/{username}",
        "Flickr": f"https://flickr.com/photos/{username}",
        "DeviantArt": f"https://deviantart.com/{username}",
        "GitLab": f"https://gitlab.com/{username}",
        "Bitbucket": f"https://bitbucket.org/{username}",
        "HackerNews": f"https://news.ycombinator.com/user?id={username}",
        "ProductHunt": f"https://producthunt.com/@{username}",
        "AngelList": f"https://angel.co/{username}",
        "Crunchbase": f"https://crunchbase.com/person/{username}",
        "About.me": f"https://about.me/{username}",
        "Keybase": f"https://keybase.io/{username}",
        "Slideshare": f"https://slideshare.net/{username}",
        "SpeakerDeck": f"https://speakerdeck.com/{username}",
        "StackOverflow": f"https://stackoverflow.com/users/{username}",
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
        "Kixify": f"https://kixify.com/{username}",
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }

    found = {}
    site_infos = [(site, url, headers) for site, url in sites.items()]

    # Use ThreadPoolExecutor for parallel requests
    with ThreadPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(check_site, site_infos))

    # Process results
    for site_name, url, exists in results:
        if exists:
            found[site_name] = url

    return {
        "found_profiles": found,
        "total_checked": len(sites),
        "found_count": len(found),
        "username": username
    } 
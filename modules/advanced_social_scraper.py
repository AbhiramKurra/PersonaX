import asyncio
import aiohttp
from bs4 import BeautifulSoup
import json
import re
from datetime import datetime

class AdvancedSocialScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': 'max-age=0'
        }

    async def scrape_twitter(self, session, username):
        try:
            url = f'https://twitter.com/{username}'
            async with session.get(url, headers=self.headers, allow_redirects=True) as response:
                if response.status == 404:
                    return {'error': 'User not found'}
                html = await response.text()
                soup = BeautifulSoup(html, 'html.parser')
                
                # Extract profile info
                profile = {
                    'name': self._get_text(soup, 'span[data-testid="UserName"]'),
                    'description': self._get_text(soup, 'div[data-testid="UserDescription"]'),
                    'location': self._get_text(soup, 'span[data-testid="UserLocation"]'),
                    'followers': self._get_text(soup, 'a[href$="/followers"]'),
                    'following': self._get_text(soup, 'a[href$="/following"]')
                }
                
                # Extract recent tweets
                posts = []
                tweet_elements = soup.find_all('article', {'data-testid': 'tweet'})
                for tweet in tweet_elements[:5]:  # Get first 5 tweets
                    posts.append({
                        'text': self._get_text(tweet, 'div[data-testid="tweetText"]'),
                        'date': self._get_text(tweet, 'time'),
                        'likes': self._get_text(tweet, 'div[data-testid="like"]')
                    })
                
                return {
                    'profile': profile,
                    'posts': posts
                }
        except Exception as e:
            return {'error': str(e)}

    async def scrape_instagram(self, session, username):
        try:
            url = f'https://www.instagram.com/{username}/'
            async with session.get(url, headers=self.headers, allow_redirects=True) as response:
                if response.status == 404:
                    return {'error': 'User not found'}
                html = await response.text()
                soup = BeautifulSoup(html, 'html.parser')
                
                # Extract profile info
                profile = {
                    'name': self._get_text(soup, 'h2'),
                    'description': self._get_text(soup, 'h1'),
                    'followers': self._get_text(soup, 'span[title*="followers"]'),
                    'following': self._get_text(soup, 'span[title*="following"]')
                }
                
                # Extract recent posts
                posts = []
                post_elements = soup.find_all('article')
                for post in post_elements[:5]:  # Get first 5 posts
                    posts.append({
                        'text': self._get_text(post, 'img[alt]'),
                        'date': self._get_text(post, 'time'),
                        'likes': self._get_text(post, 'span[title*="likes"]')
                    })
                
                return {
                    'profile': profile,
                    'posts': posts
                }
        except Exception as e:
            return {'error': str(e)}

    async def scrape_reddit(self, session, username):
        try:
            url = f'https://www.reddit.com/user/{username}/'
            async with session.get(url, headers=self.headers, allow_redirects=True) as response:
                if response.status == 404:
                    return {'error': 'User not found'}
                html = await response.text()
                soup = BeautifulSoup(html, 'html.parser')
                
                # Extract profile info
                profile = {
                    'name': username,
                    'description': self._get_text(soup, 'div[data-test-id="user-profile-about"]'),
                    'karma': self._get_text(soup, 'span[data-test-id="user-karma"]')
                }
                
                # Extract recent posts
                posts = []
                post_elements = soup.find_all('div[data-test-id="post"]')
                for post in post_elements[:5]:  # Get first 5 posts
                    posts.append({
                        'text': self._get_text(post, 'h3'),
                        'date': self._get_text(post, 'time'),
                        'likes': self._get_text(post, 'span[data-test-id="post-score"]')
                    })
                
                return {
                    'profile': profile,
                    'posts': posts
                }
        except Exception as e:
            return {'error': str(e)}

    async def scrape_facebook(self, session, username):
        try:
            url = f'https://www.facebook.com/{username}'
            async with session.get(url, headers=self.headers, allow_redirects=True) as response:
                if response.status == 404:
                    return {'error': 'User not found'}
                html = await response.text()
                soup = BeautifulSoup(html, 'html.parser')
                
                # Extract profile info
                profile = {
                    'name': self._get_text(soup, 'h1'),
                    'description': self._get_text(soup, 'div[data-testid="bio"]'),
                    'location': self._get_text(soup, 'div[data-testid="current_city"]')
                }
                
                # Extract recent posts
                posts = []
                post_elements = soup.find_all('div[data-testid="post_message"]')
                for post in post_elements[:5]:  # Get first 5 posts
                    posts.append({
                        'text': self._get_text(post, 'div[data-testid="post_message"]'),
                        'date': self._get_text(post, 'abbr'),
                        'likes': self._get_text(post, 'span[data-testid="UFI2ReactionsCount"]')
                    })
                
                return {
                    'profile': profile,
                    'posts': posts
                }
        except Exception as e:
            return {'error': str(e)}

    async def scrape_linkedin(self, session, username):
        try:
            url = f'https://www.linkedin.com/in/{username}'
            async with session.get(url, headers=self.headers, allow_redirects=True) as response:
                if response.status == 404:
                    return {'error': 'User not found'}
                html = await response.text()
                soup = BeautifulSoup(html, 'html.parser')
                
                # Extract profile info
                profile = {
                    'name': self._get_text(soup, 'h1'),
                    'description': self._get_text(soup, 'div[data-test-id="about"]'),
                    'location': self._get_text(soup, 'span[data-test-id="location"]'),
                    'title': self._get_text(soup, 'div[data-test-id="headline"]')
                }
                
                # Extract recent posts
                posts = []
                post_elements = soup.find_all('div[data-test-id="feed-post"]')
                for post in post_elements[:5]:  # Get first 5 posts
                    posts.append({
                        'text': self._get_text(post, 'div[data-test-id="feed-post-content"]'),
                        'date': self._get_text(post, 'time'),
                        'likes': self._get_text(post, 'span[data-test-id="social-actions"]')
                    })
                
                return {
                    'profile': profile,
                    'posts': posts
                }
        except Exception as e:
            return {'error': str(e)}

    def _get_text(self, element, selector):
        try:
            found = element.select_one(selector)
            return found.get_text(strip=True) if found else ''
        except:
            return ''

async def run(data):
    username = data.get("username")
    if not username:
        return "No username provided."

    scraper = AdvancedSocialScraper()
    
    # Run all scrapers in parallel
    tasks = [
        scraper.scrape_twitter(username),
        scraper.scrape_instagram(username),
        scraper.scrape_reddit(username),
        scraper.scrape_facebook(username),
        scraper.scrape_linkedin(username)
    ]
    
    results = await asyncio.gather(*tasks)

    # Combine results
    combined_results = {
        "username": username,
        "sources_checked": len(results),
        "results": results,
        "total_posts": sum(
            len(r.get("results", {}).get("posts", [])) 
            for r in results 
            if "results" in r and "posts" in r["results"]
        )
    }

    return combined_results 
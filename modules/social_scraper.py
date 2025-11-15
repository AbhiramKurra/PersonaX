import asyncio
import aiohttp
from bs4 import BeautifulSoup
from modules.advanced_social_scraper import AdvancedSocialScraper

async def run(data):
    try:
        username = data.get('username')
        if not username:
            return {
                'error': 'No username provided',
                'platforms': []
            }

        scraper = AdvancedSocialScraper()
        
        # Set timeout for all requests
        timeout = aiohttp.ClientTimeout(total=30)  # 30 seconds timeout
        
        # Configure session without proxy
        connector = aiohttp.TCPConnector(ssl=False)  # Disable SSL verification for testing
        async with aiohttp.ClientSession(timeout=timeout, connector=connector) as session:
            # Create tasks for each platform
            tasks = [
                scraper.scrape_twitter(session, username),
                scraper.scrape_instagram(session, username),
                scraper.scrape_reddit(session, username),
                scraper.scrape_facebook(session, username),
                scraper.scrape_linkedin(session, username)
            ]
            
            # Wait for all tasks to complete with a timeout
            try:
                results = await asyncio.wait_for(asyncio.gather(*tasks, return_exceptions=True), timeout=60)
            except asyncio.TimeoutError:
                return {
                    'error': 'Search timed out after 60 seconds',
                    'platforms': []
                }
            
            # Process results
            platforms = []
            for platform, result in zip(['Twitter', 'Instagram', 'Reddit', 'Facebook', 'LinkedIn'], results):
                if isinstance(result, Exception):
                    platforms.append({
                        'platform': platform,
                        'status': 'Error',
                        'message': str(result)
                    })
                else:
                    platforms.append({
                        'platform': platform,
                        'status': 'Success',
                        'profile': result.get('profile', {}),
                        'posts': result.get('posts', [])
                    })
            
            return {
                'username': username,
                'platforms': platforms,
                'total_platforms': len(platforms),
                'total_posts': sum(len(p.get('posts', [])) for p in platforms if p.get('status') == 'Success')
            }
            
    except Exception as e:
        return {
            'error': str(e),
            'platforms': []
        } 
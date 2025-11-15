import requests
from bs4 import BeautifulSoup
import base64
import json
from concurrent.futures import ThreadPoolExecutor
import os
import subprocess
from PIL import Image
import io

class AdvancedImageSearch:
    def __init__(self):
        self.setup_tools()

    def setup_tools(self):
        """Setup required tools if not already present"""
        if not os.path.exists("tools"):
            os.makedirs("tools")

    def search_google_images(self, image_path):
        """Search using Google Images"""
        try:
            # Convert image to base64
            with open(image_path, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode()
            
            url = "https://images.google.com/searchbyimage/upload"
            files = {
                'encoded_image': (image_path, open(image_path, 'rb')),
                'image_content': ''
            }
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
            }
            
            response = requests.post(url, files=files, headers=headers)
            soup = BeautifulSoup(response.text, 'lxml')
            
            results = []
            for result in soup.find_all('div', class_='g'):
                link = result.find('a')
                if link and 'href' in link.attrs:
                    results.append({
                        'url': link['href'],
                        'title': link.text if link.text else 'No title',
                        'source': 'Google Images'
                    })
            
            return {"source": "Google Images", "results": results}
        except Exception as e:
            return {"source": "Google Images", "error": str(e)}

    def search_tineye(self, image_path):
        """Search using TinEye"""
        try:
            url = "https://www.tineye.com/search"
            files = {
                'image': (image_path, open(image_path, 'rb')),
            }
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
            }
            
            response = requests.post(url, files=files, headers=headers)
            soup = BeautifulSoup(response.text, 'lxml')
            
            results = []
            for result in soup.find_all('div', class_='match'):
                link = result.find('a')
                if link and 'href' in link.attrs:
                    results.append({
                        'url': link['href'],
                        'title': link.text if link.text else 'No title',
                        'source': 'TinEye'
                    })
            
            return {"source": "TinEye", "results": results}
        except Exception as e:
            return {"source": "TinEye", "error": str(e)}

    def search_bing_images(self, image_path):
        """Search using Bing Images"""
        try:
            url = "https://www.bing.com/images/searchbyimage"
            files = {
                'image': (image_path, open(image_path, 'rb')),
            }
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
            }
            
            response = requests.post(url, files=files, headers=headers)
            soup = BeautifulSoup(response.text, 'lxml')
            
            results = []
            for result in soup.find_all('div', class_='iusc'):
                link = result.find('a')
                if link and 'href' in link.attrs:
                    results.append({
                        'url': link['href'],
                        'title': link.text if link.text else 'No title',
                        'source': 'Bing Images'
                    })
            
            return {"source": "Bing Images", "results": results}
        except Exception as e:
            return {"source": "Bing Images", "error": str(e)}

    def search_yandex_images(self, image_path):
        """Search using Yandex Images"""
        try:
            url = "https://yandex.com/images/search"
            files = {
                'upfile': (image_path, open(image_path, 'rb')),
            }
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
            }
            
            response = requests.post(url, files=files, headers=headers)
            soup = BeautifulSoup(response.text, 'lxml')
            
            results = []
            for result in soup.find_all('div', class_='serp-item'):
                link = result.find('a')
                if link and 'href' in link.attrs:
                    results.append({
                        'url': link['href'],
                        'title': link.text if link.text else 'No title',
                        'source': 'Yandex Images'
                    })
            
            return {"source": "Yandex Images", "results": results}
        except Exception as e:
            return {"source": "Yandex Images", "error": str(e)}

    def extract_metadata(self, image_path):
        """Extract metadata from image"""
        try:
            image = Image.open(image_path)
            metadata = {
                'format': image.format,
                'mode': image.mode,
                'size': image.size,
                'info': image.info
            }
            return {"source": "Image Metadata", "metadata": metadata}
        except Exception as e:
            return {"source": "Image Metadata", "error": str(e)}

def run(data):
    image_path = data.get("image_path")
    if not image_path:
        return "No image path provided."

    if not os.path.exists(image_path):
        return {"error": "Image file not found"}

    searcher = AdvancedImageSearch()
    
    # Run all searches in parallel
    with ThreadPoolExecutor(max_workers=5) as executor:
        google_future = executor.submit(searcher.search_google_images, image_path)
        tineye_future = executor.submit(searcher.search_tineye, image_path)
        bing_future = executor.submit(searcher.search_bing_images, image_path)
        yandex_future = executor.submit(searcher.search_yandex_images, image_path)
        metadata_future = executor.submit(searcher.extract_metadata, image_path)
        
        results = [
            google_future.result(),
            tineye_future.result(),
            bing_future.result(),
            yandex_future.result(),
            metadata_future.result()
        ]

    # Combine results
    combined_results = {
        "image_path": image_path,
        "sources_checked": len(results),
        "results": results,
        "total_matches": sum(len(r.get("results", [])) for r in results if "results" in r),
        "metadata": results[4].get("metadata", {}) if "metadata" in results[4] else {}
    }

    return combined_results 
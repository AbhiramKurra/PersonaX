import requests
from bs4 import BeautifulSoup
import json
from concurrent.futures import ThreadPoolExecutor
import os
import re
import time
from PIL import Image
import exifread
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import folium
import webbrowser
import tempfile

class AdvancedGeoLocator:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
        }
        self.geolocator = Nominatim(user_agent="PersonaX")

    def extract_exif_data(self, image_path):
        """Extract EXIF data from image"""
        try:
            with open(image_path, 'rb') as image_file:
                tags = exifread.process_file(image_file)
            
            exif_data = {}
            for tag in tags.keys():
                if tag.startswith('EXIF'):
                    exif_data[tag] = str(tags[tag])
            
            # Extract GPS data if available
            if 'EXIF GPS GPSLatitude' in exif_data and 'EXIF GPS GPSLongitude' in exif_data:
                lat = self._convert_to_degrees(exif_data['EXIF GPS GPSLatitude'])
                lon = self._convert_to_degrees(exif_data['EXIF GPS GPSLongitude'])
                return {
                    'latitude': lat,
                    'longitude': lon,
                    'source': 'EXIF Data'
                }
            
            return {"source": "EXIF Data", "error": "No GPS data found"}
        except Exception as e:
            return {"source": "EXIF Data", "error": str(e)}

    def _convert_to_degrees(self, value):
        """Convert GPS coordinates to decimal degrees"""
        try:
            d = float(value.values[0].num) / float(value.values[0].den)
            m = float(value.values[1].num) / float(value.values[1].den)
            s = float(value.values[2].num) / float(value.values[2].den)
            return d + (m / 60.0) + (s / 3600.0)
        except:
            return None

    def search_google_maps(self, query):
        """Search location using Google Maps"""
        try:
            url = f"https://www.google.com/maps/search/{query}"
            response = requests.get(url, headers=self.headers, timeout=10)
            soup = BeautifulSoup(response.text, 'lxml')
            
            # Extract coordinates from the page
            script_tags = soup.find_all('script')
            for script in script_tags:
                if 'window.APP_INITIALIZATION_STATE' in str(script):
                    data = str(script).split('window.APP_INITIALIZATION_STATE=')[1].split(';')[0]
                    data = json.loads(data)
                    for item in data:
                        if isinstance(item, list) and len(item) > 0:
                            if isinstance(item[0], list) and len(item[0]) > 0:
                                if isinstance(item[0][0], list) and len(item[0][0]) > 0:
                                    lat = item[0][0][0]
                                    lon = item[0][0][1]
                                    return {
                                        'latitude': lat,
                                        'longitude': lon,
                                        'source': 'Google Maps'
                                    }
            
            return {"source": "Google Maps", "error": "No location found"}
        except Exception as e:
            return {"source": "Google Maps", "error": str(e)}

    def search_openstreetmap(self, query):
        """Search location using OpenStreetMap"""
        try:
            location = self.geolocator.geocode(query)
            if location:
                return {
                    'latitude': location.latitude,
                    'longitude': location.longitude,
                    'address': location.address,
                    'source': 'OpenStreetMap'
                }
            return {"source": "OpenStreetMap", "error": "No location found"}
        except Exception as e:
            return {"source": "OpenStreetMap", "error": str(e)}

    def search_geonames(self, query):
        """Search location using GeoNames"""
        try:
            url = f"http://api.geonames.org/searchJSON?q={query}&maxRows=1&username=demo"
            response = requests.get(url, headers=self.headers, timeout=10)
            data = response.json()
            
            if data.get('geonames'):
                location = data['geonames'][0]
                return {
                    'latitude': float(location['lat']),
                    'longitude': float(location['lng']),
                    'address': location['name'],
                    'source': 'GeoNames'
                }
            return {"source": "GeoNames", "error": "No location found"}
        except Exception as e:
            return {"source": "GeoNames", "error": str(e)}

    def create_map(self, locations):
        """Create an interactive map with the locations"""
        try:
            # Create a map centered on the first valid location
            valid_locations = [loc for loc in locations if 'latitude' in loc and 'longitude' in loc]
            if not valid_locations:
                return None
            
            center_lat = valid_locations[0]['latitude']
            center_lon = valid_locations[0]['longitude']
            
            m = folium.Map(location=[center_lat, center_lon], zoom_start=13)
            
            # Add markers for each location
            for loc in valid_locations:
                if 'latitude' in loc and 'longitude' in loc:
                    popup_text = f"Source: {loc.get('source', 'Unknown')}<br>"
                    if 'address' in loc:
                        popup_text += f"Address: {loc['address']}"
                    
                    folium.Marker(
                        [loc['latitude'], loc['longitude']],
                        popup=popup_text,
                        tooltip=loc.get('source', 'Unknown')
                    ).add_to(m)
            
            # Save the map to a temporary file
            temp_dir = tempfile.gettempdir()
            map_path = os.path.join(temp_dir, 'location_map.html')
            m.save(map_path)
            
            return map_path
        except Exception as e:
            return None

def run(data):
    query = data.get("query")
    image_path = data.get("image_path")
    
    if not query and not image_path:
        return "No query or image provided."

    locator = AdvancedGeoLocator()
    results = []
    
    # Run all searches in parallel
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = []
        
        if image_path:
            futures.append(executor.submit(locator.extract_exif_data, image_path))
        
        if query:
            futures.append(executor.submit(locator.search_google_maps, query))
            futures.append(executor.submit(locator.search_openstreetmap, query))
            futures.append(executor.submit(locator.search_geonames, query))
        
        results = [f.result() for f in futures]

    # Create map if we have valid locations
    map_path = locator.create_map(results)

    # Combine results
    combined_results = {
        "query": query,
        "image_path": image_path,
        "sources_checked": len(results),
        "results": results,
        "valid_locations": len([r for r in results if 'latitude' in r and 'longitude' in r]),
        "map_path": map_path
    }

    return combined_results 
"""
Class object to search, fetch and filter data from Etsy's website using API
"""

import os
import requests
import json
from typing import List, Dict, Any


class EtsySearch:
    def __init__(self):
        self.api_key = os.environ.get("ETSY_API_KEY")


    def get_listings(self, keywords: str, offset: int) -> Dict[str, Any]:
        listing_url = "https://openapi.etsy.com/v3/application/listings/active"
        headers = {"x-api-key": self.api_key}
        params = {
            "keywords": keywords,
            "sort_on": "created",
            "min_price": 20,
            "max_price": 60,
            "limit": 100, # Etsy's max limit is 100 listings
            "offset": offset # Variable to allow for searching more than 100
            }
        try:
            response = requests.get(listing_url, headers=headers, params=params)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"An error occurred: {e}")
            return {}


    def get_listing_properties(self, shop_id: int, listing_id: int) -> Dict[str, Any]:
        url = f"https://openapi.etsy.com/v3/application/shops/{shop_id}/listings/{listing_id}/properties"
        headers = {"x-api-key": self.api_key}
        try:
            response = requests.get(url=url, headers=headers)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"An error occurred: {e}")
            return {}


    def fetch_images(self, listing_id: int) -> Dict:
        url = f"https://openapi.etsy.com/v3/application/listings/{listing_id}/images"
        headers = {"x-api-key": self.api_key}
        try:
            response = requests.get(url=url, headers=headers)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"An error occurred: {e}")
            return {}


    def check_contain_keywords(self, must_have_word: List[str], keywords: List[str],
                                bomb_words: List[str], title: str, description: str) -> bool:
        description = description.lower()
        title = title.lower()
        must_have_present = any(word in title for word in must_have_word)
        keyword_present = any(keyword in title or keyword in description for keyword in keywords)
        bomb_present = any(bomb_word in title or bomb_word in description for bomb_word in bomb_words)
        if must_have_present and keyword_present and not bomb_present:
            return True
        else:
            return False


    def save_to_json(self, listings: Dict[str, Any], filename: str) -> str:
        filepath = "data/raw/"+filename
        try:
            with open(filepath, 'w') as json_file:
                json.dump(listings, json_file, indent=4)
            print(f"Data saved to {filepath}")
        except Exception as e:
            print(f"An error occurred while saving the file: {e}")
        return filepath
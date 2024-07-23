"""
This script retrieves data, filters and saves data from Etsy website.
"""

import os
import json
import urllib.request 
from datetime import datetime, timedelta
from src.etsy_search import EtsySearch


# Function to create a directory
def make_directory(path):
    try:
        os.makedirs(path, exist_ok=True)
    except Exception as e:
        print(f"An error occurred: {e}")
    return path


# Main function to run the script
def main():
    # Search all active listings for Laura Ashley Dresses
    search = EtsySearch()
    all_listings = []
    keywords = "vintage, laura, ashley, dress"
    offset = 0
    print("1. Initial Data Extraction:")

    # Retrieve all listings
    while True:
        listings = search.get_listings(keywords=keywords, offset=offset)
        if "results" in listings:
            all_listings.extend(listings["results"])
            offset += 100 # Etsy's maximum limit is to return 100 listings, therefore I'm using the offset param
            if len(all_listings) == listings["count"]:
                break
        else:
            print("Failed to retrieve listings.")
            break

    print(f"- Total active listings retrieved: {len(all_listings)}")

    # Saving all active listings
    combined_data = {
        "count": len(all_listings),
        "results": all_listings
    }
    etsy_listings = search.save_to_json(combined_data, "etsy_data/raw/etsy_listings.json")


    #----- Level 1 Filtering: by the time created and listing description -----
    with open("src/keywords.json", "r") as file:
        data = json.load(file)

    must_have_word = data["must_have_word"]
    keywords = data["keywords"]
    bomb_words = data["bomb_words"]

    filter1_listings = []
    timestamp = (datetime.now() - timedelta(days=7)).timestamp()

    with open(etsy_listings) as file:
        data = json.load(file)

    for idx, listing in enumerate(data["results"]):
        if search.check_contain_keywords(must_have_word, keywords, bomb_words, listing["title"], listing["description"]) and \
                listing["who_made"] == "someone_else" and listing["created_timestamp"] >= timestamp:
            item = {
                "listing_id": listing["listing_id"],
                "shop_id": listing["shop_id"],
                "title": listing["title"],
                "url": listing["url"]
            }
            filter1_listings.append(item)

    print("2. First Level Filtering:")
    print(f"Listings after 1st level filtering: {len(filter1_listings)}")


    #----- Level 2 Filtering: by the listing properties -----
    properties = []

    for listing in filter1_listings:
        response = search.get_listing_properties(listing["shop_id"], listing["listing_id"])
        properties.append(response)

    listings_properties = search.save_to_json(properties, "etsy_data/raw/filtered_listings_properties.json")

    with open(listings_properties) as file:
        filtered_data = json.load(file)

    filter2_index = []

    for idx, each_item in enumerate(filtered_data):
        for property in each_item["results"]:
            if property["property_name"] == "Women's clothing size":
                if property["values"] in [["XS"], ["S"], ["36"]] or \
                (property["scale_name"] == "UK" and property["values"] in [["10"], ["8"]]) or \
                (property["scale_name"] == "US numeric" and property["values"] == ["6"]):
                    filter2_index.append(idx)

    # Cascading the level 2 filter results from the list of listings
    filter2_listings = [filter1_listings[i] for i in filter2_index]

    print("3. Second Level Filtering:")
    print(f"- Listings after 2nd level filtering: {len(filter2_listings)}")

    #----- Saving Data to Local Directory -----
    # Creating new directory at date of search
    folder_name = datetime.now().strftime("%y%m%d")
    search_dir = make_directory(f"etsy_data/{folder_name}")
    image_dir = make_directory(f"{search_dir}/images")
    # Saving listings information
    search.save_to_json(filter2_listings, f"{search_dir}/listings.json")

    # Saving listings images
    listing_ids = [items["listing_id"] for items in filter2_listings]

    for listing_id in listing_ids:
        directory = make_directory(f"{image_dir}/{listing_id}")
        images = search.fetch_images(listing_id)
        image_urls = [image["url_570xN"] for image in images["results"]]
        for idx, url in enumerate(image_urls):
            file_path = os.path.join(directory, f"dress{idx}.jpg")
            urllib.request.urlretrieve(url, file_path)

    print("All fetching and saving operations have been completed successfully.")

if __name__ == "__main__":
    main()
"""
This script retrieves data, filters and saves data from Etsy website.
"""

import os
import json
import urllib.request 
from datetime import datetime, timedelta
from src.classes.etsy_search import EtsySearch, make_directory


# Main function to run the script
def main():
    search = EtsySearch()
    keywords = "vintage, laura, ashley, dress"
    offset = 0
    all_listings = []

    #----- Fetching all active listings searched with keywords -----
    print("0. Initial Data Extraction:")
    while True:
        listings = search.get_listings(keywords=keywords, offset=offset)
        # The response schema has 2 properties "count" (int, no. of total listings) and "results" (list)
        if "results" in listings:
            all_listings.extend(listings["results"])
            offset += 100   # Etsy's maximum limit is to return 100 listings, therefore I'm using the offset param
            if len(all_listings) == listings["count"]:
                break
        else:
            print("Failed to retrieve listings.")
            break
    print(f"- Total active listings retrieved: {len(all_listings)}")

    # Saving as raw data
    combined_data = {"count": len(all_listings), "results": all_listings}
    etsy_listings = search.save_to_json(combined_data, "etsy_data/raw/etsy_listings.json")


    #----- Level 1 Filtering: by the time created and listing description -----
    keyword = {
        "must_have_words": ["laura ashley"],
        "keywords": [   
            "laura ashley", "vintage dress", "uk 8", "uk 10", "size xs", "size s", "vintage 10",
            "waist", "13 inches", "13\"", "26 inches", "26\"", "pit to pit", "17 inches", "17\"", "cotton"
        ],
        "bomb_words": [
            "uk 12", "12 uk", "uk 14", "14 uk", "uk 16", "16 uk", "us 10", "10 us", " m ", " l ",
            "laura ashley style", "like laura ashley", "handmade"
        ]
    }

    filter1_listings = []   # Creating a variable to save listings that succeed lvl 1 filtering
    timestamp = (datetime.now() - timedelta(days=7)).timestamp()    # Limit results to within the past week

    with open(etsy_listings) as file:
        data = json.load(file)

    for listing in data["results"]:
        if search.check_keywords(
            keyword["must_have_words"], keyword["keywords"], keyword["bomb_words"],
            listing["title"], listing["description"]
        ) and listing["who_made"] == "someone_else" and listing["created_timestamp"] >= timestamp:
            filter1_listings.append({
                "listing_id": listing["listing_id"],
                "shop_id": listing["shop_id"],
                "title": listing["title"],
                "url": listing["url"]
            })
    print("1. First Level Filtering:")
    print(f"Listings after 1st level filtering: {len(filter1_listings)}")


    #----- Level 2 Filtering: by the listing properties -----
    properties = []
    # Retrieving further properties of listings that succeed lvl 1 filtering, using a different endpoint
    for listing in filter1_listings:
        response = search.get_listing_properties(listing["shop_id"], listing["listing_id"])
        properties.append(response)
    listings_properties = search.save_to_json(properties, "etsy_data/raw/filtered_listings_properties.json")
    
    with open(listings_properties) as file:
        filtered_data = json.load(file)

    filter2_index = [] # Creating a variable to save listing index that passes lvl 2 filtering
    for idx, each_item in enumerate(filtered_data):
        for property in each_item["results"]:
            if property["property_name"] == "Women's clothing size":
                if property["values"] in [["XS"], ["S"], ["36"]] or \
                (property["scale_name"] == "UK" and property["values"] in [["10"], ["8"]]) or \
                (property["scale_name"] == "US numeric" and property["values"] == ["6"]):
                    filter2_index.append(idx)

    # Cascading the level 2 filter results using the saved indexes
    filter2_listings = [filter1_listings[i] for i in filter2_index]

    print("2. Second Level Filtering:")
    print(f"- Listings after 2nd level filtering: {len(filter2_listings)}")


    #----- Saving Data to Local Directory -----
    folder_name = datetime.now().strftime("%y%m%d") # Creating new directory using date for identification
    search_dir = make_directory(f"etsy_data/{folder_name}")
    image_dir = make_directory(f"{search_dir}/images")
    search.save_to_json(filter2_listings, f"{search_dir}/listings.json")

    # Saving listings images
    for listing in filter2_listings:
        directory = make_directory(f"{image_dir}/{listing['listing_id']}")
        images = search.fetch_images(listing["listing_id"])
        image_urls = [image["url_570xN"] for image in images.get("results", [])]
        for idx, url in enumerate(image_urls):
            file_path = os.path.join(directory, f"dress{idx}.jpg")
            urllib.request.urlretrieve(url, file_path)

    print("All fetching and saving operations have been completed successfully.")


if __name__ == "__main__":
    main()
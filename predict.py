"""
This script follows the get_data.py, and runs the prediction model on the retrieved Etsy data.
"""

import os
import pickle
import pandas as pd
import numpy as np
from datetime import datetime
from PIL import Image
from skimage.transform import resize


# Function to process image into array matching the size for the trained model
def process_img(img_path, target_size=(256, 256)):
    try:
        image = Image.open(img_path)
        img_array = np.array(image)
        img_array = resize(img_array, target_size, anti_aliasing=True)
        img_array = img_array.flatten()
        return np.expand_dims(img_array, axis=0)
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


# Function to use the model and make predictions to listing images within a listing folder
# And return "True" if any of the images in that folder has been predicted as a logo, else "False"
def predict_listing(listing_folder, model):
    predictions = []
    for img in os.listdir(listing_folder):
        if img.endswith("jpg"): # All images saved from previous step are .jpg files
            img_path = os.path.join(listing_folder, img)
            img_array = process_img(img_path)
            predictions.append(model.predict(img_array))
    if any(predictions):
        return True
    else:
        return False

def main():
    # Load the classification model
    with open("src/logo_identifier.pkl", "rb") as file:
        model = pickle.load(file)

    # Set the root directory file path
    date = datetime.now().strftime("%y%m%d")
    root_dir = f"etsy_data/{date}"


    # Create a dictionary for saving the predictions
    predictions = {
        "listing_id": [],
        "prediction": []
    }

    # Make predictions and append to dictionary
    for folder in os.listdir(f"{root_dir}/images"):
        if folder.isdigit():
            # then it is a listing folder
            listing_folder = os.path.join(root_dir, "images", folder)
            predictions["listing_id"].append(int(folder))
            predictions["prediction"].append(predict_listing(listing_folder, model))


    # Make results into a dataframe, and load other properties of listings from json
    results = pd.DataFrame(predictions)
    data = pd.read_json(f"{root_dir}/listings.json")
    
    if not data.empty:
        df = pd.merge(data, results, on="listing_id")
        # Tidying up the dataframe in preparation for emailing
        df.sort_values(by="listing_id", inplace=True)
        df.reset_index(drop=True, inplace=True)
        df['title'] = df['title'].str.capitalize()
        # Write data to CSV
        df.to_csv(f"etsy_data/{date}/results.csv", index=False)
        print(f"Listing data including prediction results saved.")
    else: # There are no listings this wekk
        empty_df = pd.DataFrame(columns=["listing_id", "shop_id", "title", "url", "prediction"])
        empty_df.to_csv(f"etsy_data/{date}/results.csv", index=False)
        print("No listings found. Empty results.csv created.")


if __name__ == "__main__":
    main()
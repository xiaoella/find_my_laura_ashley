"""
This script follows the get_data.py, and runs the prediction model on the retrieved Etsy data.
"""

import os
import pickle
import pandas as pd
import numpy as np
from datetime import datetime
import tensorflow as tf
from tensorflow.keras.utils import load_img, img_to_array


# Function to process image into array matching the size for the trained model
def process_img(img_path, target_size=(256, 256)):
    try:
        image = load_img(img_path)
        img_array = img_to_array(image)
        img_array = tf.image.resize(img_array, target_size).numpy().flatten()
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


    # Combine prediction results with listing details
    results = pd.DataFrame(predictions)
    data = pd.read_json(f"{root_dir}/listings.json")

    df = pd.merge(data, results, on="listing_id")


    # Write data to CSV
    df.to_csv(f"etsy_data/{date}/results.csv", index=False)
    print(f"Listing data including prediction results saved.")


if __name__ == "__main__":
    main()
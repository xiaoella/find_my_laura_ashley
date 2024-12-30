"""
This script sends an email reporting the fetched and predicted listings.
"""

import pandas as pd
from datetime import datetime
from src.classes.emailer import Emailer

def main():
    # Getting today's date
    date = datetime.now().strftime("%y%m%d")
    root_dir = f"etsy_data/{date}"

    # Reading and sorting the CSV file
    df = pd.read_csv(f"{root_dir}/results.csv")

    # Preparing image paths
    img_paths = []
    for folder in df["listing_id"]:
        try:
            img_paths.append(f"{root_dir}/images/{folder}/dress0.jpg")
        except Exception as e:
            print("Error with image path: {e}")
    
    # Prepare email
    emailer = Emailer()
    html_content = emailer.email_content(df)

    # Send email
    emailer.send_email("Weekly Laura Ashley Digest", html_content, img_paths)

if __name__ == "__main__":
    main()
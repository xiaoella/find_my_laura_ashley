"""
This script combines the 3 scripts into one, it is designed to be scheduled and run automatically using a cron job or similar.
"""

from src import get_data, predict, send_email
import shutil
from dotenv import load_dotenv

def main():
    load_dotenv()
    get_data.main()
    predict.main()
    send_email.main()
    shutil.rmtree("etsy_data") # Clean up the directory

    return None

if __name__ == "__main__":
    main()
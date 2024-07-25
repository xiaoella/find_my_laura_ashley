# Find My Laura Ashley

### Where it started...
I have been collecting Laura Ashley dresses for a few years, especially the vintage-inspired floral dresses from the brand's 'golden era' - the 1980s. Vintage prairie dress lovers and collectors, like myself, are very fond of these dresses for their quality craftsmanship as well as the nostalgic, pictorial, and romantic style.

Finding a Laura Ashley dress that also fits perfectly is not easy. Since the brand stopped making these dresses after the 80s, and had gone out of business in 2020, these dresses are only available through second-hand sellers on platforms, like Etsy. The search is then further complicated by vintage sizing discrepancies: a 1980s Laura Ashley dress labelled as a 'UK 10' might fit a modern UK 8. Moreover, the brand's popularity leads some sellers to label other non-Laura-Ashely floral dresses as _'Laura Ashley style'_ or _'like Laura Ashley'_, adding another layer of complexity to the search.

This project aims to identify the perfect Laura Ashley dress by fetching data via API from Etsy's website, and filtering the downloaded .json file results based on the listings' descriptions such as size and measurements. After the filtering process, a Random Forest Classifier model was trained to try and detect if any images of the listed item contains the true Laura Ashley label which shows its 1980s logo.

<img src="src/images/80s_laura_ashley_tag.png" alt="logos" width="500"/>
<sup>image source: https://vintageclothingguides.com/tags-labels/how-to-tell-if-laura-ashley-is-vintage</sup>

<sup>This blog also contains some in-depth information on Laura Ashley tags and styles over the years, it's worth a read if you're interested!</sup>


## 1. Fetching and Filtering Data from Etsy
The first step is to fetch, filter and save data from Etsy's active listings. The `get_data.py` script is designed to exactly this. The script interacts with Etsy's Open API v3. To check if your API works, you could first run:

```
python test_etsy_api.py
```
It will then display if your API key is working or not.

Endpoint used and documentation references:
- [findAllListingsActive](https://developers.etsy.com/documentation/reference/#operation/findAllListingsActive)
- [getListingProperties](https://developers.etsy.com/documentation/reference/#operation/getListingProperties
)
- [getListingImages](https://developers.etsy.com/documentation/reference/#operation/getListingImages)


### Instructions to Run
To fetch and save data:

```
python get_data.py
```

### Features
**Data Fetching:** Retrieves active listings from Etsy using specific keywords related to vintage Laura Ashley dresses.

**Data Filtering:** Implements two levels of filtering:

- Level 1 Filtering: Filters listings based on title keywords, and creation timestamp. This script is designed to run once a week, so I only aim to fetch the listings that were created and posted within the last week.
- Level 2 Filtering: Further filters the listings based on specific property values like whether it is a clothing, and its listed size.

**Saving Data and Directory Management:** Saves the filtered listings along with their properties and associated images as .json files, and automatically creates directories based on the current date in order to organise the saved data.

**Sample output:**
```
1. Initial Data Extraction:
- Total active listings retrieved: 820
- Data saved to etsy_data/raw/etsy_listings.json
2. First Level Filtering:
Listings after 1st level filtering: 43
- Data saved to etsy_data/raw/filtered_listings_properties.json
3. Second Level Filtering:
- Listings after 2nd level filtering: 3
- Data saved to etsy_data/240723/listings.json
All fetching and saving operations have been completed successfully.
```

## 2. Making Predictions
The `predict.py` script is designed to run a classification model on the saved data from the previous step, identifying if any images contain the 1980s Laura Ashley tag.

### Classification Model
Hoping to automate the identification of authentic Laura Ashley dresses from online listings as much as possible, I trained a Random Forest model focusing on recognising the iconic Laura Ashley logo, particularly the one from the 1980s. This task will be very helpful in the process, because many sellers tend to upload these close-up photos of the label, as they serve as a key indicator of authenticity.

To train the model, I gathered a dataset comprising two categories:

| Label Images | Non-label Images |
|--------------|------------------|
| <sup>These images featured the distinctive Laura Ashley tags from the 80s. The images are mostly clear with the tag centred, making them idea for model training.</sup> | <sup>These include a variety of pictures of general product photography, not showing any Laura Ashley logos.</sup> |
| ![logos](src/images/logos.png) | ![dresses](src/images/dresses.png) |

I aimed to curate the dataset to closely mimic the type of images the model would encounter when deployed. Specifically, for the non-logo images, I selected examples that captured the typical noise and variability found in real-world data. These images showcase various elements such as the dress, intricate details, and different parts of the label, thereby providing a comprehensive representation of the non-logo context.

### Instructions to Run
```
python predict.py
```
Note: run the script after data has been fetched and saved.

This script will processes all images in each listing folder that's associated with each listing, using a Random Forest model. If the model detects a logo in any of the images for a given folder, it will classify that listing as 'True'. This indicates that it is likely a genuine Laura Ashley dress, as the presence of a logo in at least one image suggests authenticity.

At the end of the script, a .csv file is generated, which is prepared for emailing (the next step). This file summarises the prediction results, as illustrated in the example image below:
<img src="src/images/prediction_results.png" alt="prediction results"/>

## 3. Sending Results in an Email
The send_email.py script as a final step, will compose and send an email containing the results of the Etsy data analysis, including images of the listings. This script is executed after the data has been fetched and filtered, and predictions have been made.

The script includes basic error handling to catch and print errors related to email sending or file operations. It is also prepared for different scenarios: such as when there are no listings (the dataframe is empty), or only one of "True" or "False" predictions exist. If there are only truly predicted listings, the body will include details and images of these and will omit sections related to false predictions, and vice versa for only the "False" ones present.

### Instructions to Run
```
python send_email.py
```
Note: run the script after data has been fetched and saved, and predictions have been made.

**Sample Email**

When there is a comprehensive DataFrame that contains both "True" and "False" predictions, the email will have two sections. It starts with the listings that have a "True" prediction. The second section of the email includes the "False" predictions. It is possible that these listings are still authentic Laura Ashley dresses, but the seller might not have uploaded a picture of the logo.

| ![Email example](src/images/listings_1.png) | ![Email example](src/images/listings_2.png) |
|---------------------------------------------|---------------------------------------------|

Sample Email when there is only one section related to the predictions:
<img src="src/images/one_listing.png" alt="Email example" width="400"/>

Sample Email when there are no listings after fetching and filtering:
<img src="src/images/no_listing.png" alt="Email example" width="400"/>

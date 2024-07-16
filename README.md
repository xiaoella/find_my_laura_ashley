# Find My Laura Ashley

### Where it started...
I have been collecting Laura Ashley dresses for a few years, especially the vintage-inspired floral dresses from the brand's 'golden era' in the 1980s. Vintage fashion enthusiasts and collectors, like myself, are very fond of these dresses for their quality craftsmanship and their nostalgic, pictorial, and romantic style.

Finding a Laura Ashley dress that also fits perfectly is not easy. Since the brand stopped making these silhouettes and patterns after the 80s, and has gone out of business in 2020, these dresses are only available through second-hand sellers on platforms like Etsy. This search is further complicated by vintage sizing discrepancies: a 1980s Laura Ashley dress labelled as a 'UK 10' might fit a modern UK 8. Moreover, the brand's popularity leads some sellers to label non-Laura Ashley dresses as 'Laura Ashley Style' or 'like Laura Ashley', adding another layer of complexity to the search.

This project aims to identify the perfect Laura Ashley dress by fetching data from Etsy's website via the Etsy API, and filtering the results based on the listings' descriptions including sizes and measurements. It also use a Random Forest Classifier model to try to recognise if any images of the listed item contains the Laura Ashley label showing its 1980s logo.

## Classification Model
In an effort to automate the identification of authentic Laura Ashley dresses from online listings, I trained a random forest model focusing on recognising the iconic Laura Ashley logo, particularly the one from the 1980s. This task is crucial because many sellers tend to upload close-up photos of the label, which serves as a key indicator of authenticity.

### Data Collection and Preparation
To train the model, I gathered a dataset comprising two categories:

- Label Images: These images featured the distinctive Laura Ashley logo from the 1980s. The logos were mostly clear and centred, making them ideal for model training.

![logos](src/images/logo.png)

- Non-Label Images: These included a variety of Laura Ashley and Laura Ashley 'style' dress photos from Etsy listings. The images in this category did not contain the Laura Ashley logo and represented general product photography, capturing the typical noise and variability found in real-world data.

![dresses](src/images/dresses.png)

I aimed to curate the dataset to closely mimic the type of images the model would encounter when deployed.
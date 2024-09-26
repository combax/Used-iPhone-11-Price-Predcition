# eBay price prediction
Predicting used iPhone 11 price with Scrapped eBay data.

## This project contains:
- Data scarpping on [eBay.ca](https://www.ebay.ca/) using Python (*beautifulsoup4*).
- EDA of the data.
- XGBoost and Random Forest models for Price and Shipping cost prediction respectively.
- REST API deployment of the models using *FastAPI* (Python).

---

## Scraping eBay data:

- **scraper.py** is used to scrape eBay data till 300 pages because after that there are no listings.

- A basic filter is applied here to only select iPhone 11, 11 pro and 11 pro max models, exclude autions, and variable offers.

---

## Dataset created:

Dataset generated is stored in csv file but is not shared in the project for obvious reasons. (**6850 rows**)

It contains following columns:

- **iPhone** - Full title of the listing.
- **Condition** - Categorical variable (Brand New, New (Other), Open Box, Certified - Refurbished, Excellent - Refurbished, Very Good - Refurbished, Good - Refurbished, Refurbished, Pre-Owned, Parts Only).
- **Price** - Price in Candian Dollars. Format - C$500.
- **Seller_type** - If eBay classifies seller as *Top Rated Seller* or not.
- **Seller** - Name of the seller, number of reviews, rating of those review. Format - seller1(1000)94.6%.
- **Shipping** - Shipping cost of the Phones. Format - C$20.
- **Seller_rating** - eBay seller ratings in stars. Format - 4.5, 5, etc.
- **Seller_location** - Country of the seller. Format - from United States.

---

## EDA:

### Data Cleaning:

1. iPhone column:
   - Removing rows with "shop on eBay", with more than 1 value for storage, listings with "crack", "No Face ID", "Box Only".
   - Removing listings with more than 1 values for Storage in same listing.

2. Price column:
   - Removing "C", "&" from listings.
   - Removing non-numeric values to cast Price.

3. Shipping column:
   - Removing " ", "C", "$", "shipping", and "estimate" from rows.
   - Replacing "Free Shipping", nan, na rows with 0.
   - Type case Shipping as float.

4. Seller_location:
   - Removing "from" and empty spaces.
   - Replacing na with Canada.

5. seller column:
   - Stripping into Seller_name, Seller_reviews, Seller_rating.
   - Removing "%" from Seller_rating.

6. Storage column(new):
   - Extracting GB from iPhone column.
 
7. Carrier_status column(new):
   - Extracting "Unlocked" & "Locked" from iPhone.

---

### Understanding Data:

1. **iPhone models price distribution:**

![](/graphs/iphone_11_variants.png)

- We see lot of outliers on top and some on the bottom.

2. **iPhone conditions:**

![](/graphs/Conditons_iPhones.png)

- **Removal of outliers** - Considered but because top 100 and bottom 100 outliers have high numbers from ***Brand New*** and ***Parts Only*** conditions respectively.
- This would eliminate small number of cases they have in the data, which are important.

- Most iPhones are **Pre-Owned**.

3. **Carrier Status:**

![](/graphs/Carries_status.png)

4. **Shipping:**

![](/graphs/Shipping.png)

- Most sellers are from ***USA***, but seller country plays important role in shipping prices.

---

### Model Selection:


1. Results for ***LinearRegression***:
  - Price Model -> RMSE: 102.79598072034938, R^2: 0.41722499573136074, Adjusted R^2: 0.4087964316200374
  
  - Shipping Model -> RMSE: 9.728743433873511, R^2: 0.40216063461271667, Adjusted R^2: 0.39351419751000793

2. Results for ***RandomForest***:
  - Price Model -> RMSE: 76.99599477296677, R^2: 0.6730473088388476, Adjusted R^2: 0.668318654214616

  - ***Shipping Model -> RMSE: 7.589071483817029, R^2: 0.6362120623756692, Adjusted R^2: 0.6309506665835818***

3. Results for ***XGBoost***:
  - ***Price Model -> RMSE: 73.03391165574511, R^2: 0.7058304125866577, Adjusted R^2: 0.7015758937604317***
  
  - Shipping Model -> RMSE: 7.899921763075357, R^2: 0.6058000289018368, Adjusted R^2: 0.6000987896504171

**So Price model is better with XGBoost and Shipping model with Random Forest.**

---

## Hyper-paramter tuning:

1. Best hyperparameters for Price model: {'xgb__learning_rate': 0.1, 'xgb__max_depth': None, 'xgb__min_child_weight': 1, 'xgb__n_estimators': 100, 'xgb__subsample': 0.8}

   - ***XGBoost Price Model RMSE: 72.64967722008117, R2: 0.7089175471758347, Adjusted R2: 0.7047076769903612***

2. Best hyperparameters for Shipping model: {'rf__max_depth': 20, 'rf__min_samples_leaf': 2, 'rf__min_samples_split': 5, 'rf__n_estimators': 200}

   - ***Random Forest Shipping Model RMSE: 7.487505593540977, R2: 0.6458841815622949, Adjusted R2: 0.6422410147059399***

---

### REST API:

- Models and Label encoders were saved using joblib into *models* and *variables* folders respectively.
- **main.py** contains REST API implemented in FastAPI in Python.

---

#### Future ideas:

- To implement Neural Networks, Undersampling, or Oversampling to improve models.

import csv
import requests
from bs4 import BeautifulSoup
import time
import random

# Define the base URL and the filters
base_url = "https://www.ebay.ca/sch/i.html?"
filters = {
    "_dcat": "9355",  # Electronics category (cell phones)
    "_fsrp": "1",  # Free shipping filter
    "rt": "nc",  # Newly listed
    "_from": "R40",  # Search results
    "_nkw": "iPhone 11",  # Keyword search (specific to iPhone 11 models)
    "Model": "Apple iPhone 11|Apple iPhone 11 Pro|Apple iPhone 11 Pro Max",  # iPhone models
    "LH_BIN": "1",  # Buy It Now
}

# Build the complete URL with filters
for key, value in filters.items():
    base_url += f"&{key}={value}"

max_pages = 300  # Adjust as needed


with open("ebay_iphone11_new.csv", "w", newline="", encoding="utf-8") as csvfile:
    fieldnames = ["iPhone", "Condition", "Price", "Seller_type", "Seller", "Shipping", "Seller_review", "Seller_location"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for page_num in range(1, max_pages + 1):
        url = f"{base_url}&_pgn={page_num}"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        items = soup.find_all("li", class_="s-item")

        for item in items:
            title = item.find("span", {"aria-level": "3"}).text.strip()
            condition = item.find("span", class_="SECONDARY_INFO").text.strip() if item.find("span", class_="SECONDARY_INFO") else ""
            price = item.find("span", class_="s-item__price").text.strip()
            seller_type = item.find("span", class_="s-item__etrs-text").text.strip() if item.find("span", class_="s-item__etrs-text") else ""
            seller = item.find("span", class_="s-item__seller-info-text").text.strip() if item.find("span", class_="s-item__seller-info-text") else ""
            shipping = item.find("span", class_="s-item__shipping").text.strip() if item.find("span", class_="s-item__shipping") else ""
            seller_review = item.find("div", class_="x-star-rating").text.strip().split(" ")[0] if item.find("div", class_="x-star-rating") else ""
            seller_location = item.find("span", class_="s-item__location").text.strip() if item.find("span", class_="s-item__location") else ""

            writer.writerow({"iPhone": title, "Condition": condition, "Price": price, "Seller_type": seller_type, "Seller": seller, "Shipping": shipping, "Seller_review": seller_review, "Seller_location": seller_location})
            time.sleep(0.5)  # Delay between requests

        print(f"Page {page_num} scraped successfully.")
        time.sleep(0.5)  # Delay between pages

print("Scraping completed.")

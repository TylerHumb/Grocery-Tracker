import requests
from bs4 import BeautifulSoup
import csv
from datetime import date

def scrape_database():

    #for storing scraped data
    data = []

def call_api():
    # Example API for proof of concept, fetching all deli meat ID's
    api_url = "www.woolworths.com.au/apis/ui/browse/category"

    # Define the headers
    headers = {
        "categoryId": "1_696F07C",
        "pageNumber": "1",  
        "pageSize": "269", # changed to return all items instead of a select amount
        "sortType": "TraderRelevance",
        "url": "/shop/browse/deli-chilled-meals/deli-meats",
        "location": "/shop/browse/deli-chilled-meals/deli-meats",
        "formatObject": "{\"name\":\"Deli Meats\"}",
        "isSpecial": "false",
        "isBundle": "false",
        "isMobile": "false",
        "filters": "[]",
        "token": "",
        "gpBoost": "0",
        "isHideUnavailableProducts": "false",
        "isRegisteredRewardCardPromotion": "false",
        "enableAdReRanking": "false",
        "groupEdmVariants": "true",
        "categoryVersion": "v2",
        "flags": "{\"EnableProductBoostExperiment\":false}",
    }

    # Make the GET request with the provided headers
    response = requests.get(api_url, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        # Print or return the JSON response
        print(response.json())
    else:
        print(f"Error: Failed to fetch data (status code {response.status_code})")



def scrape_details(productid):
    base_url = "https://www.woolworths.com.au/api/v3/ui/schemaorg/product/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
    }

    apiurl = base_url + productid
    response = requests.get(apiurl, headers=headers)

    if response.status_code != 200:
        print(f"Error: Failed to fetch page (status code {response.status_code})")
        return None

    product_data = response.json()

    # Extracting product name
    if 'name' in product_data:
        product_name = product_data['name']
        print(f"Product Name: {product_name}")
    else:
        print("Product name not found.")
        return None

    # Extracting product price
    if 'offers' in product_data and 'price' in product_data['offers']:
        product_price = product_data['offers']['price']
        print(f"Product Price: {product_price}")
    else:
        print("Price not found.")
        return None

    # Timestamp each record so we can track price changes over time
    timestamp = str(date.today())
    print(f"Timestamp: {timestamp}")

    return [product_name, product_price, timestamp]

data = scrape_details("304977")
print(data)
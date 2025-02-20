import requests
import csv
from datetime import date
import urllib.parse
import Repository

def scrape_database():

    #for storing scraped data
    data = []

def fetch_ids():

    # Base URL for the API
    base_url = "https://www.woolworths.com.au/apis/ui/browse/category"

    # Parameters for the API call
    params = {
        "categoryId": "1_696F07C",
        "url": "/shop/browse/deli-chilled-meals/deli-meats",
        "formatObject": '{"name":"Deli Meats"}',
        "pageNumber": 1,
        "pageSize": 36,
        "sortType": "TraderRelevance",
        "location": "/shop/browse/deli-chilled-meals/deli-meats",
        "isSpecial": False,
        "isBundle": False,
        "isMobile": False,
        "filters": "[]", 
        "token": None, 
        "gpBoost": 0,
        "isHideUnavailableProducts": False,
        "enableAdReRanking": False,
        "groupEdmVariants": True,
        "categoryVersion": "v2",
        "flags": '{"EnableProductBoostExperiment":false}'
    }

    # Properly encode the parameters
    encoded_params = urllib.parse.urlencode(params, quote_via=urllib.parse.quote)

    # Combine base URL with encoded parameters
    final_url = f"{base_url}?{encoded_params}"

    # Headers for the request
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
    }

    # Make the GET request with headers
    response = requests.get(final_url, headers=headers)

    # Check if the response was a success
    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        return

    response = response.json()

    for product in response['Bundles']:
        Name = product["Name"]
        subclass = product["Products"]
        subclass2 = subclass[0]
        ID = subclass2["Stockcode"]
        Price = subclass2["CupPrice"]
        try:
            #if the product isnt already in the repository, add it to the repository
            if not Repository.checkProductExists(ID):
                Repository.createNewProduct(Name,ID)
            #timestamp the entry to track price's over time
            timestamp = str(date.today())
            Repository.addprice(ID,Price,timestamp)
        except Exception as e:
            print(str(e))
    print('price entry successful')


#----------------------------------------------------------------------------------------------------------------------------------------------------

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

    try:
        #if the product isnt already in the repository, add it to the repository
        if not Repository.checkProductExists(productid):
            Repository.createNewProduct(product_name,productid)
        #timestamp the entry to track price's over time
        timestamp = str(date.today())
        Repository.addprice(productid,product_price,timestamp)
    except:
        print("error during product/price entry")

fetch_ids()
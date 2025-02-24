import requests
from datetime import date
import urllib.parse
import Repository

def fetch_ids(CategoryID,URL,Format,pg,conn):

    # Base URL for the API
    base_url = "https://www.woolworths.com.au/apis/ui/browse/category"
    # Parameters for the API call
    params = {
        "categoryId": CategoryID,
        "url": "/shop/browse/" + URL,
        "formatObject": '{"name":"'+Format+'"}',
        "pageNumber": str(pg),
        "pageSize": 36,
        "sortType": "TraderRelevance",
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
        return False
    response = response.json()
    if addResponseToDatabase(response,conn):
        # if the length of the list of products is less than 36 we are on the last page, (page usually shows 36 products)
        if len(response['Bundles']) >= 36:
            return  fetch_ids(CategoryID,URL,Format,pg + 1,conn)
    else:
        print("error during data entry")


def addResponseToDatabase(response,conn):
    for product in response['Bundles']:
        Name = product["Name"]
        subclass = product["Products"]
        subclass2 = subclass[0]
        ID = subclass2["Stockcode"]
        Price = subclass2["Price"]
        try:
            #if the product isnt already in the repository, add it to the repository
            if not Repository.checkProductExists(ID,conn):
                Repository.createNewProduct(Name,ID,conn)
            #timestamp the entry to track price's over time
            timestamp = str(date.today())
            #only enter the price into the price repository if it exists
            if Price:
                Repository.addprice(ID,Price,timestamp,conn)
        except Exception as e:
            print(str(e))
            return False
    return True

# make function to retrieve all category codes and shit, https://www.woolworths.com.au/apis/ui/PiesCategoriesWithSpecials (GET not POST)
def populate_db():
    URL = 'https://www.woolworths.com.au/apis/ui/PiesCategoriesWithSpecials'
    # Headers for the request
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
    }

    categories = requests.get(URL,headers = headers)
    if categories.status_code != 200:
        print(f"Error: {categories.status_code}")
        return

    categories = categories.json()
    try:
        conn = Repository.createConnection()
        for group in categories['Categories']:
            # ignore specials and front of store to avoid duplicate entries
            if group['NodeId'] == "specialsgroup" or group['NodeId'] == "1_B63CF9E":
                pass
            else:
                #enter each group into the database
                print("adding data from "+group['Description'])
                fetch_ids(group['NodeId'],group['UrlFriendlyName'],group['Description'],1,conn)
    except Exception as e:
        print(str(e))
        Repository.closeConnection(conn)



#----------------------------------------------------------------------------------------------------------------------------------------------------
#EXTREMELY SLOW FOR SOME REASON, high latency for server communication
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

populate_db()
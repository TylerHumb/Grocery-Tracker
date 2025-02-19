import requests
from bs4 import BeautifulSoup
import csv
from datetime import date

def scrape_uci_datasets():
    base_url = "https://archive.ics.uci.edu/datasets"

    headers = ["Product_Name","Product_Price","Date"]
    
    #for storing scraped data
    data = []

def scrape_details(website_url):
    response = requests.get(website_url)
    soup = BeautifulSoup(response.text,'html.parser')
    product_name = soup.find('h1', class_="shelfProductTile-title heading4")
    if product_name:
        product_name = product_name.text.strip()
    else:
        return
    
    #woolworths tracks dolalrs and cents seperately so we get them individually and concat them
    product_price = soup.find('span', class_="price-dollars")
    if product_price:
        product_price = product_price.text.strip()
    else:
        return
    price_cents = soup.find('span', class_="price-cents")
    if price_cents:
        price_cents = price_cents.text.strip()
    else:
        return
    
    product_price = product_price + '.' + price_cents

    #timestamp each record so we can track price changes over time
    timestamp = str(date.today())
    print(timestamp)

    return [product_name,product_price,timestamp]

data = scrape_details("https://www.woolworths.com.au/shop/productdetails/123456")
print(data)
    
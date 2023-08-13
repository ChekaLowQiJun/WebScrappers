import datetime
import logging

import azure.functions as func

from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
import pandas as pd

search_term = 'manga'
amazon_url = "https://www.amazon.sg/s?k={}".format(search_term)

def main(mytimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()
    

    client = uReq(amazon_url)
    page_html = client.read()
    client.close()


    page_soup = soup(page_html)


    span_tags_product_name = page_soup.findAll('span', {'class': 'a-size-base-plus a-color-base a-text-normal'})
    product_names = []
    for product_name in span_tags_product_name:
        product_names.append(product_name.text)

    
    span_tags_prices = page_soup.findAll('span', {'class': "a-price", 'data-a-size': "xl"})
    prices = []
    for price in span_tags_prices:
        prices.append(price.text[:(len(price.text)//2)])

    
    df = pd.DataFrame(product_names, prices)


    name = "{}_prices".format(search_term) + str(utc_timestamp)  +".csv"
    name = "".join( x for x in name if (x.isalnum() or x in "._- "))
    df.to_csv(name)

    
    logging.info('Python timer trigger function ran at %s', utc_timestamp)

#!/usr/bin/python
#==============================================================================
# coding: utf-8
# Program to check whether pricing needs to be adjusted per price-match policy
# Basic Logic: 
# 1.Take product links and store pricing from store page
#2. Dump as JSON
#==============================================================================



# TODO: combine new and current files, preserving ignore status, etc
#       Add date scraped to each product.
#       Add record of store with best price - aggressor store
#       Output reports to a folder with the file labeled as a date.
#       Set first json object as date, as it can be the same for all prices in the file. Parse on input.


##Dependancies:
from __future__ import print_function
from lxml import html
from decimal import Decimal
import requests
import pycurl
from io import BytesIO
import time
import json
from pprint import pprint
import sys
import time
import random

storeID = "8327"
#Load the pages required to parse and read them
pagelist=['http://pricespy.co.nz/shop.php?f='+storeID+'&lista=prod','http://pricespy.co.nz/shop.php?f='+storeID+'&lista=prod&s=100',
        'http://pricespy.co.nz/shop.php?f='+storeID+'&lista=prod&s=200','http://pricespy.co.nz/shop.php?f='+storeID+'&lista=prod&s=300',
        'http://pricespy.co.nz/shop.php?f='+storeID+'&lista=prod&s=400','http://pricespy.co.nz/shop.php?f='+storeID+'&lista=prod&s=500', 
        'http://pricespy.co.nz/shop.php?f='+storeID+'&lista=prod&s=600', 'http://pricespy.co.nz/shop.php?f='+storeID+'&lista=prod&s=700']
#pagelist=['http://pricespy.co.nz/shop.php?f='+storeID+'&lista=prod']

#######################
#    Debug            #
#######################
# Set to 1 to output debug information to terminal
debug = 1
#######################

#Reset useful elements for ease of use
products = []
productPage = []
ourPrice = []
bestPrice = []
ourPriced = []
bestPriced = []
prod_id=[]
results=[]

outFile = 'pricespy.json'

#######################
#    Debug            #
#######################
if debug == 1:
    print("Fetching Pages")
#######################
#Use xPath to find useful elements in pages
pn=len(pagelist)
for p in range(0, pn):

    #######################
    #    Debug            #
    #######################
    if debug == 1:
        print('.', end='')
        sys.stdout.flush()
    #######################
    page = requests.get(pagelist[p])
    tree = html.fromstring(page.content)
    
    products = products + tree.xpath('//td[2]/a/text()')
    productPage = productPage + tree.xpath('//td[2]/a/@href')
    ourPrice = ourPrice + (tree.xpath('//td[4]/a/text()'))
    bestPrice = bestPrice + (tree.xpath('//td[5]/a/text()|//td[5]/span/a/text()'))

num=len(products)  
errorflag=[None] * num
#When alternative prices are avilable, the first thing the script sees instead of the price is '*'   
for q in range(0,num):
    if '*' in bestPrice[q]:
        del bestPrice[q]

#Convert Price to decimal list (Strip non numeric characters)
for d in range(0,num):
    stripa= ourPrice[d].strip('$')
    stripa = stripa.replace(',', '')
    stripb= bestPrice[d].strip('$')
    stripb= stripb.replace(',', '')
    ourPriced.append(Decimal(stripa))
    if stripb != "No prices":
        bestPriced.append(Decimal(stripb))
    else:
        bestPriced.append("0")
    
    pid=productPage[d].strip('/product.php?p=')
    prod_id.append(pid)    

#Compare Our price to other prices add to table of prices to go down
for x in range(0, num):
    # if bestPriced[x] < ourPriced[x]:
    results.append({
        "product":products[x],
        "theirPrice":str(bestPriced[x]),
        "ourPrice":str(ourPriced[x]),
        "link":'http://pricespy.co.nz/product.php?p='+prod_id[x],
        "ignoreStatus":"0", 
        "productID": prod_id[x],
        "dateScraped": time.strftime("%b %d %Y") })

#######################
#    Debug            #
#######################
if debug == 1:
    print("\nStarting Output")
#######################



oldInFile = "prices.json"

outProducts = []
outFile="prices.json"

oldData = json.load(open(oldInFile))

for line in results:
    for oldLine in oldData:
        if line['productID'] == oldLine['productID']:


            if (line['ignoreStatus'] != oldLine['ignoreStatus'] or
                line['theirPrice'] != oldLine['theirPrice'] or
                line['ourPrice'] != oldLine['ourPrice']):
                    outProducts.append({
                    "product":line['product'],
                    "theirPrice":line['theirPrice'],
                    "ourPrice": line['ourPrice'],
                    "link":'http://pricespy.co.nz/product.php?p='+line['productID'],
                    "ignoreStatus": oldLine['ignoreStatus'], 
                    "productID": line['productID'],
                    "dateScraped": line['dateScraped'],
                    "dateIgnored": oldLine['dateIgnored'] })

#               print(line['productID']+" and "+oldLine['productID'])
            else:
                 outProducts.append({
                    "product":line['product'],
                    "theirPrice":line['theirPrice'],
                    "ourPrice": line['ourPrice'],
                    "link":'http://pricespy.co.nz/product.php?p='+line['productID'],
                    "ignoreStatus": line['ignoreStatus'], 
                    "productID": line['productID'], 
                    "dateScraped": line['dateScraped'] })

open(outFile, 'w').write(json.dumps(outProducts))

#open(outFile, 'w').write(json.dumps(results))
#!/usr/bin/python
# ==============================================================================
# coding: utf-8
# Program to check whether pricing against a specific store
# Basic Logic:
# 1. Take product links and store pricing from store page
# 2. Dump as JSON
# ==============================================================================

# TODO: combine new and current files, preserving ignore status, etc
#   Add record of store with best price - aggressor store

# Dependancies:
from __future__ import print_function
from lxml import html
from decimal import Decimal
import requests
import time
import json
import sys

outFile = 'prices.json'
prodURL = 'http://pricespy.co.nz/product.php?p='
# ID of the target store
tgStore = '8327'

# Load the pages required to parse and read them
pagelist = [
    'http://pricespy.co.nz/shop.php?f=' + tgStore + '&lista=prod',
    'http://pricespy.co.nz/shop.php?f=' + tgStore + '&lista=prod&s=100',
    'http://pricespy.co.nz/shop.php?f=' + tgStore + '&lista=prod&s=200',
    'http://pricespy.co.nz/shop.php?f=' + tgStore + '&lista=prod&s=300',
    'http://pricespy.co.nz/shop.php?f=' + tgStore + '&lista=prod&s=400',
    'http://pricespy.co.nz/shop.php?f=' + tgStore + '&lista=prod&s=500',
    'http://pricespy.co.nz/shop.php?f=' + tgStore + '&lista=prod&s=600',
    'http://pricespy.co.nz/shop.php?f=' + tgStore + '&lista=prod&s=700']

#######################
#    Debug            #
#######################
# To output Debugging information, add '--debug-level=' followed by 1, 2, or 3
debug = 0
try:
    if "--" in sys.argv[1]:
        if sys.argv[1] == '--debug-level=1':
            debug = 1
            print("Debug set to level 1 'Basic'")
        if sys.argv[1] == '--debug-level=2':
            debug = 2
            print("Debug set to level 2 'Normal'")
        if sys.argv[1] == '--debug-level=3':
            debug = 3
            print("Debug set to level 3 'Verbose'")
        else:
            print(
                """Unknown option.
                For Debugging, the command is '--debug-level=' followed by 1, 2, or 3""")
except IndexError:
    pass

#######################

# Reset useful elements for ease of use
prod = []
pPage = []
tgPrice = []
bPrice = []
tgPriced = []
bPriced = []
prodID = []
results = []

#######################
#    Debug            #
#######################
if debug >= 1:
    print("Fetching Pages")
#######################
# Use xPath to find useful elements in pages
pn = len(pagelist)
for p in range(0, pn):

    #######################
    #    Debug            #
    #######################
    if debug >= 1:
        print('.', end='')
        sys.stdout.flush()
    #######################
    page = requests.get(pagelist[p])
    tree = html.fromstring(page.content)

    prod = prod + tree.xpath('//td[2]/a/text()')
    pPage = pPage + tree.xpath('//td[2]/a/@href')
    tgPrice = tgPrice + (tree.xpath('//td[4]/a/text()'))
    bPrice = bPrice + (tree.xpath(
        '//td[5]/a/text()|//td[5]/span/a/text()'))

pLen = len(prod)
errorflag = [None] * pLen

# When alternative prices are avilable,
# the first thing the script sees instead of the price is '*'

for q in range(0, pLen):
    if '*' in bPrice[q]:
        del bPrice[q]

# Convert Price to decimal list (Strip non pLeneric characters)
for d in range(0, pLen):
    stripa = tgPrice[d].strip('$')
    stripa = stripa.replace(',', '')
    stripb = bPrice[d].strip('$')
    stripb = stripb.replace(',', '')
    tgPriced.append(Decimal(stripa))
    if stripb != "No prices":
        bPriced.append(Decimal(stripb))
    else:
        bPriced.append("0")

    pid = pPage[d].strip('/product.php?p=')
    prodID.append(pid)

# Compare target price to other prices add to table of prices to go down
for x in range(0, pLen):
    # if bPriced[x] < tgPriced[x]:
    results.append({
        "product": prod[x],
        "theirPrice": str(bPriced[x]),
        "ourPrice": str(tgPriced[x]),
        "link": 'http://pricespy.co.nz/product.php?p=' + prodID[x],
        "ignoreStatus": "0",
        "dateIgnored": "0",
        "productID": prodID[x],
        "dateScraped": time.strftime("%b %d %Y")})

#######################
#    Debug            #
#######################
if debug >= 1:
    print("\nStarting Output")
#######################

outProd = []

oldData = json.load(open(outFile))

for line in results:
    for oldLine in oldData:
        if line['productID'] == oldLine['productID']:
            if (line['ignoreStatus'] != oldLine['ignoreStatus'] or
                line['theirPrice'] != oldLine['theirPrice'] or
                    line['ourPrice'] != oldLine['ourPrice']):
                #######################
                #    Debug            #
                #######################
                if debug >= 3:
                    print(
                        "Appended Product: " + line['product'])
                #######################

                try:
                    outProd.append({
                        "product": line['product'],
                        "theirPrice": line['theirPrice'],
                        "ourPrice": line['ourPrice'],
                        "link": prodURL + line['productID'],
                        "ignoreStatus": oldLine['ignoreStatus'],
                        "productID": line['productID'],
                        "dateScraped": line['dateScraped'],
                        "dateIgnored": oldLine['dateIgnored']})
                except KeyError:
                    outProd.append({
                        "product": line['product'],
                        "theirPrice": line['theirPrice'],
                        "ourPrice": line['ourPrice'],
                        "link": prodURL + line['productID'],
                        "ignoreStatus": oldLine['ignoreStatus'],
                        "productID": line['productID'],
                        "dateScraped": line['dateScraped']})
#               print(line['productID']+" and "+oldLine['productID'])
            else:
                #######################
                #    Debug            #
                #######################
                if debug >= 3:
                    print(
                        "Added Product: " + line['product'])
                #######################
                outProd.append({
                    "product": line['product'],
                    "theirPrice": line['theirPrice'],
                    "ourPrice": line['ourPrice'],
                    "link": prodURL + line['productID'],
                    "ignoreStatus": line['ignoreStatus'],
                    "productID": line['productID'],
                    "dateScraped": line['dateScraped']})

output = open(outFile, 'w').write(json.dumps(outProd))

# open(outFile, 'w').write(json.dumps(results))

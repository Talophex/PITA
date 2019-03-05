# -*- coding: utf-8 -*-
"""
Created on Mon Mar 04 11:10:17 2019

@author: Lucas
"""

import json
import requests


""" Retrieve current price data on all contracts and write it to JSON file. """

URL = "https://www.predictit.org/api/marketdata/all/"
response = requests.get(URL)

jsondata = json.loads(response.text)

for i in xrange(0,len(jsondata['markets'])):
    print jsondata['markets'][i]['name']
    
    



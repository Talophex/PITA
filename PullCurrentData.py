# -*- coding: utf-8 -*-
"""
Created on Mon Mar 04 11:10:17 2019

@author: Lucas
"""

import datetime
import dateutil
import dateutil.parser
import os
import json
import requests
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.exc import MultipleResultsFound


starttime = datetime.datetime.now()

""" Retrieve current price data on all contracts and write it to JSON file. """
URL = "https://www.predictit.org/api/marketdata/all/"
response = requests.get(URL)

jsondata = json.loads(response.text)


""" Add data to SQLite3 tables """
engine = sqlalchemy.create_engine('sqlite:///' + os.getcwd() + '/pita.db')
base = automap_base()
base.prepare(engine, reflect=True)
Markets = base.classes.Markets
Contracts = base.classes.Contracts
Prices = base.classes.Prices
session = Session(engine)


""" Add price data to database. If contract or market is missing, add it. """
currtimestamp = dateutil.parser.parse(jsondata['markets'][0]['timeStamp'])
for a in xrange(0,len(jsondata['markets'])):
    currmark = jsondata['markets'][a]
    try:
        checkmark = session.query(Markets.market_id).filter_by(market_predictit_id=currmark['id']).scalar()
        if checkmark is None:
            session.add(Markets(market_name=currmark['name'], market_url=currmark['url'], market_status=currmark['status'], market_predictit_id=currmark['id']))
    except MultipleResultsFound, e:
            print e
    for b in xrange(0,len(currmark['contracts'])):
        currcon = currmark['contracts'][b]
        try:
            checkcon = session.query(Contracts.contract_id).filter_by(contract_predictit_id=currcon['id']).scalar()
            if checkcon is None:
                session.add(Contracts(market_id=session.query(Markets.market_id).filter_by(market_predictit_id=currmark['id']).scalar(), contract_name=currcon['name'], contract_status=currcon['status'], contract_predictit_id=currcon['id']))
        except MultipleResultsFound, e:
            print e
        newprice = Prices(contract_id=session.query(Contracts.contract_id).filter_by(contract_predictit_id=currcon['id']).scalar(),last_price=currcon['lastTradePrice'],buy_yes=currcon['bestBuyYesCost'],buy_no=currcon['bestBuyNoCost'],sell_yes=currcon['bestSellYesCost'],sell_no=currcon['bestSellNoCost'],time_stamp=currtimestamp)
        session.add(newprice)
session.commit()

print "Total time taken: " + str(datetime.datetime.now()-starttime)

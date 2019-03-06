# -*- coding: utf-8 -*-
"""
Created on Mon Mar 04 11:10:17 2019

@author: Lucas
"""

import datetime
import os
import json
import requests
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.exc import MultipleResultsFound


""" Retrieve current price data on all contracts and write it to JSON file. """
URL = "https://www.predictit.org/api/marketdata/all/"
response = requests.get(URL)

jsondata = json.loads(response.text)


""" Add data to SQLite3 tables """
engine = sqlalchemy.create_engine('sqlite:///' + os.getcwd() + '\\pita.db', echo=True)
base = automap_base()
base.prepare(engine, reflect=True)
Markets = base.classes.Markets
Contracts = base.classes.Contracts
session = Session(engine)


""" Only check/update market and contract names every hour. """
now = datetime.datetime.now()
if now.minute == 0:
    
    """ Check for existence of each market in database and add if not found. """
    for i in xrange(0,len(jsondata['markets'])):
        try:
            checkexist = session.query(Markets.market_id).filter_by(market_name=jsondata['markets'][i]['name']).scalar()
            if checkexist is None:
                session.add(Markets(market_name=jsondata['markets'][i]['name'], market_url=jsondata['markets'][i]['url'], market_status=jsondata['markets'][i]['status'], market_predictit_id=jsondata['markets'][i]['id']))
        except MultipleResultsFound, e:
            print e
    session.commit()
    
    """ Check for existence of each contract in database and add if not found. Contracts are linked to their market. """
    for j in xrange(0,len(jsondata['markets'])):
        for k in xrange(0,len(jsondata['markets'][j]['contracts'])):
            currcon = jsondata['markets'][j]['contracts'][k]
            try:
                checkexist = session.query(Contracts.contract_id).filter_by(contract_name=currcon['name']).scalar()
                if checkexist is None:
                    session.add(Contracts(market_id=session.query(Markets.market_id).filter_by(market_name=jsondata['markets'][j]['name']).scalar(), contract_name=currcon['name'], contract_status=currcon['status'], contract_predictit_id=currcon['id']))
            except MultipleResultsFound, e:
                print e
    session.commit()
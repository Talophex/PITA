# -*- coding: utf-8 -*-
"""
Created on Mon Mar 04 11:10:17 2019

@author: Lucas
"""

import json
import requests
import sqlalchemy
from sqlalchemy import Table, Column, Integer, String, DECIMAL
from sqlalchemy import MetaData, create_engine, ForeignKey
from sqlalchemy.orm import relation, backref, sessionmaker, scoped_session


""" Retrieve current price data on all contracts and write it to JSON file. """

URL = "https://www.predictit.org/api/marketdata/all/"
response = requests.get(URL)

jsondata = json.loads(response.text)

for i in xrange(0,len(jsondata['markets'])):
    print jsondata['markets'][i]['name']
    
    
""" Build database with SQLAlchemy """

engine = sqlalchemy.create_engine('sqlite:////pita.sqlite', echo=True)
base = sqlalchemy.ext.declarative.declarative_base(bind=engine)

# Define tables:
class Markets(base):
    __tablename__ = 'Markets'
    market_id = Column(Integer, primary_key=True)
    market_name = Column(String)
    market_url = Column(String)
    market_status = Column(String)
    market_predictit_id = Column(Integer)
    
class Contracts(base):
    __tablename__ = 'Contracts'
    contract_id = Column(Integer, primary_key=True)
    market_id = Column(Integer, ForeignKey('Markets.market_id'))
    contract_name = Column(String)
    contract_status = Column(String)
    contract_predictit_id = Column(Integer)
    
class Prices(base):
    __tablename__ = 'Prices'
    price_id = Column(Integer, primary_key=True)
    contract_id = Column(Integer, ForeignKey('Contracts.contract_id'))
    last_price = Column(DECIMAL(1,2))
    buy_yes = Column(DECIMAL(1,2))
    buy_no = Column(DECIMAL(1,2))
    sell_yes = Column(DECIMAL(1,2))
    sell_no = Column(DECIMAL(1,2))
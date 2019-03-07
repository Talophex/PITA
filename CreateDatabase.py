# -*- coding: utf-8 -*-
"""
Created on Tue Mar 05 17:06:40 2019

@author: Lucas
"""

import os
import sqlalchemy
import sqlalchemy.ext.declarative
from sqlalchemy import Table, Column, Integer, String, DECIMAL
from sqlalchemy import MetaData, create_engine, ForeignKey
from sqlalchemy.orm import relation, backref, sessionmaker, scoped_session

""" Build database with SQLAlchemy """

engine = sqlalchemy.create_engine('sqlite:///' + os.getcwd() + '/pita.db', echo=True)
base = sqlalchemy.ext.declarative.declarative_base(bind=engine)

# Define tables:
class Markets(base):
    __tablename__ = 'Markets'
    market_id = Column(Integer, primary_key=True)
    market_name = Column(String)
    market_url = Column(String)
    market_status = Column(String)
    market_predictit_id = Column(Integer)
    
    def __init__(self, market_name, market_url, market_status, market_predictit_id):
        self.market_name = market_name
        self.market_url = market_url
        self.market_status = market_status
        self.market_predictit_id = market_predictit_id

    def __repr__(self):
        return "<Asset('%s', '%s')>" % (self.market_name, self.market_url, self.market_status, self.market_predictit_id)
    
class Contracts(base):
    __tablename__ = 'Contracts'
    contract_id = Column(Integer, primary_key=True)
    market_id = Column(Integer, ForeignKey('Markets.market_id'))
    contract_name = Column(String)
    contract_status = Column(String)
    contract_predictit_id = Column(Integer)
    
    def __init__(self, contract_name, contract_status, contract_predictit_id):
        self.contract_name = contract_name
        self.contract_status = contract_status
        self.contract_predictit_id = contract_predictit_id

    def __repr__(self):
        return "<Asset('%s', '%s')>" % (self.contract_name, self.contract_status, self.contract_predictit_id)
    
class Prices(base):
    __tablename__ = 'Prices'
    price_id = Column(Integer, primary_key=True)
    contract_id = Column(Integer, ForeignKey('Contracts.contract_id'), nullable=False)
    last_price = Column(DECIMAL(1,2))
    buy_yes = Column(DECIMAL(1,2))
    buy_no = Column(DECIMAL(1,2))
    sell_yes = Column(DECIMAL(1,2))
    sell_no = Column(DECIMAL(1,2))
    time_stamp = Column(sqlalchemy.types.TIMESTAMP)
    
    def __init__(self, last_price, buy_yes, buy_no, sell_yes, sell_no):
        self.last_price = last_price
        self.buy_yes = buy_yes
        self.buy_no = buy_no
        self.sell_yes = sell_yes
        self.sell_no = sell_no
        self.time_stamp = time_stamp

    def __repr__(self):
        return "<Asset('%s', '%s')>" % (self.last_price, self.buy_yes, self.buy_no, self.sell_yes, self.sell_no, self.time_stamp)
    
base.metadata.create_all(engine)
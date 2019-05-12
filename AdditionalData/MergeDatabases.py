# -*- coding: utf-8 -*-
"""
Created on Sat May 11 10:11:37 2019

@author: Lucas
"""

import os
import sqlalchemy
import sqlalchemy.ext.declarative

from pathlib import Path
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import UniqueConstraint
from sqlalchemy import Table, Column, Integer, String, DECIMAL
from sqlalchemy import MetaData, create_engine, ForeignKey
from sqlalchemy.orm import relation, backref, sessionmaker, scoped_session


mainpitapath = Path(__file__).parents[1] / 'pita.db'
mainengine = sqlalchemy.create_engine('sqlite:///' + str(mainpitapath), echo=False)
mainbase = automap_base()
mainbase.prepare(mainengine, reflect=True)
mainMarkets = mainbase.classes.Markets
mainContracts = mainbase.classes.Contracts
mainPrices = mainbase.classes.Prices
mainsession = Session(mainengine)


for child in Path.cwd().iterdir():
    if child.match('*.db'):
        print child
        childengine = sqlalchemy.create_engine('sqlite:///' + str(child), echo=False)
        childbase = automap_base()
        childbase.prepare(childengine, reflect=True)
        childMarkets = childbase.classes.Markets
        childContracts = childbase.classes.Contracts
        childPrices = childbase.classes.Prices
        childsession = Session(childengine)
        
        pricesquery = childsession.query(childPrices).all()
        for price in pricesquery:
            
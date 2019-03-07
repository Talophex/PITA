# -*- coding: utf-8 -*-
"""
Created on Wed Mar 06 22:33:54 2019

@author: Lucas
"""

import os
import sys
import csv
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.exc import MultipleResultsFound


""" Retrieve and map sqlite3 database """
engine = sqlalchemy.create_engine('sqlite:///' + os.getcwd() + '/pita.db', echo=False)
base = automap_base()
base.prepare(engine, reflect=True)
Markets = base.classes.Markets
Contracts = base.classes.Contracts
Prices = base.classes.Prices
session = Session(engine)

""" Process argument """
args = sys.argv
if len(args) < 2:
    print
    print "Please supply requested market ID as argument."
    print "Example: python DumpCSV.py 3352"
else:
    mark_id = session.query(Markets.market_id).filter_by(market_predictit_id=int(args[1])).scalar()
    if mark_id is None:
        print
        print "Market: "+str(args[1])+" not found."
    else:
        for mark_name, in session.query(Markets.market_name).filter_by(market_predictit_id==mark_id)
        print "Market: "+str(mark_name)+" found and dumped."
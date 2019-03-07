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
    print "Please supply a market ID as an argument."
    print "Example: python DumpCSV.py 3352"
else:
    m_id = session.query(Markets.market_id).filter_by(market_predictit_id=int(args[1])).scalar()
    if m_id is None:
        print
        print "Market: "+str(args[1])+" not found."
    else:
        m_name = session.query(Markets.market_name).filter_by(market_id=m_id).scalar()
        c_ids = session.query(Contracts.contract_id).filter_by(market_id=m_id).all()
        for a in c_ids:
            fileout = open(str(args[1])+'-'+str(a[0])+'.csv', 'wb')
            outcsv = csv.writer(fileout)
            records = session.query(Prices).filter_by(contract_id=a[0]).all()
            outcsv.writerow([column.name for column in Prices.__mapper__.columns])
            [outcsv.writerow([getattr(curr, column.name) for column in Prices.__mapper__.columns]) for curr in records]
            fileout.close()
        print 'Market: '+m_name+' found and dumped to '+str(len(c_ids))+' csv files.'
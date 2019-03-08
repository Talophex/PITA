import datetime
import os
import json
from StringIO import StringIO

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

import requests
from dateutil.parser import parse as datetime_parse

import pandas as pd


def scrape_market(market_id):

    r = requests.get(
        'https://www.predictit.org/Resource/DownloadMarketChartData',
        params={'marketid': market_id, 'timespan': '24h'})

    strio = StringIO()
    strio.write(r.content)
    strio.seek(0)

    df = pd.read_csv(strio)

    # print(df.head())
    n_contracts = len(df['ContractId'].unique())

    latest_values = df.sort_values('DateString',
                                   ascending=False)[0:n_contracts]

    return latest_values


starttime = datetime.datetime.now()

# URL = 'https://www.predictit.org/Resource/DownloadMarketChartData\?marketid\=3633\&timespan\=7d'

URL = "https://www.predictit.org/api/marketdata/all/"
response = requests.get(URL)
all_market_data = json.loads(response.text)['markets']


engine = sqlalchemy.create_engine('sqlite:///' + os.getcwd() + '/pita.db',
                                  echo=True)
base = automap_base()
base.prepare(engine, reflect=True)
Contracts = base.classes.Contracts
Volumes = base.classes.Volumes
session = Session(engine)


for market_id in (k['id'] for k in all_market_data):

    latest_values = scrape_market(market_id)

    for i, vals in latest_values.iterrows():

        newprice = Volumes(
            contract_id=session.query(Contracts.contract_id)\
                .filter_by(contract_predictit_id=vals['ContractId'])\
                .scalar(),
            open_share_price=vals['OpenSharePrice'],
            high_share_price=vals['HighSharePrice'],
            low_share_price=vals['LowSharePrice'],
            close_share_price=vals['CloseSharePrice'],
            volume=vals['TradeVolume'],
            time_stamp=datetime_parse(vals['DateString']))

        try:
            session.add(newprice)
            session.commit()
        except sqlalchemy.exc.IntegrityError:
            print(vals)
            raise

    break

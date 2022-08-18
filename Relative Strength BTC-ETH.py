# -*- coding: utf-8 -*-
"""
Created on Thu Aug 18 16:58:59 2022

@author: Rodrigo
"""

import requests
import pandas as pd

request_url_btc = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart?vs_currency=usd&days=90"
request_url_eth = "https://api.coingecko.com/api/v3/coins/ethereum/market_chart?vs_currency=usd&days=90"

def normal_series(request_url):
    r = requests.get(request_url)
    status_code = r.status_code
    if (status_code == 200):
        response_data = r.json()
        response_data = pd.json_normalize(data=response_data, record_path="prices")
        response_data[0] = pd.to_datetime(response_data[0], unit="ms",origin="unix")
        response_data.rename(columns = {0:'date', 1:'close'}, inplace=True)
    else:
        print("error")
    return response_data

def graph (dt):
    dt = dt.set_index(dt['date'])
    dt = dt.drop(['date'], axis=1)
    dt.plot(title="Relative Strenght Dorsey")


btc = pd.DataFrame(normal_series(request_url_btc))
eth = pd.DataFrame(normal_series(request_url_eth))

relative = pd.DataFrame()
relative["result"] = btc["close"] / eth["close"]
relative["date"] = btc["date"]
relative = relative[["date", "result"]]
graph(relative)

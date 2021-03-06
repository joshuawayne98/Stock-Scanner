import bs4 as bs
import pickle
import requests
import os
import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
import pandas_datareader as web

def save_snp500_tickers():
    resp = requests.get('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    soup = bs.BeautifulSoup(resp.text, 'lxml')
    table = soup.find('table', {'id': 'constituents'})
    tickers=[]
    for row in table.findAll('tr')[1:]:
        ticker = row.find_all('td') [0].text.replace('\n','')
        mapping = str.maketrans(".","-")
        ticker = ticker.translate(mapping)
        tickers.append(ticker)

    with open("snp500tickers.pickle", "wb") as f:
        pickle.dump(tickers, f)
    print(tickers)
    return tickers
save_snp500_tickers()

def get_stock_data(reload_snp500=False):
    if reload_snp500:
        tickers=save_snp500_tickers()
    else:
        with open("snp500tickers.pickle","rb") as f:
            tickers = pickle.load(f) 
    if not os.path.exists('stock_dfs'):
        os.makedirs('stock_dfs')
    start = dt.datetime(2000,1,1)
    end = dt.datetime(2020,8,10)

    for ticker in tickers:
        print (ticker)
        if not os.path.exists('stock_dfs/{}.csv'.format(ticker)):
            df = web.DataReader(ticker, 'yahoo', start, end)
            df.to_csv('stock_dfs/{}.csv'.format(ticker))
        else:
            print('Already have {}'.format(ticker))
get_stock_data()

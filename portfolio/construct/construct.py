import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
import tqdm as tqdm
from tqdm import tqdm
tqdm.pandas()
import datetime
import locale
from os.path import exists

class Portfolio:


    def __init__(self,portfolio,cols):
        self.import_portfolio(portfolio,cols)
        self.get_ts()
        
    def get_portfolio_ts(self,weights):
        portfolio_ts = pd.DataFrame(index=self.all_ts.index,columns=['Portfolio']).fillna(0)
        self.pf_copy = self.pf.copy(deep=True)
        self.pf_copy.set_index('Ticker',inplace=True)

        for i in portfolio_ts.index:
            y = 0
            for j in self.all_ts.columns:
                y = y + self.all_ts.loc[i,j]*self.pf_copy.loc[j,weights]

            portfolio_ts.loc[i,'Portfolio'] = y
            
        self.portfolio_ts = portfolio_ts.copy(deep=True)
        return portfolio_ts

    def import_portfolio(self,portfolio,cols):
        import pandas as pd
        self.pf = pd.read_csv(portfolio)
        self.pf = self.pf[cols]
        
    def get_ts(self):
        pf = self.pf.copy(deep=True)
    
        df_all = pd.DataFrame()
        for tick in list(self.pf['Ticker']):
            df_all[tick] = self.__get_timeseries(tick)
            
        self.all_ts = df_all.copy(deep=True)
        
    def get_weights(self,portfolio):
        pf_wgt = pd.read_csv(portfolio)
        pf_wgt = pd.read_csv('myportfolio.csv')
        pf_wgt['Price'] = pf_wgt['Ticker'].apply(lambda x: yf.Ticker(x).fast_info['previousClose'])
        pf_wgt['Total Value']  = pf_wgt['Quantity']*pf_wgt['Price']
        self.pf_wgt  = pf_wgt[['Name','Total Value']]
        self.pf_wgt.set_index('Name',inplace=True)
        
    def __get_timeseries(self,ticker):
        today = datetime.datetime.today().date().strftime('%Y-%m-%d')
        start_date = str(datetime.datetime.today().year-1)+'-'+today[5:]
        data = yf.download(ticker, start=start_date, end=today)
        return data['Close']
    

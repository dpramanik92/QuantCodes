from construct import construct
from VaRmodels import bootstrap

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
import tqdm as tqdm
from tqdm import tqdm
tqdm.pandas()
import datetime

def get_benchseries(ticker):
        today = datetime.datetime.today().date().strftime('%Y-%m-%d')
        start_date = str(datetime.datetime.today().year-1)+'-'+today[5:]
        print(start_date)
        data = yf.download(ticker, start=start_date, end=today)
        return data['Close']

class portAnalytics:
    def __init__(self,portfolio,rate):
        self.port = portfolio
        self.portfolio_ts = self.port.portfolio_ts
        self.rate=rate
        bm = get_benchseries('^nsei')
        self.bm = pd.DataFrame(bm)
        self.bm['Return'] = self.bm['Close'].pct_change()
        self.portfolio_ts['Compare'] = self.bm['Close']*self.portfolio_ts['Portfolio'][0]/self.bm['Close'][0]
        
    def get_returns(self):
        self.portfolio_ts['Return'] = self.portfolio_ts['Portfolio'].pct_change()
        
    def calc_portfolio_VaR(self,level,time,model=None):
        self.get_returns()
        if model == None:
            VaR = self.portfolio_ts['Return'].quantile(level)*self.portfolio_ts['Portfolio'][-1]
            return VaR*np.sqrt(time)
        else:
            return model.calc_var(self.portfolio_ts,level)*np.sqrt(time)
        
    def calc_sharpe_ratio(self,time):
        ts = self.portfolio_ts.copy(deep=True)
        daily_mean = ts['Return'].mean()
        annual_mean = ((1+daily_mean)**(261.0*time))-1.0
        daily_vol = ts['Return'].std()
        annual_vol = daily_vol*np.sqrt(261*time)
        rate = (1+self.rate)**(time)-1.0
        sharpe_ratio = (annual_mean-rate)/annual_vol
        
        return sharpe_ratio
    
    def calc_tracking_error(self,time):
        ts = self.portfolio_ts.copy(deep=True)
        ts['Diff'] = ts['Return'] - self.bm['Return']
        daily_te = ts['Diff'].std()
        return daily_te*np.sqrt(261*time)
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
import os
from construct.construct import Portfolio
from VaRmodels.bootstrap import BootStrap
from analytics import portAnalytics

class getSummary:
    def __init__(self,**kwargs):
        self.rate = kwargs.get('rate')
        self.infile = kwargs.get('portfolio')
        benchmark = kwargs.get('benchmark')
        
        self.port = Portfolio(portfolio=self.infile,cols=['Ticker','Quantity'])

        self.ts = self.port.get_portfolio_ts('Quantity')
        self.ts['Return'] = self.ts['Portfolio'].pct_change()
        self.model = kwargs.get('model')
        self.analys = portAnalytics(self.port,self.rate,benchmark)
        self.ts = self.analys.portfolio_ts

    
    def risk_metrics(self,level,days,time,outfile):
        print("===========================================================================")
        self.var = self.analys.calc_portfolio_VaR(level,days,model=self.model)
        print('The Var is :',self.var)
        self.sharpe = self.analys.calc_sharpe_ratio(time)
        print('The Sharpe Ratio is: ',self.sharpe)
        self.te = self.analys.calc_tracking_error(time)
        print('The Tracking error is: ',self.te)
        self.annual_return = (self.ts['Portfolio'][-1]-self.ts['Portfolio'][0])/self.ts['Portfolio'][0]*100
        self.bench_return = (self.ts['Compare'][-1]-self.ts['Compare'][0])/self.ts['Compare'][0]*100

        print('The annualized return is : {} %'.format(self.annual_return))
        print('The benchmark return is : {} %'.format(self.bench_return))

        self.ret = self.model.bootstrap_series(self.ts)
        today = datetime.datetime.today().date().strftime('%d-%m-%Y')
        print("===========================================================================")
        
        summary_file = outfile

        if os.path.exists(summary_file) == True:
            df_summary = pd.read_csv(summary_file)
        else:
            df_summary = pd.DataFrame(columns=['Date','Portfolio Value','Tracking Error','Sharpe Ratio','1D VaR','Last Return','Daily Returns (%)'])
        
        data_dict = {'Date':today,'Portfolio Value':self.ts['Portfolio'][-1],'Tracking Error':self.te,'Sharpe Ratio':self.sharpe,'1D VaR':self.var,'Last Return':(self.ts['Portfolio'][-1]-self.ts['Portfolio'][-2]),'Daily Returns (%)':"{:2.1f} %".format((self.ts['Portfolio'][-1]-self.ts['Portfolio'][-2])/self.ts['Portfolio'][-2]*100)}
        df_summary = df_summary.append(data_dict,ignore_index=True)
        df_summary = df_summary.drop_duplicates(subset=['Date'],keep='last')
        df_summary.to_csv(summary_file,index=False)
        
    def get_portfolio_alpha_beta(self):
        import statsmodels.api as sm        

        X = self.ts['Compare'].pct_change()[1:]
        Y = self.ts['Portfolio'].pct_change()[1:]

        X = sm.add_constant(X)
        model = sm.OLS(Y, X).fit()
        model_summary = model.summary()
        self.beta = model.params[1]
        self.alpha = self.annual_return-self.beta*self.bench_return






        
    def get_composition(self):
        pf_wgt = pd.read_csv(self.infile)
        pf_wgt['Price'] = pf_wgt['Ticker'].apply(lambda x: yf.Ticker(x).fast_info['previousClose'])
        pf_wgt['Total Value']  = pf_wgt['Quantity']*pf_wgt['Price']
        pf_wgt.set_index('Name',inplace=True)
        self.pf_wgt = pf_wgt.copy(deep=True)
    
    def get_gains(self):
        all_ts = self.port.all_ts
        close = all_ts.iloc[-1]
        opened = all_ts.iloc[-2]

        df = pd.DataFrame()
        df['Close'] = close
        df['Open'] = opened
        df['Quantity'] = self.port.pf.set_index('Ticker',drop=True)
        pf_wgt = pd.read_csv(self.infile)
        pf_wgt.set_index('Ticker',inplace=True)

        df['Gain'] = (df['Close']-df['Open'])*df['Quantity']
        df['Total Value'] = df['Close']*df['Quantity']

        df['Daily Change'] =(df['Close']-df['Open']) /df['Open']*100
        df.index = pf_wgt['Name']

        Gainers = df[df['Gain']>0].sort_values('Gain',ascending=False)
        Losers = df[df['Gain']<=0].sort_values('Gain')

        self.Top_Gainers = Gainers.head(5)[['Total Value','Gain','Daily Change']]
        self.Top_Losers = Losers.head(5) [['Total Value','Gain','Daily Change']]






    def get_summary(self,level,days,time,outfile):
        self.risk_metrics(level,days,time,outfile)
        self.get_gains()
        self.get_composition()
        self.get_portfolio_alpha_beta()
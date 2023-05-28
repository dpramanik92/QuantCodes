import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
import tqdm as tqdm
from tqdm import tqdm
tqdm.pandas()
import datetime

class BootStrap:


    def __init__(self):
        self.steps = 3
        self.num_sim = 10000
        
    def __single_return(self,ts):
        N = len(ts)
        ts1 = ts.reset_index()
        total = 1.0
        for i in range(self.steps):
            x = np.random.randint(N)
            y = ts1.loc[x,'Return']
            total = total*(1.0+y)
        total = total -1
        return total/np.sqrt(self.steps)
    
    
    def bootstrap_series(self,ts):
        bts = pd.DataFrame(index=[j for j in range(self.num_sim)],columns=['Return']).fillna(0)
        for i in range(self.num_sim):
            bts.loc[i,'Return'] = self.__single_return(ts)
    
        self.bts = bts.copy(deep=True)
        return bts
        
    def calc_var(self,ts,level):
        self.bootstrap_series(ts)
        return self.bts['Return'].quantile(level)*ts['Portfolio'][-1]
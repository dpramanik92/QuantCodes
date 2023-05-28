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
from summary import getSummary

def format_rupees(x, _):
    try:
        return  '{} Lacs'.format(locale.currency(x/100000, grouping=True))
    except IndexError:
        pass
    

class plotReport:
    def __init__(self,out_file):
        self.out_file = out_file


    def plot_page(self,summary):
        locale.setlocale(locale.LC_MONETARY, 'en_IN')
        import matplotlib.dates as mdates
        import matplotlib.ticker as ticker

        fig,ax = plt.subplots(2,2,figsize=(24,16))
        plt.suptitle("Portfolio Summary: {}".format(datetime.datetime.today().date().strftime('%b %d,%Y')),fontsize=45,weight='bold')
        plt.yticks(fontsize=20)
        plt.xticks(fontsize=20)
        color = ['#000548','#4B5EB6','#6867AF','#7FBABE','#3CDEA8','#56D385','#CBBC7B']

        plt.text(-1.5,1.0,'Key Summary:',transform=ax[0,1].transAxes,fontsize=25,weight='bold')
        plt.text(-2.0,0.7,'Present Value:',fontsize=30,color='k',transform=ax[0,1].transAxes, weight='bold')
        plt.text(-1.35,0.7,locale.currency(summary.ts['Portfolio'][-1], grouping=True),fontsize=30,color='#292685',transform=ax[0,1].transAxes, weight='bold')
        plt.text(0.1,1.0,'Portfolio Composition:',fontsize=25,color='k',transform=ax[0,1].transAxes, weight='bold')

        plt.text(-1.9,0.5,'1D VaR [99%]:',fontsize=25,color='#585958',transform=ax[0,1].transAxes, weight='bold')
        plt.text(-1.33,0.5,"({})".format(locale.currency(-1*summary.var, grouping=True)),fontsize=25,color='red',transform=ax[0,1].transAxes)
        plt.text(-1.9,0.6,'Annual Return:',fontsize=25,color='#585958',transform=ax[0,1].transAxes,weight='bold')
    
        if summary.annual_return>0:
            annual = "{:0.1f} %".format(summary.annual_return)
            ret_color = 'green'
        else:
            annual = '({:0.1f} %)'.format(-1*summary.annual_return)
            ret_color = 'red'
        plt.text(-1.3,0.6,annual,fontsize=25,color=ret_color,transform=ax[0,1].transAxes)
        # plt.text(-1.17,0.6,'Portfolio Beta:',fontsize=25,color='#585958',transform=ax[0,1].transAxes, weight='bold')
        # plt.text(-0.83,0.7,locale.currency(-1*var, grouping=True),fontsize=25,color='red',transform=ax[0,1].transAxes)

        plt.text(-2.0,0.4,"Characteristics [1Y]:",fontsize=24,color='k',transform=ax[0,1].transAxes,weight='bold')

        plt.text(-1.9,0.3,"Sharpe Ratio  :",fontsize=24,color='#585958',transform=ax[0,1].transAxes,weight='bold')
        plt.text(-1.35,0.3,"{:1.2f}".format(summary.sharpe),fontsize=24,color= color[0],transform=ax[0,1].transAxes,weight='bold')

        plt.text(-1.9,0.2,"Tracking Error:",fontsize=24,color='#585958',transform=ax[0,1].transAxes,weight='bold')
        plt.text(-1.35,0.2,"{:0.2f}".format(summary.te),fontsize=24,color=color[0],transform=ax[0,1].transAxes,weight='bold')

        plt.text(0.35,0.457,'{:0.2f} L'.format(summary.ts['Portfolio'][-1]/1e5),fontsize=42,color='#04297D',transform=ax[0,1].transAxes, weight='bold')


        ax[0,0].remove()
        l1 = ax[1,1].plot(summary.ts['Portfolio'],lw=2,color='#007AB4')
        l2 = ax[1,1].plot(summary.ts['Compare'],lw=2,color='#e8e8e8')
        ax[1,1].legend([l1[0],l2[0]],['Portfolio','Nifty 50'],fontsize=18,frameon=False)

        plt.text(-1.2,1.05,'Return Distribution [1D] (Simulated)',fontsize=30,weight='bold',transform=ax[1,1].transAxes)
        plt.text(0.,1.05,'Nifty50 1Y Comparison',fontsize=30,weight='bold',transform=ax[1,1].transAxes)
        ax[0,1].pie(summary.pf_wgt['Total Value'],labels=summary.pf_wgt.index,textprops={'fontsize': 20},wedgeprops=dict(width=0.35),colors=color)
        ax[1,0].hist(summary.ret,bins=50,color='#3d8545')
        ax[0,1].spines['top'].set_color('none')
        ax[0,1].spines['right'].set_color('none')
        ax[0,1].spines['left'].set_color('none')
        ax[0,1].spines['bottom'].set_color('none')
        ax[0,1].set_xticks([])
        ax[0,1].set_yticks([])
        ax[1,1].spines['top'].set_color('none')
        ax[1,1].spines['right'].set_color('none')
        ax[1,0].spines['top'].set_color('none')
        ax[1,0].spines['right'].set_color('none')
        ax[1,0].tick_params(axis='x', labelsize=20)
        ax[1,1].xaxis.set_major_formatter(mdates.DateFormatter('%b\' %y'))
        ax[1,1].yaxis.set_major_formatter(format_rupees)
        # ax[1,0].spines['left'].set_color('none')
        ax[1,0].set_yticks([])
        plt.savefig(self.out_file)
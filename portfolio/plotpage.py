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
    def __init__(self,out_file,summary):
        self.out_file = out_file
        self.summary = summary


    def plot_page(self):
        summary = self.summary
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
        plt.text(-1.0,0.6,'Index Return:',fontsize=25,color='#585958',transform=ax[0,1].transAxes,weight='bold')

        if summary.annual_return>0:
            annual = "{:0.1f} %".format(summary.annual_return)
            ret_color = 'green'
        else:
            annual = '({:0.1f} %)'.format(-1*summary.annual_return)
            ret_color = 'red'

        if summary.bench_return>0:
            bench = "{:0.1f} %".format(summary.bench_return)
            ret_color = 'green'
        else:
            bench = '({:0.1f} %)'.format(-1*summary.bench_return)
            ret_color = 'red'
        plt.text(-1.3,0.6,annual,fontsize=25,color=ret_color,transform=ax[0,1].transAxes)
        plt.text(-0.5,0.6,bench,fontsize=25,color=ret_color,transform=ax[0,1].transAxes)

        # plt.text(-1.1,0.,'Portfolio Beta:',fontsize=25,color='#585958',transform=ax[0,1].transAxes, weight='bold')
        # plt.text(-0.83,0.7,locale.currency(-1*var, grouping=True),fontsize=25,color='red',transform=ax[0,1].transAxes)

        plt.text(-2.0,0.4,"Characteristics [1Y]:",fontsize=24,color='k',transform=ax[0,1].transAxes,weight='bold')

        plt.text(-1.9,0.3,"Sharpe Ratio  :",fontsize=24,color='#585958',transform=ax[0,1].transAxes,weight='bold')
        plt.text(-1.35,0.3,"{:1.2f}".format(summary.sharpe),fontsize=24,color= color[0],transform=ax[0,1].transAxes,weight='bold')

        plt.text(-1.9,0.2,"Tracking Error:",fontsize=24,color='#585958',transform=ax[0,1].transAxes,weight='bold')
        plt.text(-1.35,0.2,"{:0.2f}".format(summary.te),fontsize=24,color=color[0],transform=ax[0,1].transAxes,weight='bold')

        plt.text(-1.9,0.1,"Beta:",fontsize=24,color='#585958',transform=ax[0,1].transAxes,weight='bold')
        plt.text(-1.7,0.1,"{:0.2f},".format(summary.beta),fontsize=24,color=color[0],transform=ax[0,1].transAxes,weight='bold')

        plt.text(-1.5,0.1,"Alpha:",fontsize=24,color='#585958',transform=ax[0,1].transAxes,weight='bold')
        plt.text(-1.3,0.1,"{:0.2f}%".format(summary.alpha),fontsize=24,color=color[0],transform=ax[0,1].transAxes,weight='bold')


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
        output = self.out_file + "_summary.pdf"
        plt.savefig(output)

    def plot_gains(self):
        summary = self.summary
        locale.setlocale(locale.LC_MONETARY, 'en_IN')
        import matplotlib.dates as mdates
        import matplotlib.ticker as ticker

        fig,ax = plt.subplots(figsize=(24,16))
        plt.suptitle("Component Returns: {}".format(datetime.datetime.today().date().strftime('%b %d,%Y')),fontsize=45,weight='bold')
        plt.text(0.051,0.95,"Top Gainers:",fontsize=30,weight="bold")
        plt.text(0.051,0.5,"Top Losers:",fontsize=30,weight="bold")
        plt.text(0.051,0.9,"Company    |      Value     |   1D Chanage |    Return (%) [1D]",fontsize=24,weight="bold",color='#007AB4')
        plt.text(0.051,0.45,"Company    |      Value     |   1D Chanage |    Return (%) [1D]",fontsize=24,weight="bold",color='#007AB4')
    
        if len(summary.Top_Gainers)>0:
            for i,ind in enumerate(summary.Top_Gainers.index):
                plt.text(0.02,0.85-0.05*i,"{}:".format(ind),fontsize=24)
                plt.text(0.19,0.85-0.05*i,locale.currency(summary.Top_Gainers.loc[ind,'Total Value'],grouping=True),fontsize=24)
                plt.text(0.33,0.85-0.05*i,locale.currency(summary.Top_Gainers.loc[ind,'Gain'],grouping=True),fontsize=24,color='green')
                plt.text(0.48,0.85-0.05*i,"{:.2f}%".format(summary.Top_Gainers.loc[ind,'Daily Change']),fontsize=24,color='green')

        if len(summary.Top_Losers)>0:
            for i,ind in enumerate(summary.Top_Losers.index):
                plt.text(0.02,0.4-0.05*i,"{}:".format(ind),fontsize=24)
                plt.text(0.19,0.4-0.05*i,locale.currency(summary.Top_Losers.loc[ind,'Total Value'],grouping=True),fontsize=24)
                plt.text(0.33,0.4-0.05*i,"({})".format(locale.currency(-1*summary.Top_Losers.loc[ind,'Gain']),grouping=True),fontsize=24,color='red')
                plt.text(0.48,0.4-0.05*i,"({:.2f})%".format(-1*summary.Top_Losers.loc[ind,'Daily Change']),fontsize=24,color='red')
            

        ax.spines['top'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['right'].set_visible(False)
        
        ax.spines['bottom'].set_visible(False)
    
        output = self.out_file + "_gains.pdf"
        plt.savefig(output)
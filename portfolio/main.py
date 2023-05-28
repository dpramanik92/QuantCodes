from VaRmodels.bootstrap import BootStrap
from plotpage import plotReport
from summary import getSummary
import matplotlib
matplotlib.use('agg')

bts = BootStrap()
summary = getSummary(rate=0.07,portfolio=r'C:\Users\MSUSERSL123\Documents\financials\myportfolio.csv',model=bts)
summary.get_summary(0.01,1,1)
report = plotReport(r'C:\Users\MSUSERSL123\Documents\financials\Daily_portfolio_report.pdf')
report.plot_page(summary)
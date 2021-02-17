#!/usr/bin/env python
# coding: utf-8

# In[129]:


import pandas as pd
import numpy as np
#import ankitfinance as af
#from scipy.stats import norm
#import scipy.stats
#from scipy.optimize import minimize
#from sklearn.svm import SVC
#from sklearn.metrics import accuracy_score
#import matplotlib.pyplot as plt
#import statsmodels.api as sm
get_ipython().run_line_magic('load_ext', 'autoreload')
get_ipython().run_line_magic('autoreload', '2')
get_ipython().run_line_magic('matplotlib', 'inline')
#import sklearn
import yfinance as yf
import yahoo_fin.stock_info as si


# In[186]:


ratio_valuation_function=['Trailing P/E','Forward P/E 1','Price/Book (mrq)','Price/Sales (ttm)','PEG Ratio (5 yr expected) 1']


# In[187]:


ratio_stat=['Beta (5Y Monthly)','% Held by Insiders 1','% Held by Institutions 1','Trailing Annual Dividend Yield 3','Forward Annual Dividend Yield 4','Return on Equity (ttm)','Return on Assets (ttm)','Diluted EPS (ttm)','Quarterly Earnings Growth (yoy)','Total Debt/Equity (mrq)']


# In[237]:


tickers=['AMZN','GOOG','PG','KO','IBM']
table=pd.DataFrame()
table2=pd.DataFrame()
for steps in range(len(tickers)):
    p=str(tickers[steps])
    data=si.get_stats(p)
    data.index=data["Attribute"]
    data=data.drop(labels="Attribute",axis=1)
    raw_table=data.T
    raw_table=raw_table[ratio_stat]
    table=table.append(raw_table)   #Table having Data about the company
    
table.index=tickers

table2=pd.DataFrame()
for steps in range(len(tickers)):
    p=str(tickers[steps])
    extra_ratio=si.get_stats_valuation(p)
    extra_ratio.index=extra_ratio[0]
    extra_ratio=extra_ratio.drop(labels=0,axis=1)
    new_table=extra_ratio.T
    new_table=new_table[ratio_valuation_function]
    table2=table2.append(new_table)  #Table having Data about the company
    
table2.index=tickers

final=pd.concat([table,table2],axis=1)


# In[238]:


final


# In[ ]:





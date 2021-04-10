def tear_sheet(returns,riskfreerateannual=0.013,threshold_return=0,headline='I-Strategy'):
    "Expects the dataframe of Returns including the Benchmarks"
    "With Format: strategy-Benchmark1-Benchmar2.....-BenchmarkN"
    "Monthly Compounded Returns Only"
    from tabulate import tabulate
    import pandas as pd
    import numpy as np
    from scipy.stats import norm
    import matplotlib.pyplot as plt

    import seaborn as sb
    sb.set_style('darkgrid')
    import monthly_returns_heatmap as mrh

    def compound(df):
        return ((1+df).prod())-1
    def rollingstd(df):
        return df.std()*np.sqrt(12)
    
    annualreturns=((1+returns).prod())**(12/returns.shape[0])-1
    monthlyreturns=((1+returns).prod())**(1/returns.shape[0])-1
    monthlydeviation=returns.std()
    annualdeviation=(returns.std())*np.sqrt(12)
    semiannualdeviation=(returns[returns<0].std())*np.sqrt(12)
    sharperatio=(annualreturns-riskfreerateannual)/annualdeviation
    sortinoratio=(annualreturns-riskfreerateannual)/semiannualdeviation
    doublingindex=72/(annualreturns*100)
    wealth=(1+returns).cumprod()
    peak=wealth.cummax()
    drawdowns=(wealth-peak)/peak
    annual_return=(((1+returns).prod())**(12/returns.shape[0]))-1
    Roys_safety=(annual_return-threshold_return)/annualdeviation
    
    skew=returns.skew()
    kurt=returns.kurt()
    z = norm.ppf(5/100)
    s = returns.skew()
    k = returns.kurt()
    z = (z +(z**2 - 1)*s/6 +(z**3 -3*z)*(k-3)/24 -(2*z**3 - 5*z)*(s**2)/36)
    var= (-(returns.mean() + z*returns.std(ddof=0)))*100
    
    max_monthly=returns.max()
    min_monthly=returns.min()
    max_month=returns.idxmax()
    min_month=returns.idxmin()
    number=returns.count()
    start=returns.head(1).index
    end=returns.tail(1).index
    
    days=drawdowns[drawdowns<0]
    mini=days.min()
    calmar=annualreturns/-mini
    dd_min=days.min()
    dd_min_day=days.idxmin()
    
    compounded=(1+returns).cumprod()
    absolute=((compounded.iloc[-1]/compounded.iloc[0])-1)*100
    
    sample_yearly=returns.resample(rule='Y').apply(compound)
    yearly_max=sample_yearly.max()
    yearly_max_time=sample_yearly.idxmax()
    yearly_min=sample_yearly.min()
    yearly_min_time=sample_yearly.idxmin()
    
    sample_quarter=returns.resample(rule='Q').apply(compound)
    quarter_max=sample_quarter.max()
    quarter_max_time=sample_quarter.idxmax()
    quarter_min=sample_quarter.min()
    quarter_min_time=sample_quarter.idxmin()
    
    dataframe=pd.DataFrame({"Start-Date":str(returns.index[0]),
                            'End-Date':str(returns.index[-1]),
                            'Total-Months-Tested':returns.count(),
                            "Risk-Free-Rate-Annual":riskfreerateannual*100,
                            "Monthly-Returns":monthlyreturns*100,
                            "CAGR":annualreturns*100,
                            'Absolute-Return':absolute,
                            "Monthly-Volatility":monthlydeviation*100,
                            "Annual-Volatility":annualdeviation*100,
                            'Sharpe-Ratio':sharperatio,
                            'Sortino-Ratio':sortinoratio,
                            'Calmar-Ratio':calmar,
                            "Roy's Safety Ratio with threshold of 0":Roys_safety,
                            'Probabilty of Returns Less than "0"':norm.cdf(-Roys_safety)*100,
                            'Coefficient of Variation':returns.std()/returns.mean(),                    
                            'Wealth-Double-Period':doublingindex,
                            'Arithmetic Mean':returns.mean(),
                            'Median':returns.median(),
                            'Skewness':skew,
                            'Excess of Kurtosis':kurt,
                            'Cornish-Fischer-Var':var,
                            "Maximum-Return-Monthy":max_monthly*100,
                            'Maximum-Return-Yearly':yearly_max*100,
                            "Maximum-Return-Month":max_month,
                            'Maximum-Returns-Year':yearly_max_time,
                            'Maximum-Return-Quarterly':quarter_max*100,
                            'Maximum-Return-Quarter':quarter_max_time,
                            "Minimum-Return-Monthly":min_monthly*100,
                            'Minimum-Return-Yearly':yearly_min*100,
                            "Minimum-Return-Month":min_month,
                            'Minimum-Return-Year':yearly_min_time,
                            'Minimum-Return-Quarterly':quarter_min*100,
                            'Minimum-Return-Quarter':quarter_min_time,
                             "Maximum-Drawdown":dd_min*100,
                             "Maximum-Drawdown-Month":dd_min_day
                            
                            
                            
                            
                            
                            })
    dataframe=round(dataframe,2)
    
    g=print("Performance Metrics: "+headline)
    g1=print(tabulate(dataframe.T,headers=dataframe.index,tablefmt='fancy_grid'))
    c1=print(tabulate(sample_yearly*100,headers=sample_yearly.columns+str(" Yearly Returns"),tablefmt='fancy_grid'))
    c2=print(tabulate(sample_quarter*100,headers=sample_yearly.columns+str(" Quarterly Returns"),tablefmt='fancy_grid'))

    a=sample_yearly.plot.bar(figsize=(15,7),title='Strategy Returns V/S Benchmark "Yearly Basis"',grid=True)
    
    b=sample_quarter.plot.bar(figsize=(15,7),title='Strategy Returns V/S Benchmark "Quarterly Basis"',grid=True)
    
   
    
    ax=drawdowns.plot(figsize=(15,7),title='Drawdowns')
    ax.set_ylabel("Drop")
    
    
    std_df=returns.rolling(window=3).apply(rollingstd)
    std_df.plot(figsize=(15,7),title='Rolling 3 Months Volatility')
    
    ai=((1+returns).cumprod()).plot(figsize=(15,7),title='Wealth-Index of Strategy and Benchmark')# Wealth Index with respect to Benchmark
    
    rolling_q=returns.rolling(window=3).apply(compound).dropna()
    
    
    xx=rolling_q.plot(title='Rolling Quarterly Returns',figsize=(15,7)) 
    
    mrh.plot(returns,figsize=(15,7))

    b=sample_quarter.plot.bar(figsize=(15,7),title='Strategy Returns V/S Benchmark "Quarterly Basis"',grid=True)
    
    ax=((1+pd.DataFrame(returns.iloc[:, 0])).cumprod()).plot.line(figsize=(15,7),title='Wealth-Index With Drawdowns and Monthly Returns of Strategy',sharex=True,color='Red',grid=True)
    
    ax.plot(pd.DataFrame(drawdowns.iloc[:, 0]))
    ax.plot(pd.DataFrame(returns.iloc[:, 0]))
    plt.legend(labels=["Wealth",'drawdowns','Monthly Returns'])
    
    returns.plot(figsize=(15,7))

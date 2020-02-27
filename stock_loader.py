import os
import pandas as pd
import numpy as np
import datetime as dt

def symbol_to_path(symbol, base_dir=None):                                                                                                                                                                                                                                                      
    """Return CSV file path given ticker symbol."""                                                                                                                                                                                                                                                     
    if base_dir is None:                                                                                                                                                                                                                                                        
        base_dir = os.environ.get("MARKET_DATA_DIR", 'data/')                                                                                                                                                                                                                                                        
    return os.path.join(base_dir, "{}.csv".format(str(symbol)))                                                                                                                                                                                                                                                         
                                                                                                                                                                                                                                                        
def get_data(symbols, dates, addSPY=True, colname = 'Adj Close'):                                                                                                                                                                                                                                                       
    """Read stock data (adjusted close) for given symbols from CSV files."""                                                                                                                                                                                                                                                    
    df = pd.DataFrame(index=dates)                                                                                                                                                                                                                                                      
    if addSPY and 'SPY' not in symbols:  # add SPY for reference, if absent                                                                                                                                                                                                                                                     
        symbols = ['SPY'] + list(symbols) # handles the case where symbols is np array of 'object'                                                                                                                                                                                                                                                      
                                                                                                                                                                                                                                                        
    for symbol in symbols:                                                                                                                                                                                                                                                      
        df_temp = pd.read_csv(symbol_to_path(symbol), index_col='Date',                                                                                                                                                                                                                                                         
                parse_dates=True, usecols=['Date', colname], na_values=['nan'])                                                                                                                                                                                                                                                         
        df_temp = df_temp.rename(columns={colname: symbol})                                                                                                                                                                                                                                                     
        df = df.join(df_temp)                                                                                                                                                                                                                                                   
        if symbol == 'SPY':  # drop dates SPY did not trade                                                                                                                                                                                                                                                     
            df = df.dropna(subset=["SPY"])                                                                                                                                                                                                                                                      
                                                                                                                                                                                                                                                        
    return df

if __name__=="__main__":                                                                                                                                    
    
    print("Let us fetch data for Google, Apple and SPY500")
    
    start = dt.datetime(2008, 1, 1)
    end = dt.datetime(2009, 1, 1)

    prices = get_data(symbols=['GOOG', 'AAPL', 'SPY'], dates=pd.date_range(start, end))
    print("Size of the returned dataframe")
    print(prices.shape)
    normed = prices / prices.values[0]
    
    # arbitrary allocations for each stock
    allocs = [0.4, 0.4, 0.2]
    alloced = normed * allocs
    start_val = 1000000

    pos_vals = alloced * start_val

    port_val = pos_vals.sum(axis=1) # Sum across columns

    # compute statistics
    daily_returns = (port_val / port_val.shift(1)) - 1
    daily_returns.iloc[0] = 0
    daily_returns = daily_returns[1:]

    # cumulative return
    cumulative_returns = port_val[-1]/port_val[0] - 1

    # avg and std daily returns
    avg_daily_returns = daily_returns.mean()
    std_daily_returns = daily_returns.std()

    # sharpe ratio (indicator for risk adjusted return)
    # multiply with the sampling rate which is sqrt of 252 days of trading
    sharpe_ratio = np.sqrt(252) * (avg_daily_returns / std_daily_returns)

    
    print("avg daily returns: ", avg_daily_returns)
    print("cumulative return: ", cumulative_returns)
    print("std daily return: ", std_daily_returns)
    print("sharpe ratio: ", sharpe_ratio)




    


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

    df = get_data(symbols=['GOOG', 'AAPL', 'SPY'], dates=pd.date_range(start, end))
    print("Size of the returned dataframe")
    print(df.shape)

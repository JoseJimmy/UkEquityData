import os
import pandas as pd
from pandas._libs.parsers import EmptyDataError

data_loc = r'c:/data/data'

def getFileNames(dir,filt_key='.',ext='.csv'):
    Files = []
    for file in os.listdir(dir):
        if file.endswith(ext):
            if file.lower().count(filt_key.lower()) > 0:
                Files.append(os.path.join(dir, file))
    return Files

ratio_files = getFileNames(data_loc,'ratios')
bal_files = getFileNames(data_loc,'balance')
inc_files = getFileNames(data_loc,'income')
cash_files = getFileNames(data_loc,'cash')
price_files = getFileNames(data_loc,'prices')

def fetch_csv_df(file,date_col):
    tic = file.split('_')[1]
    try :
        df = pd.read_csv(file, index_col=0, header=None).T
    except EmptyDataError:
        return pd.DataFrame([])
    df.insert(loc=0, column='Ticker', value=tic)
    for col in date_cols:
        df[col] = pd.to_datetime(df[col])
    return df

def df_column_uniquify(df):
    df_columns = df.columns
    new_columns = []
    for item in df_columns:
        counter = 0
        newitem = item
        while newitem in new_columns:
            counter += 1
            newitem = "{}_{}".format(item, counter)
        new_columns.append(newitem)
    df.columns = new_columns
    return df


## Ratios
ratios = pd.DataFrame([])
date_cols = ['Year','Period Ending']
for file in ratio_files[0:20]:
    df = fetch_csv_df(file,date_cols)
    ratios = ratios.append(df, ignore_index=True, sort=False)
ratios = ratios.set_index('Ticker')


incomes = pd.DataFrame([])
comm_col = set()
date_cols = ['Year','Period Ending']
for file in inc_files:
    df = fetch_csv_df(file,date_cols)
    if(df.empty):
        continue
    df=df_column_uniquify(df)
    incomes = incomes.append(df, ignore_index=True,verify_integrity=False)
incomes = incomes.set_index('Ticker')


bals = pd.DataFrame([])
comm_col = set()
date_cols = ['Year','Period Ending']
for file in bal_files:
    df = fetch_csv_df(file,date_cols)
    if(df.empty):
        continue
    df=df_column_uniquify(df)
    bals = bals.append(df, ignore_index=True,verify_integrity=False)
bals = bals.set_index('Ticker')


cashfs = pd.DataFrame([])
comm_col = set()
date_cols = ['Year','Period Ending']
for idx,file in enumerate(cash_files):
    print(idx,'-',file)
    df = fetch_csv_df(file,date_cols)
    if(df.empty):
        continue
    df=df_column_uniquify(df)
    cashfs = cashfs.append(df, ignore_index=True,verify_integrity=False)
cashfs = cashfs.set_index('Ticker')


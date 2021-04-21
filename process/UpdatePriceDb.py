from sqlalchemy import Float
from process.helper_fncs import *
from sqlalchemy import (MetaData, Table, Column, String,
                        create_engine, Date)
from sqlalchemy.dialects.mysql import insert

from tqdm import tqdm
from settings import *
import pandas as pd

import numpy as np

###################################################################################
# DB Connection and define table
###################################################################################

engine = create_engine(CONNECTION_STRING)
connection = engine.connect()
metadata = MetaData()
db_Prices_table = Table('prices', metadata,
               Column('Ticker', String(30), primary_key=True),
               Column('Date', Date, primary_key=True),
               Column('Open', Float),
               Column('High', Float),
               Column('Low', Float),
               Column('Close', Float),
               Column('Change', Float),
               Column('Volume',Float),
               Column('Adjustment', Float))


metadata.create_all(engine)
###################################################################################
# process csv to db
###################################################################################

tic2exch_dict = tic_to_exchange()
tracker = load_tracker()

for col in ['Price_start', 'Price_end']:
    tracker[col] = pd.to_datetime(tracker[col])
files_to_delete = []
price_files = getFileNames(price_folder, 'prices', '.csv')

pbar = tqdm(price_files)
idx = 0
for file in price_files:
    # pbar.set_description("Processing %50s" % file.split('\\')[-1])
    print("Processing %50s" % file.split('\\')[-1])

    df = pd.read_csv(file, low_memory=False)
    df = df[~(df['TIDM'] == 'TIDM')]
    df = df[~(df['TIDM'] == 'undefinedTIDM')]
    df['Date'] = pd.to_datetime(df['Date'], dayfirst=True)
    df = df.rename(columns={'TIDM': 'Ticker','Change%': 'Change'})
    df['Ticker'] = df['Ticker'].map(tic2exch_dict.get)
    # df = df.replace({'Ticker':tic2exch_dict})
    df = df.set_index('Ticker', drop=False)
    df = df[df.index.isin(tracker.index)]
    tics = df.index.unique()
    float_cols = ['Open', 'High', 'Low', 'Close', 'Change', 'Volume', 'Adjustment']
    df[float_cols] = df[float_cols].apply(pd.to_numeric)
    df['Change'] = df['Change'].fillna((df.Close / df.Open) - 1)
    df = df[df['Close'] != 0]
    hi_chg_msk = df['Change']> 500
    df.loc[hi_chg_msk, 'Change'] = (df.loc[hi_chg_msk, 'Close'] / df.loc[hi_chg_msk, 'Open']) - 1
    tic_list=''
    for tic in tics:
        tic_df = df.loc[[tic]].copy()
        tic_df['Volume'] = tic_df['Volume'].replace([np.inf, -np.inf], np.nan)
        tic_df['Volume'] = tic_df['Volume'].fillna(tic_df['Volume'].interpolate())
        tic_df['Volume'] = tic_df['Volume'].fillna(tic_df['Volume'].fillna(0).mean())
        tic_df['Volume'] = tic_df['Volume'].astype(int)
        tic_df = tic_df.drop_duplicates(subset=['Date'])
        tic_df = tic_df.round(2)
        tic_df = tic_df.loc[tic_df['Close'] != 0]
        tic_df = tic_df.fillna(0)
        ins_records = tic_df.to_dict('records')
        insert_stmt = insert(db_Prices_table).values(ins_records)
        update_dict = {x.name: x for x in insert_stmt.inserted}
        upsert_query = insert_stmt.on_duplicate_key_update(update_dict)
        result = connection.execute(upsert_query)
        print('%d... Copied %s Last Date'%(idx,tic,))
        idx+=1
        tic_list = tic_list + ' '+tic

connection.close()

